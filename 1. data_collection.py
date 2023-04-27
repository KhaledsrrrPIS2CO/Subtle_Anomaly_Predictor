import os
import requests
import pandas as pd
from sqlalchemy import create_engine
import yfinance as yf
from datetime import datetime
from sqlalchemy import text

os.environ['DB_USER'] = 'root'
os.environ['DB_PASSWORD'] = '2020$2020$ABC'


def fetch_and_insert_spy_data(start_date: object, end_date: object) -> object:
    # Fetch the daily OHLC data for SPY
    spy = yf.Ticker("SPY")
    data = spy.history(start=start_date, end=end_date)

    # Keep only the OHLC columns and add a date column
    ohlc_data = data[['Open', 'High', 'Low', 'Close']].reset_index()
    ohlc_data.rename(columns={'index': 'Date'}, inplace=True)

    # Get database credentials from environment variables
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']

    # Establish a database connection using the environment variables
    engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@localhost/spy_ohlc')

    # Check if the connection is successful
    try:
        with engine.connect() as connection:
            print("Connection to the database is successful!")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

    # Connect to the engine
    with engine.connect() as connection:
        # Insert each row of data into the price_data table of spy_ohlc SQL database
        for index, row in ohlc_data.iterrows():
            query = f"""
                   INSERT INTO price_data (
                       date,
                       open_price,
                       high_price,
                       low_price,
                       close_price
                   )
                   VALUES (
                       '{row['Date'].strftime('%Y-%m-%d %H:%M:%S')}',
                       {row['Open']},
                       {row['High']},
                       {row['Low']},
                       {row['Close']}
                   )
               """

            try:
                connection.execute(text(query))
            except Exception as e:
                print(f"Error inserting row {index}: {e}")

    # Close the database connection
    engine.dispose()


fetch_and_insert_spy_data("2023-01-01", "2023-04-26")
