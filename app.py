from flask import Flask, jsonify
import yfinance as yf
import numpy as np
from datetime import datetime

app = Flask(__name__)

@app.route('/top-ten-sharpe-ratios')
def top_ten_sharpe_ratios():
    end_date = datetime.now().strftime('%Y-%m-%d')
    sharpe_threshold = 0.04
    top_ten_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'JPM', 'BAC', 'WMT', 'V']

    sharpe_ratios = []

    for ticker_symbol in top_ten_tickers:
        ticker_info = yf.Ticker(ticker_symbol)
        ticker_history = ticker_info.history(period="max")
        if not ticker_history.empty:
            start_date = ticker_history.index[0].strftime('%Y-%m-%d')
            stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
            if not stock_data['Close'].empty:
                stock_data['Daily_Return'] = stock_data['Close'].pct_change()
                risk_free_rate = 0.03
                daily_risk_free_rate = (1 + risk_free_rate) ** (1/252) - 1
                daily_returns = stock_data['Daily_Return']
                sharpe_ratio = np.mean(daily_returns - daily_risk_free_rate) / np.std(daily_returns)
                sharpe_ratios.append((ticker_symbol, sharpe_ratio))

    sorted_sharpe_ratios = sorted(sharpe_ratios, key=lambda x: x[1], reverse=True)

    top_ten = [{'Ticker': ticker, 'Sharpe Ratio': ratio} for ticker, ratio in sorted_sharpe_ratios[:10]]

    return jsonify({'top_ten_sharpe_ratios': top_ten})

if __name__ == '__main__':
    app.run(debug=True)
