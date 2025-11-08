# Recurring Investments Examples

This directory contains example scripts demonstrating how to use the recurring investments API.

## Prerequisites

1. Install dependencies:
   ```bash
   pip install robin_stocks python-dotenv pyotp
   ```

2. Create a `.env` file in the repository root with:
   ```
   robin_username=your_email@example.com
   robin_password=your_password
   robin_mfa=your_mfa_secret  # Optional, only if you use 2FA
   ```

## Example Scripts

### 1. `get_all_recurring.py`
Fetch and display all your recurring investments.

```bash
python examples/recurring_investments/get_all_recurring.py
```

### 2. `create_recurring.py`
Create a single recurring investment.

```bash
python examples/recurring_investments/create_recurring.py
```

Edit the script to change:
- `symbol` - Stock/ETF symbol
- `amount` - Dollar amount per period
- `frequency` - 'daily', 'weekly', 'biweekly', or 'monthly'

### 3. `cancel_recurring.py`
Cancel a recurring investment by its schedule ID.

```bash
python examples/recurring_investments/cancel_recurring.py
```

### 4. `create_from_csv.py`
Create multiple recurring investments from a CSV file.

First, create an `investments.csv` file:
```csv
symbol,amount,frequency
TSLA,50,weekly
AAPL,100,monthly
SPY,200,biweekly
```

Then run:
```bash
python examples/recurring_investments/create_from_csv.py
```

## Using the Library Directly

You can also use the functions directly in your own scripts:

```python
import robin_stocks.robinhood as rh

# Login
rh.login(username='...', password='...')

# Get all recurring investments
investments = rh.get_recurring_investments()

# Create a new one
rh.create_recurring_investment('TSLA', 50.0, frequency='weekly')

# Update (pause/resume)
rh.update_recurring_investment(schedule_id, state='paused')

# Cancel
rh.cancel_recurring_investment(schedule_id)
```

## Available Functions

- `rh.get_recurring_investments()` - Get all recurring investments
- `rh.create_recurring_investment(symbol, amount, frequency='weekly')` - Create new
- `rh.update_recurring_investment(schedule_id, state='paused')` - Update/pause/resume
- `rh.cancel_recurring_investment(schedule_id)` - Cancel
- `rh.get_next_investment_date(frequency='weekly')` - Get next date

## Notes

- These functions use Robinhood's native recurring investments feature
- Once created, Robinhood handles the scheduling automatically
- No need for cron/pm2 scripts - Robinhood does it all!

