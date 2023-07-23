import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

COMPANIES = {
    "Apple Inc.": "AAPL",
    "Microsoft Corporation": "MSFT",
    "Amazon.com Inc.": "AMZN",
    "Alphabet Inc. (Google)": "GOOGL",
    "Facebook Inc.": "FB",
    "Tesla Inc.": "TSLA",
    "Netflix Inc.": "NFLX",
    "NVIDIA Corporation": "NVDA",
    "The Walt Disney Company": "DIS",
    "Coca-Cola Company": "KO"
}

def get_stock_data(symbol, start_date, end_date):
    df = yf.download(symbol, start=start_date, end=end_date)
    return df

def calculate_one_month_prediction(df):
    # Calculate the exponential moving average (EMA) with a span of 20 days
    ema = df['Close'].ewm(span=20, adjust=False).mean()

    # Extrapolate the EMA for the next 30 days to make predictions
    last_ema = ema[-1]
    daily_return = df['Close'].pct_change().mean()
    one_month_prediction = last_ema * (1 + daily_return) ** 30

    return one_month_prediction

def main():
    st.title('Stock Tracker - Last Two Months History and One-Month Prediction')
    stock_symbol = st.selectbox('Select a company:', list(COMPANIES.keys()))

    if stock_symbol:
        symbol = COMPANIES[stock_symbol]

        # Get the date range for the last two months
        end_date = datetime.now()
        start_date = end_date - timedelta(days=60)

        df = get_stock_data(symbol, start_date, end_date)

        if not df.empty:
            st.write(f"**Last Two Months History for {stock_symbol} ({symbol})**")
            st.line_chart(df['Close'])

            # Calculate one-month prediction
            prediction = calculate_one_month_prediction(df)
            st.write(f"**One-Month Price Prediction:** {prediction:.2f}")

            # Create a dataframe for the prediction line
            prediction_date = df.index[-1] + timedelta(days=1)
            prediction_df = pd.DataFrame(index=pd.date_range(start=prediction_date, periods=30, freq='D'),
                                         data=prediction, columns=['Prediction'])

            # Concatenate historical data and prediction dataframes
            full_df = pd.concat([df['Close'], prediction_df])

            # Plot the line chart with historical data and prediction
            st.write(f"**Historical Data with One-Month Prediction for {stock_symbol} ({symbol})**")
            st.line_chart(full_df)

if __name__ == "__main__":
    main()
