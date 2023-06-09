import os
import yfinance as yf
from sqlalchemy import create_engine, text
import pandas as pd
import mysql.connector


def fetch_price_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)
    return data.round(2)


def store_normal_price_data_to_database(price_data, db_user, db_password):
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']

    # Create a connection to the MySQL database
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@localhost/spy_ohlc')

    try:
        # Check if the connection is successful
        connection = engine.connect()
        print("Connected to the database for insertion!")
    except Exception as e:
        print("Error connecting to the database:", e)
        return

    # Iterate through the DataFrame rows and insert the data into the 'spy_normal_price_data' table
    for index, row in price_data.iterrows():
        date = index.date()
        open_price = row['Open']
        high_price = row['High']
        low_price = row['Low']
        close_price = row['Close']
        adj_close = row['Adj Close']
        volume = row['Volume']

        query = text(f"""
        INSERT IGNORE INTO spy_normal_price_data (Date, Open, High, Low, Close, `Adj Close`, Volume)
        VALUES ('{date}', {open_price}, {high_price}, {low_price}, {close_price}, {adj_close}, {volume});
        """)

        try:
            # Execute the query and commit the transaction
            connection.execute(query)
            connection.execute(text("COMMIT;"))
        except Exception as e:
            print(f"Error inserting data for {date}:", e)
            connection.execute(text("ROLLBACK;"))
            continue

    # Close the database connection
    connection.close()
    print("Data insertion complete and connection closed!\n")


def get_spy_normal_price_data_table_details(db_user, db_password):
    # Create a connection to the MySQL database
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@localhost/spy_ohlc')

    try:
        # Check if the connection is successful
        connection = engine.connect()
        print("Connected to the database for verification!")
    except Exception as e:
        print("Error connecting to the database:", e)
        return

    # Fetch the first 5 rows from the table
    query = text("SELECT * FROM spy_normal_price_data LIMIT 5;")
    result = connection.execute(query)
    print("First 5 rows of the table:")
    for row in result:
        print(row)

    # Get the table dimensions
    query = text("SELECT COUNT(*) FROM spy_normal_price_data;")
    row_count = connection.execute(query).scalar()
    print(f"Table dimensions: {row_count} rows x 7 columns")

    # Close the database connection
    connection.close()
    print("Verification completed. Connection closed!\n")


def calculate_heikin_ashi(db_user, db_password, initial_ha_open, initial_ha_high, initial_ha_low, initial_ha_close):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=db_user,
            password=db_password,
            database='spy_ohlc'
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return

    query = "SELECT * FROM spy_normal_price_data;"
    result = connection.cursor()
    result.execute(query)

    data = [dict(zip([column[0] for column in result.description], row)) for row in result.fetchall()]
    normal_prices_df = pd.DataFrame(data)
    normal_prices_df.set_index(pd.to_datetime(normal_prices_df['Date']), inplace=True)

    heikin_ashi_prices_df = pd.DataFrame(index=normal_prices_df.index,
                                         columns=['HA_Open', 'HA_High', 'HA_Low', 'HA_Close'])

    heikin_ashi_prices_df.loc[pd.Timestamp('2019-12-31')] = {
        'HA_Open': initial_ha_open,
        'HA_High': initial_ha_high,
        'HA_Low': initial_ha_low,
        'HA_Close': initial_ha_close
    }

    for index, row in normal_prices_df.iloc[1:].iterrows():
        open_price, high_price, low_price, close_price = row['Open'], row['High'], row['Low'], row['Close']

        previous_date = heikin_ashi_prices_df.index.get_loc(index) - 1
        previous_date = heikin_ashi_prices_df.index[previous_date]

        previous_row = heikin_ashi_prices_df.loc[previous_date]

        previous_ha_open, previous_ha_high, previous_ha_low, previous_ha_close = \
            previous_row['HA_Open'], previous_row['HA_High'], previous_row['HA_Low'], previous_row['HA_Close']

        ha_open = (float(previous_ha_open) + float(previous_ha_close)) / 2
        ha_high = max(float(high_price), ha_open, float(close_price))
        ha_low = min(float(low_price), ha_open, float(close_price))
        ha_close = (open_price + high_price + low_price + close_price) / 4

        heikin_ashi_prices_df.loc[index] = {
            'HA_Open': ha_open,
            'HA_High': ha_high,
            'HA_Low': ha_low,
            'HA_Close': ha_close
        }

    heikin_ashi_prices_df.sort_index(inplace=True)
    connection.close()

    return heikin_ashi_prices_df


def store_heikin_ashi_data(heikin_ashi_prices_df, db_user, db_password):
    print("Connecting to the database...")
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=db_user,
            password=db_password,
            database='spy_ohlc'
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return

    print("Connected to the database successfully.")
    cursor = connection.cursor()

    for index, row in heikin_ashi_prices_df.iterrows():
        date = index.strftime('%Y-%m-%d')
        ha_open, ha_high, ha_low, ha_close = ('NULL' if pd.isna(val) else val for val in
                                              (row['HA_Open'], row['HA_High'], row['HA_Low'], row['HA_Close']))

        query = f"INSERT INTO spy_heikin_ashi_price_data (Date, Open, High, Low, Close) " \
                f"VALUES ('{date}', {ha_open}, {ha_high}, {ha_low}, {ha_close}) " \
                f"ON DUPLICATE KEY UPDATE Open = {ha_open}, High = {ha_high}, Low = {ha_low}, Close = {ha_close};"

        cursor.execute(query)

    print("Heikin-Ashi prices stored successfully. Committing changes to the database.")
    connection.commit()
    cursor.close()
    connection.close()
    print("Database connection closed.")


def main_data_collection_and_heikin_conversion(ticker, start_date, end_date,
                                               initial_ha_open, initial_ha_high, initial_ha_low, initial_ha_close):
    # Define the ticker symbol and the time range for the data
    ticker = ticker
    start_date = start_date
    end_date = end_date
    initial_ha_open = initial_ha_open
    initial_ha_high = initial_ha_high
    initial_ha_low = initial_ha_low
    initial_ha_close = initial_ha_close

    # Call the function to fetch the data
    spy_price_data = fetch_price_data(ticker, start_date, end_date)

    # Set the environment variables
    db_user = os.environ['DB_USER'] = 'root'
    db_password = os.environ['DB_PASSWORD'] = '2020$2020$ABC'

    # Call the function to store the data in the database
    store_normal_price_data_to_database(spy_price_data, db_user, db_password)

    # Call the function to get table details
    get_spy_normal_price_data_table_details(db_user, db_password)

    # Call the calculate_heikin_ashi function
    ha_prices = calculate_heikin_ashi(db_user, db_password,
                                      initial_ha_open, initial_ha_high, initial_ha_low, initial_ha_close)

    print(ha_prices)

    # Call the store_heikin_ashi_data function
    store_heikin_ashi_data(ha_prices, db_user, db_password)


# Call the main_data_collection function
if __name__ == "__main__":
    main_data_collection_and_heikin_conversion()
