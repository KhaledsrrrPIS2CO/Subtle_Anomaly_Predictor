import os
import yfinance as yf
from sqlalchemy import text
from sqlalchemy import create_engine, MetaData, func


os.environ['DB_USER'] = 'root'
os.environ['DB_PASSWORD'] = '2020$2020$ABC'


def fetch_and_insert_spy_data(start_date: object, end_date: object) -> object:
    # Fetch the daily OHLC data for SPY
    spy = yf.Ticker("SPY")
    data = spy.history(start=start_date, end=end_date)

    # Keep only the OHLC columns and add a date column
    ohlc_data = data[['Open', 'High', 'Low', 'Close']].reset_index()
    ohlc_data.rename(columns={'index': 'Date'}, inplace=True)
    ohlc_data['Date'] = ohlc_data['Date'].dt.tz_localize(None)

    # Get database credentials from environment variables
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']

    # Establish a database connection using the environment variables
    engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@localhost/spy_ohlc')

    # Check if the connection is successful
    try:
        with engine.connect() as connection:
            print("Connection to the database is successful! Ready to insert the data.")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

    # Connect to the engine
    with engine.connect() as connection:
        # Start a transaction
        trans = connection.begin()

        # Insert each row of data into the price_data table of spy_ohlc SQL database
        try:
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

                connection.execute(text(query))

            # Commit the transaction
            trans.commit()
        except Exception as e:
            print(f"Error inserting data: {e}")
            # Rollback the transaction in case of an error
            trans.rollback()

    # Close the database connection
    engine.dispose()


def check_database_by_fetch_and_print_data():
    # Get database credentials from environment variables
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']

    # Establish a database connection using the environment variables
    engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@localhost/spy_ohlc')

    # Connect to the engine
    with engine.connect() as connection:
        # Fetch table metadata
        try:
            metadata = MetaData()
            metadata.reflect(bind=engine)
            table = metadata.tables['price_data']
            query = table.select().with_only_columns(func.count()).select_from(table)
            num_rows = connection.execute(query).scalar()
            columns = [column.name for column in table.columns]
            print(f"\nTable name: {table.name}\nNumber of rows: {num_rows}\nColumns: {columns}")

            # Fetch a sample of data from the price_data table
            query = text("SELECT * FROM price_data ORDER BY date DESC LIMIT 5")
            results = connection.execute(query).fetchall()
            print("\nSample data from the price_data table:")

            for row in results:
                print(row)

        except Exception as e:
            print(f"Error fetching data: {e}")

    # Close the database connection
    engine.dispose()


def main_data_collection():
    fetch_and_insert_spy_data("2023-01-01", "2023-04-26")
    check_database_by_fetch_and_print_data()

if __name__ == "__main__":
    main_data_collection()