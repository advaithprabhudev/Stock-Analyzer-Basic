# 📈 Stock Analyzer App

> ⚠️ **Disclaimer:** This tool is for educational purposes only and should not be considered financial advice. Always do your own research and consult with a qualified financial advisor before making investment decisions.


A simple web app I built for analyzing stock data. You can check out historical prices, volumes, and some cool charts!

## What does it do?

This app lets you:
- Enter any stock ticker (like AAPL for Apple)
- Pick a date range to analyze
- See price charts with moving averages
- Check out trading volume
- Look at daily returns and percentage changes
- View some cool 3D visualizations

## Technologies I used

- **Streamlit** - for the web interface
- **yfinance** - to download stock data from Yahoo Finance
- **Pandas** - for data manipulation
- **Matplotlib** - for creating charts
- **Plotly** - for the 3D graph
- **Seaborn** - for styling
- **NumPy** - for calculations

## How to run it

1. First, clone this repo or download the code

2. Install the required packages:
```bash
pip install streamlit pandas numpy matplotlib yfinance plotly seaborn
```

3. Run the app:
```bash
streamlit run app.py
```

4. It should open in your browser automatically!

## How to use

1. Type in a stock ticker symbol (like TSLA, AAPL, MSFT, etc.)
2. Choose your start and end dates
3. Click through the different tabs:
   - **Analytics** - basic price data
   - **Metrics** - daily changes and percentages
   - **Key Metrics** - current price, 52-week highs/lows
   - **Charts** - price history and volume charts
   - **Summary** - cool 3D visualization of price data

## Features

- 📊 Interactive charts
- 💹 Real-time data from Yahoo Finance
- 📉 50-day moving averages
- 📈 Volume analysis with smart scaling (K, M, B)
- 🎨 Clean UI with multiple tabs
- 💾 View raw data option
- 🎯 52-week high/low tracking

## Notes

- The app caches data so it doesn't keep re-downloading the same stuff
- You can enter multiple tickers separated by commas (though some features work better with one ticker)
- Data comes from Yahoo Finance so you need internet connection
- Some calculations might take a second depending on the date range

## Future improvements

If I have time, I might add:
- Comparison between multiple stocks
- More technical indicators
- Export to CSV feature
- Better error handling
- Dark mode theme

## Disclaimer

This is just a learning project! Don't use this for actual investment decisions. I'm not a financial advisor lol.

---


Made with ❤️ and lots of Stack Overflow 😅
