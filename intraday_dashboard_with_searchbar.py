
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# Title
st.title("NSE Intraday Support/Resistance Dashboard")

# Load stock list (Fallback list for demo)
stock_list = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "ICICIBANK.NS", "HDFCBANK.NS",
    "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "AXISBANK.NS", "BPCL.NS"
]

# Search bar
search_query = st.text_input("Search for a stock:", "")
filtered_stocks = [s for s in stock_list if search_query.upper() in s.upper()]

selected_stock = st.selectbox("Select Stock", filtered_stocks if filtered_stocks else stock_list)

# Fetch data
data = yf.download(selected_stock, period="5d", interval="15m")
if data.empty:
    st.error("No data found for the selected stock.")
else:
    # Calculate support and resistance using recent lows and highs
    support = data["Low"].rolling(window=20).min().iloc[-1]
    resistance = data["High"].rolling(window=20).max().iloc[-1]

    st.markdown(f"**Support Level:** {support:.2f}")
    st.markdown(f"**Resistance Level:** {resistance:.2f}")

    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data.index, open=data['Open'], high=data['High'],
        low=data['Low'], close=data['Close'], name='Price'
    ))
    fig.add_hline(y=support, line_color="green", line_dash="dot", annotation_text="Support")
    fig.add_hline(y=resistance, line_color="red", line_dash="dot", annotation_text="Resistance")
    fig.update_layout(title=selected_stock, xaxis_title="Time", yaxis_title="Price")
    st.plotly_chart(fig)
