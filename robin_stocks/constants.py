import requests

Session = requests.Session()
Session.headers = {
"Accept": "*/*",
"Accept-Encoding": "gzip,defalte,br",
"Accept-Language": "en-US,en;q=1",
"Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
"X-Robinhood-API-Version": "1.0.0",
"Connection": "keep-alive",
"User-Agent": "Robinhood/823 (iphone; iOS 7.1.2, Scale/2.00)"
}
