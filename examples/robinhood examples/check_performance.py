#!/usr/bin/env python3
"""
Enhanced portfolio performance checker with senior-level Python patterns.

Features:
- Type hints and dataclasses for type safety
- Progress bars with tqdm
- Retry logic with exponential backoff
- Rate limiting
- Structured logging
- Context managers for resource cleanup
- Separation of concerns
"""

import os
import sys
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from contextlib import contextmanager
from functools import wraps
import time

# Add repo root to path if needed
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(script_dir))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import robin_stocks.robinhood as r
from dotenv import load_dotenv
import pyotp

# Try to import requests-cache for HTTP response caching
try:
    from requests_cache import CachedSession, install_cache
    from requests_cache.backends import SQLiteCache
    HAS_REQUESTS_CACHE = True
except ImportError:
    HAS_REQUESTS_CACHE = False

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    # Fallback progress indicator with periodic updates
    class tqdm:
        def __init__(self, iterable, desc=None, unit="item", **kwargs):
            self.iterable = iterable
            self.desc = desc or "Processing"
            self.unit = unit
            self.total = len(iterable) if hasattr(iterable, '__len__') else None
            self.count = 0
            
        def __iter__(self):
            for item in self.iterable:
                self.count += 1
                if self.count % 10 == 0 or self.count == 1:
                    if self.total:
                        pct = (self.count / self.total) * 100
                        print(f"\r{self.desc}: {self.count}/{self.total} {self.unit}s ({pct:.1f}%)", end="", flush=True)
                    else:
                        print(f"\r{self.desc}: {self.count} {self.unit}s", end="", flush=True)
                yield item
            print()  # New line when done

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


@dataclass
class PositionPerformance:
    """Data class for position performance metrics."""
    ticker: str
    daily_gain: float
    percent_change: float
    equity: float
    quantity: float
    portfolio_percentage: float
    name: Optional[str] = None


@dataclass
class PortfolioConfig:
    """Configuration for portfolio operations."""
    rate_limit_delay: float = 1.0
    max_retries: int = 3
    retry_delay: float = 2.0
    show_progress: bool = True
    # Cache expiration settings (in seconds)
    cache_fundamentals_expiry: int = 86400  # 24 hours - fundamentals rarely change
    cache_prices_expiry: int = 300  # 5 minutes - prices update frequently
    cache_instruments_expiry: int = 3600  # 1 hour - instrument data changes infrequently
    cache_enabled: bool = True  # Enable/disable caching


def retry_on_failure(max_retries: int = 3, delay: float = 2.0, backoff: float = 2.0):
    """Decorator for retrying functions with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        wait_time = delay * (backoff ** attempt)
                        error_msg = str(e).lower()
                        if '429' in error_msg or 'rate limit' in error_msg:
                            logger.warning(
                                f"Rate limited. Retrying in {wait_time:.1f}s "
                                f"(attempt {attempt + 1}/{max_retries})..."
                            )
                        else:
                            logger.warning(
                                f"Error: {e}. Retrying in {wait_time:.1f}s "
                                f"(attempt {attempt + 1}/{max_retries})..."
                            )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Failed after {max_retries} attempts: {e}")
            raise last_exception
        return wrapper
    return decorator


@contextmanager
def robinhood_session(config: PortfolioConfig):
    """Context manager for Robinhood session with automatic cleanup and caching."""
    load_dotenv()
    username = os.getenv('robin_username')
    password = os.getenv('robin_password')
    mfa_secret = os.getenv('robin_mfa')
    
    if not username:
        username = input("Enter Robinhood username: ")
    if not password:
        password = input("Enter Robinhood password: ")
    
    # Setup HTTP caching if enabled and available
    cache_installed = False
    if config.cache_enabled and HAS_REQUESTS_CACHE:
        try:
            # Get repo root (same logic as at top of file)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            repo_root_local = os.path.dirname(os.path.dirname(script_dir))
            
            # Create cache directory if it doesn't exist
            cache_dir = os.path.join(repo_root_local, '.cache', 'robinhood_api')
            os.makedirs(cache_dir, exist_ok=True)
            cache_file = os.path.join(cache_dir, 'api_cache.sqlite')
            
            # Install cache with URL-specific expiration rules
            from requests_cache import install_cache
            
            # Configure cache with different expiration times for different endpoints
            # URLs matching patterns get different expiration times
            install_cache(
                cache_name=cache_file,
                backend='sqlite',
                # Match URLs containing these patterns with specific expiration times
                urls_expire_after={
                    '*/fundamentals/': config.cache_fundamentals_expiry,
                    '*/quotes/': config.cache_prices_expiry,
                    '*/instruments/': config.cache_instruments_expiry,
                    '*': 60,  # Default 1 minute for other endpoints
                }
            )
            cache_installed = True
            logger.info("HTTP caching enabled (fundamentals: 24h, prices: 5min, instruments: 1h)")
        except Exception as e:
            logger.warning(f"Failed to setup HTTP caching: {e}. Continuing without cache.")
    elif config.cache_enabled and not HAS_REQUESTS_CACHE:
        logger.info("HTTP caching disabled - requests-cache not installed. Install with: pip install requests-cache")
    
    logger.info("Authenticating with Robinhood...")
    try:
        if mfa_secret:
            totp = pyotp.TOTP(mfa_secret)
            mfa_code = totp.now()
            r.login(username, password, mfa_code=mfa_code)
        else:
            r.login(username, password)
        
        # Enable rate limiting
        r.enable_rate_limiting(delay=config.rate_limit_delay)
        logger.info("Login successful. Rate limiting enabled.")
        
        yield
        
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise
    finally:
        try:
            r.logout()
            logger.info("Logged out successfully.")
        except Exception:
            pass
        
        # Clear cache if it was installed
        if cache_installed and HAS_REQUESTS_CACHE:
            try:
                from requests_cache import clear
                # Don't clear on exit - let it persist for next run
                # clear()  # Uncomment if you want to clear cache on exit
            except Exception:
                pass


class PortfolioAnalyzer:
    """Analyzes portfolio performance with progress tracking."""
    
    def __init__(self, config: PortfolioConfig):
        self.config = config
        self.holdings: Dict[str, Dict] = {}
        self.positions: List[Dict] = []
    
    def _fetch_batch_with_retry(self, symbols: List[str], fetch_func, data_key: str, 
                                 initial_chunk_size: int = 50, min_chunk_size: int = 10):
        """
        Fetch data in batches with automatic retry using smaller chunks on failure.
        
        Args:
            symbols: List of symbols to fetch
            fetch_func: Function to call for batch fetching (e.g., r.get_fundamentals)
            data_key: Key for logging (e.g., 'fundamentals')
            initial_chunk_size: Starting chunk size
            min_chunk_size: Minimum chunk size before falling back to individual calls
        
        Returns:
            Dictionary mapping symbol to fetched data
        """
        result_data = {}
        symbols_list = list(symbols)
        chunk_size = initial_chunk_size
        
        iterator = range(0, len(symbols_list), chunk_size)
        if self.config.show_progress:
            iterator = tqdm(range(0, len(symbols_list), chunk_size), 
                          desc=f"Fetching {data_key}", unit="chunk")
        
        for i in iterator:
            chunk = symbols_list[i:i + chunk_size]
            success = False
            retry_chunk_size = chunk_size
            
            # Try batch fetch, retry with smaller chunks if needed
            while not success and retry_chunk_size >= min_chunk_size:
                try:
                    batch_result = fetch_func(chunk)
                    if batch_result:
                        # Process results
                        for j, symbol in enumerate(chunk):
                            if j < len(batch_result) and batch_result[j]:
                                result_data[symbol] = batch_result[j]
                        success = True
                    else:
                        # Empty result, try smaller chunks
                        retry_chunk_size = max(min_chunk_size, retry_chunk_size // 2)
                        if retry_chunk_size < chunk_size:
                            logger.debug(f"Empty result for {data_key} chunk, retrying with size {retry_chunk_size}")
                        
                except Exception as e:
                    error_msg = str(e).lower()
                    # Check if it's a 400 Bad Request (likely URL too long)
                    if '400' in error_msg or 'bad request' in error_msg or 'url' in error_msg:
                        # Reduce chunk size and retry
                        retry_chunk_size = max(min_chunk_size, retry_chunk_size // 2)
                        if retry_chunk_size < chunk_size:
                            logger.warning(
                                f"400 error for {data_key} chunk (size {chunk_size}), "
                                f"retrying with smaller chunks (size {retry_chunk_size})"
                            )
                            # Split chunk into smaller pieces
                            for sub_i in range(0, len(chunk), retry_chunk_size):
                                sub_chunk = chunk[sub_i:sub_i + retry_chunk_size]
                                try:
                                    sub_result = fetch_func(sub_chunk)
                                    if sub_result:
                                        for j, symbol in enumerate(sub_chunk):
                                            if j < len(sub_result) and sub_result[j]:
                                                result_data[symbol] = sub_result[j]
                                except Exception as sub_e:
                                    logger.warning(f"Error fetching {data_key} sub-chunk: {sub_e}")
                                    # Fallback to individual calls for this sub-chunk
                                    for symbol in sub_chunk:
                                        try:
                                            individual_result = fetch_func([symbol])
                                            if individual_result and individual_result[0]:
                                                result_data[symbol] = individual_result[0]
                                        except Exception:
                                            pass
                            success = True  # Mark as handled
                        else:
                            # Already at minimum, fall through to individual calls
                            success = False
                            break
                    else:
                        # Other error, log and try individual calls
                        logger.warning(f"Error fetching {data_key} chunk: {e}")
                        success = False
                        break
            
            # Fallback to individual calls if batch failed
            if not success:
                logger.debug(f"Falling back to individual calls for {data_key} chunk")
                for symbol in chunk:
                    if symbol not in result_data:  # Only fetch if not already retrieved
                        try:
                            individual_result = fetch_func([symbol])
                            if individual_result and individual_result[0]:
                                result_data[symbol] = individual_result[0]
                        except Exception as ind_e:
                            logger.debug(f"Failed to fetch {data_key} for {symbol}: {ind_e}")
                            pass
        
        return result_data
    
    @retry_on_failure(max_retries=3, delay=2.0)
    def fetch_positions(self) -> List[Dict]:
        """Fetch open stock positions with retry logic."""
        logger.info("Fetching open stock positions...")
        positions = r.get_open_stock_positions()
        logger.info(f"Found {len(positions)} positions")
        return positions
    
    @retry_on_failure(max_retries=3, delay=2.0)
    def fetch_holdings(self) -> Dict[str, Dict]:
        """Fetch comprehensive holdings data with progress tracking."""
        logger.info("Building comprehensive holdings data...")
        
        # Get position count first for progress estimation
        positions_data = r.get_open_stock_positions()
        portfolios_data = r.load_portfolio_profile()
        accounts_data = r.load_account_profile()
        
        if not positions_data or not portfolios_data or not accounts_data:
            logger.warning("No positions found")
            return {}
        
        # Filter out None positions
        valid_positions = [p for p in positions_data if p]
        num_positions = len(valid_positions)
        logger.info(f"Found {num_positions} positions to process")
        
        if num_positions == 0:
            logger.warning("No positions found")
            return {}
        
        # Calculate total equity
        if portfolios_data['extended_hours_equity'] is not None:
            total_equity = max(float(portfolios_data['equity']), float(
                portfolios_data['extended_hours_equity']))
        else:
            total_equity = float(portfolios_data['equity'])
        
        cash = float(accounts_data['cash']) + float(accounts_data['uncleared_deposits'])
        
        # Step 1: Extract all symbols (with progress)
        logger.info("Step 1/4: Extracting symbols from positions...")
        symbols_data = {}
        iterator = valid_positions
        if self.config.show_progress:
            iterator = tqdm(valid_positions, desc="Extracting symbols", unit="position")
        
        for item in iterator:
            try:
                instrument_data = r.get_instrument_by_url(item['instrument'])
                symbol = instrument_data['symbol']
                symbols_data[symbol] = {
                    'instrument_data': instrument_data,
                    'position': item
                }
            except Exception as e:
                logger.warning(f"Failed to extract symbol: {e}")
                continue
        
        symbols = list(symbols_data.keys())
        logger.info(f"Extracted {len(symbols)} symbols")
        
        if not symbols:
            logger.warning("No valid symbols found")
            return {}
        
        # Step 2: Batch fetch fundamentals (with automatic retry on errors)
        logger.info("Step 2/4: Batch fetching fundamentals...")
        fundamentals_data = self._fetch_batch_with_retry(
            symbols, 
            r.get_fundamentals, 
            'fundamentals',
            initial_chunk_size=50,
            min_chunk_size=10
        )
        
        if self.config.show_progress:
            logger.info(f"  Fetched fundamentals for {len(fundamentals_data)}/{len(symbols)} symbols...")
        
        # Step 3: Batch fetch prices (with automatic retry on errors)
        logger.info("Step 3/4: Batch fetching prices...")
        prices_data = self._fetch_batch_with_retry(
            symbols,
            r.get_latest_price,
            'prices',
            initial_chunk_size=50,
            min_chunk_size=10
        )
        
        if self.config.show_progress:
            logger.info(f"  Fetched prices for {len(prices_data)}/{len(symbols)} symbols...")
        
        # Step 4: Build holdings dictionary (with progress)
        logger.info("Step 4/4: Building holdings dictionary...")
        holdings = {}
        iterator = symbols
        if self.config.show_progress:
            iterator = tqdm(symbols, desc="Building holdings", unit="symbol")
        
        for symbol in iterator:
            try:
                symbol_info = symbols_data[symbol]
                item = symbol_info['position']
                instrument_data = symbol_info['instrument_data']
                
                # Get data (use cached/batched data when available)
                fundamental_data = fundamentals_data.get(symbol)
                if not fundamental_data:
                    fundamental_data = r.get_fundamentals(symbol)[0] if r.get_fundamentals(symbol) else {}
                
                price = prices_data.get(symbol)
                if not price:
                    price = r.get_latest_price(symbol)[0] if r.get_latest_price(symbol) else "0"
                
                quantity = item['quantity']
                equity = float(quantity) * float(price)
                equity_change = (float(quantity) * float(price)) - \
                    (float(quantity) * float(item['average_buy_price']))
                percentage = float(quantity) * float(price) * \
                    100 / (float(total_equity) - float(cash)) if (float(total_equity) - float(cash)) > 0 else 0
                
                if (float(item['average_buy_price']) == 0.0):
                    percent_change = 0.0
                else:
                    percent_change = (float(price) - float(item['average_buy_price'])) * 100 / float(item['average_buy_price'])
                
                if (float(item['intraday_average_buy_price']) == 0.0):
                    intraday_percent_change = 0.0
                else:
                    intraday_percent_change = (float(price) - float(item['intraday_average_buy_price'])) * 100 / float(item['intraday_average_buy_price'])
                
                holdings[symbol] = {
                    'price': price,
                    'quantity': quantity,
                    'average_buy_price': item['average_buy_price'],
                    'equity': "{0:.2f}".format(equity),
                    'percent_change': "{0:.2f}".format(percent_change),
                    'intraday_percent_change': "{0:.2f}".format(intraday_percent_change),
                    'equity_change': "{0:2f}".format(equity_change),
                    'type': instrument_data['type'],
                    'name': r.get_name_by_symbol(symbol),
                    'id': instrument_data['id'],
                    'pe_ratio': fundamental_data.get('pe_ratio', '') if fundamental_data else '',
                    'percentage': "{0:.2f}".format(percentage)
                }
            except Exception as e:
                logger.warning(f"Error processing {symbol}: {e}")
                continue
        
        logger.info(f"Retrieved holdings for {len(holdings)} stocks")
        return holdings
    
    def calculate_performance(
        self,
        holdings: Dict[str, Dict]
    ) -> List[PositionPerformance]:
        """Calculate performance metrics from holdings data (already has everything we need)."""
        logger.info("Calculating performance metrics...")
        
        performance_data = []
        for ticker, holding_data in holdings.items():
            # build_holdings() already provides all this data!
            equity = float(holding_data.get('equity', 0))
            quantity = float(holding_data.get('quantity', 0))
            percent_change = float(holding_data.get('percent_change', 0))
            price = float(holding_data.get('price', 0))
            avg_buy_price = float(holding_data.get('average_buy_price', 0))
            
            # Calculate daily gain (current equity - cost basis)
            cost_basis = quantity * avg_buy_price if avg_buy_price > 0 else 0
            daily_gain = equity - cost_basis
            
            performance_data.append(
                PositionPerformance(
                    ticker=ticker,
                    daily_gain=daily_gain,
                    percent_change=percent_change,
                    equity=equity,
                    quantity=quantity,
                    portfolio_percentage=float(holding_data.get('percentage', 0)),
                    name=holding_data.get('name')
                )
            )
        
        return sorted(performance_data, key=lambda x: x.daily_gain, reverse=True)
    
    def generate_summary(self, performance_data: List[PositionPerformance]) -> Dict:
        """Generate portfolio summary statistics."""
        total_equity = sum(p.equity for p in performance_data)
        net_gain = sum(p.daily_gain for p in performance_data)
        
        return {
            'total_positions': len(performance_data),
            'total_equity': total_equity,
            'net_daily_gain': net_gain,
            'top_gainers': sorted(performance_data, key=lambda x: x.daily_gain, reverse=True)[:10],
            'top_losers': sorted(performance_data, key=lambda x: x.daily_gain)[:10],
        }
    
    def display_performance(self, performance_data: List[PositionPerformance]):
        """Display performance report in formatted table."""
        print("\n" + "=" * 100)
        print("MY POSITIONS PERFORMANCE (Daily)")
        print("=" * 100)
        print(f"{'Ticker':<8} {'Daily Gain':>12} {'% Change':>10} {'Equity':>12} {'Qty':>10} {'% Portfolio':>12} {'Name':<30}")
        print("-" * 100)
        
        iterator = performance_data
        if self.config.show_progress:
            iterator = tqdm(performance_data, desc="Generating report", unit="position")
        
        for perf in iterator:
            name = (perf.name[:27] + "...") if perf.name and len(perf.name) > 30 else (perf.name or "N/A")
            print(
                f"{perf.ticker:<8} "
                f"${perf.daily_gain:>11.2f} "
                f"{perf.percent_change:>9.2f}% "
                f"${perf.equity:>11.2f} "
                f"{perf.quantity:>9.4f} "
                f"{perf.portfolio_percentage:>11.2f}% "
                f"{name:<30}"
            )
        
        print("-" * 100)
    
    def display_summary(self, summary: Dict):
        """Display portfolio summary."""
        print("\n" + "=" * 100)
        print("PORTFOLIO SUMMARY")
        print("=" * 100)
        print(f"Total Positions: {summary['total_positions']}")
        print(f"Total Equity: ${summary['total_equity']:,.2f}")
        print(f"Net Daily Gain: ${summary['net_daily_gain']:,.2f}")
        
        print("\nTop 10 Gainers:")
        for i, perf in enumerate(summary['top_gainers'], 1):
            print(f"  {i:2}. {perf.ticker:<6} ${perf.daily_gain:>10,.2f} ({perf.percent_change:>6.2f}%)")
        
        print("\nTop 10 Losers:")
        for i, perf in enumerate(summary['top_losers'], 1):
            print(f"  {i:2}. {perf.ticker:<6} ${perf.daily_gain:>10,.2f} ({perf.percent_change:>6.2f}%)")


def main():
    """Main execution function."""
    config = PortfolioConfig(
        rate_limit_delay=0.5,  # Reduced from 1.0s - batching reduces API calls significantly
        max_retries=3,
        retry_delay=2.0,
        show_progress=True,
        cache_enabled=True,  # Enable HTTP caching for faster repeated runs
        cache_fundamentals_expiry=86400,  # 24 hours
        cache_prices_expiry=300,  # 5 minutes
        cache_instruments_expiry=3600  # 1 hour
    )
    
    analyzer = PortfolioAnalyzer(config)
    
    try:
        with robinhood_session(config):
            # Fetch data
            positions = analyzer.fetch_positions()
            
            if not positions:
                logger.warning("No positions found in account.")
                return
            
            holdings = analyzer.fetch_holdings()
            
            if not holdings:
                logger.warning("No holdings data retrieved.")
                return
            
            # Calculate performance directly from holdings (no redundant API calls!)
            performance_data = analyzer.calculate_performance(holdings)
            
            # Display results
            analyzer.display_performance(performance_data)
            
            # Generate and display summary
            summary = analyzer.generate_summary(performance_data)
            analyzer.display_summary(summary)
            
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
