import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go


@st.cache_data
def data_fetching(ticker_list, start_date, end_date):
    data = yf.download(tickers=ticker_list, start=start_date, end=end_date)
    df = pd.DataFrame(data)
    return df


st.set_page_config(
    page_title="Stock Analyzer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="auto"
)

st.title("💰 Simple Stock Analyzer")

st.write("A web-based stock analysis tool that allows users to visualize and analyze historical stock performance. Enter any stock ticker symbol, select a date range, and instantly view price trends, trading volume, daily returns, and key performance metrics. Perfect for investors and traders who want quick insights into stock behavior over time.")
st.divider()


today = datetime.date.today()
one_year_before = today - datetime.timedelta(days=365)
st.warning("⚠️ Disclaimer: This tool is for educational purposes only and should not be considered financial advice. Always do your own research and consult with a qualified financial advisor before making investment decisions.")

stock_ticker = st.text_input("Enter a stock's ticker symbol, ex : AAPL")
start_date = st.date_input("Enter the start date:",
                           value=one_year_before)
end_date = st.date_input("Enter the end date:", value=today)
ticker_list = []

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Analytics", "Metrics", "Key Metrics", "Charts", "Summary"])

with tab1:
    if st.button("Analyze Information!"):
        ticker_list = [t.strip().upper()
                       for t in stock_ticker.split(",") if t.strip()]
    if not ticker_list:
        st.warning("Please enter a ticker symbol!")
    else:
        with st.spinner("Downloading data from Yahoo FInance!"):

            df = data_fetching(ticker_list, start_date, end_date)

        if df is not None and not df.empty:
            st.success("Data Fetched Successfully")
            st.balloons()
            st.write("### Price results ", df.head())

            st.divider()
            st.title(f"Line Chart for {ticker_list}")
            with st.expander("View Raw Data"):
                st.write(df)

with tab2:
    if st.button("Analyze Metrics!"):
        ticker_list = [t.strip().upper()
                       for t in stock_ticker.split(",") if t.strip()]
        if not ticker_list:
            st.warning("Please enter a ticker symbol!")
        else:
            with st.spinner("Downloading data from Yahoo FInance!"):

                df = data_fetching(ticker_list, start_date, end_date)

            if df is not None and not df.empty:
                latest_price = df["Close"].iloc[-1]
                starting_price = df["Close"].iloc[0]
                price_change = latest_price - starting_price
                percentage_change = (price_change / starting_price) * 100

                if "Close" in df.columns:
                    close_price = df["Close"]

                    if isinstance(close_price, pd.DataFrame):
                        close_price = close_price.iloc[:, 0]

                else:
                    st.error("'Close' column not found in data")
                    st.stop()

                metrics_df = pd.DataFrame(index=close_price.index)
                metrics_df["Close Price"] = close_price
                metrics_df["Previous Close"] = close_price.shift(1)
                metrics_df["Price Change"] = close_price.diff()
                metrics_df["Percentage Change"] = close_price.pct_change() * \
                    100

                metrics_df = metrics_df.dropna().round(2)
                metrics_df.round(2)

                st.dataframe(metrics_df)


with tab3:
    ticker_list = []
    df = None

    if st.button("Analyze Key Metrics!"):
        ticker_list = [t.strip().upper()
                       for t in stock_ticker.split(",") if t.strip()]
    if not ticker_list:
        st.warning("Please enter a ticker symbol!")
    else:
        with st.spinner("Downloading data from Yahoo FInance!"):

            df = data_fetching(ticker_list, start_date, end_date)

    if df is not None and not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        if "Close" in df.columns:
            close_price = df["Close"]

            if isinstance(close_price, pd.DataFrame):
                close_price = close_price.iloc[:, 0]

        else:
            st.error("'Close' column not found in data")
            st.stop()

        key_metrics_df = pd.DataFrame(index=close_price.index)

        with col1:
            st.markdown("#### Current Price")
            st.table(df.iloc[:25, 3])

        with col2:
            st.markdown("#### % Change")
            df["Daily Return Percentage"] = df["Close"].pct_change() * 100
            st.table(df["Daily Return Percentage"].iloc[:25])

        with col3:

            st.markdown("#### 52-Week High")
            week_52_high = close_price.rolling(window=249, min_periods=1).max()
            key_metrics_df["52-Week High"] = week_52_high
            st.table(key_metrics_df["52-Week High"].iloc[:25])

        with col4:

            st.markdown("#### 52-Week Low")
            week_52_low = close_price.rolling(window=249, min_periods=1).min()
            key_metrics_df["52-Week Low"] = week_52_low
            st.table(key_metrics_df["52-Week Low"].iloc[:25])

with tab4:
    if st.button("Analyze Charts!"):
        ticker_list = [t.strip().upper()
                       for t in stock_ticker.split(",") if t.strip()]
        if not ticker_list:
            st.warning("Please enter a ticker symbol!")
        else:
            with st.spinner("Downloading data from Yahoo FInance!"):

                df = data_fetching(ticker_list, start_date, end_date)

            if df is not None and not df.empty:
                st.subheader(f"Price History for {ticker_list}")

                if "Close" in df.columns:
                    close_price = df["Close"]

                    if isinstance(close_price, pd.DataFrame):
                        close_price = close_price.iloc[:, 0]

                fig, ax = plt.subplots()

                for ticker in ticker_list:
                    stock = yf.Ticker(ticker)
                    hist_full = stock.history(period="100d")
                    hist_full.index = pd.to_datetime(hist_full.index)
                    open_price = hist_full["Open"]
                    close_price = hist_full["Close"]

                    moving_average = open_price.rolling(window=50).mean()

                    hist = hist_full.tail(50)
                    moving_average = moving_average.tail(50)

                    ax.plot(hist.index,
                            hist["Open"], label="Open Price")
                    ax.plot(hist.index, hist["Close"], label="Close Price")
                    ax.plot(hist.index, moving_average,
                            label="50-Day Moving Average")

                ax.set_title("Price History")
                ax.set_xlabel("Time")
                ax.set_ylabel("Price")
                ax.legend(title="Legend", loc="lower right",
                          frameon=True, fontsize=10)
                ax.grid(True)
                plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

                st.pyplot(fig)

                plt.close()

                st.subheader(f"Volume Chart for {ticker_list}")

                fig, ax = plt.subplots()
                max_vol = 0

                for ticker in ticker_list:
                    stock = yf.Ticker(ticker)
                    volume = df["Volume"]
                    hist_full = stock.history(period="100d")
                    max_vol = max(max_vol, hist["Volume"].max())

                    hist = hist_full.tail(50)
                    volume = volume.tail(50)

                    ax.bar(hist.index, hist["Volume"],
                           label=f"{ticker} Volume")

                ax.set_title(f"Bar Graph for Volume of {ticker}")
                ax.legend(title="Legend", loc="lower right",
                          frameon=True, fontsize=10)
                ax.grid(True)
                ax.set_xlabel("Date")
                ax.set_ylabel("Volume")

                if max_vol >= 1e9:
                    scale = 1e9
                    suffix = "B"
                elif max_vol >= 1e6:
                    scale = 1e6
                    suffix = "M"
                elif max_vol >= 1e3:
                    scale = 1e3
                    suffix = "K"
                else:
                    scale = 1
                    suffix = ""

                tick_interval = max_vol / 5
                ticks = [i for i in range(
                    0, int(max_vol)+1, int(tick_interval))]

                ax.set_yticks(ticks)
                ax.set_yticklabels([f"{int(t/scale)}{suffix}" for t in ticks])

                plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

                st.pyplot(fig)

                plt.close()

with tab5:
    if st.button("Analyze Summary!"):
        ticker_list = [t.strip().upper()
                       for t in stock_ticker.split(",") if t.strip()]
        if not ticker_list:
            st.warning("Please enter a ticker symbol!")
        else:
            with st.spinner("Downloading data from Yahoo FInance!"):

                df = data_fetching(ticker_list, start_date, end_date)

            if df is not None and not df.empty:
                st.subheader(f"Summary for {ticker_list}")

                col1, col2, = st.columns(2)

                with col1:
                    ticker = ticker_list[0]
                    hist = yf.Ticker(ticker).history(period="100d")

                    prices = np.vstack([hist["Open"].values,
                                        hist["High"].values,
                                        hist["Low"].values,
                                        hist["Close"].values])

                    X, Y = np.meshgrid(
                        np.arange(prices.shape[1]), np.arange(prices.shape[0]))

                    fig = go.Figure(
                        data=[go.Surface(z=prices, x=X, y=Y, colorscale='Spectral')])

                    fig.update_layout(
                        scene=dict(
                            xaxis_title='Time (Days)',
                            yaxis_title='Price Type (O,H,L,C)',
                            yaxis=dict(tickvals=[0, 1, 2, 3], ticktext=[
                                       "Open", "High", "Low", "Close"]),
                            zaxis_title='Price',
                            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
                        ),
                        width=1000,
                        height=700,
                        margin=dict(l=50, r=50, t=100, b=50)
                    )

                    st.plotly_chart(fig, use_container_width=True)
