import sys
sys.path.insert(1,'/Users/Kevincheng96/Documents/Coding Projects/Python projects/examples')
sys.path.insert(2,'/Users/Kevincheng96/Documents/Coding Projects/Python projects/robin_stocks')

from flask import Flask

from actions import generate_portfolio_summary

app = Flask(__name__)

@app.route('/')
def index():
	return generate_portfolio_summary()