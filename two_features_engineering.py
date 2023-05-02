import os
import pandas as pd
from sqlalchemy import create_engine


def fetch_heikin_ashi_data(db_user, db_password, start_date, end_date):
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@localhost/spy_ohlc')

    try:
        connection = engine.connect()
        print("Connected to the database!")
    except Exception as e:
        print("Error connecting to the database:", e)
        return

    query = f"SELECT * FROM spy_heikin_ashi_price_data WHERE Date >= '{start_date}' AND Date <= '{end_date}';"
    heikin_ashi_data = pd.read_sql_query(query, connection)

    connection.close()
    print("Connection closed!\n")

    return heikin_ashi_data


def open_high_difference_stats_go_short(db_user, db_password, start_date, end_date, min_diff, max_diff):
    ohlc_data = fetch_heikin_ashi_data(db_user, db_password, start_date, end_date)
    total_days = len(ohlc_data)
    filtered_days = []
    signal_dates = []  # Add this line to store the signal dates

    for index, row in ohlc_data.iterrows():
        open_price, high_price, date = row['Open'], row['High'], row['Date']
        difference = high_price - open_price

        if min_diff < difference < max_diff:
            filtered_days.append(difference)
            signal_dates.append(date)  # Add this line to store the date for each signal

    signal_count = len(filtered_days)
    percentage = (signal_count / total_days) * 100 if total_days > 0 else 0

    if signal_count > 0:
        average_diff = sum(filtered_days) / signal_count
        std_dev = pd.Series(filtered_days).std()
        min_diff_observed = min(filtered_days)
        max_diff_observed = max(filtered_days)
        median_diff = pd.Series(filtered_days).median()
    else:
        average_diff = None
        std_dev = None
        min_diff_observed = None
        max_diff_observed = None
        median_diff = None

    stats = {
        'total_days': total_days,
        'signal_count': signal_count,
        'percentage': percentage,
        'average_diff': average_diff,
        'std_dev': std_dev,
        'min_diff_observed': min_diff_observed,
        'max_diff_observed': max_diff_observed,
        'median_diff': median_diff,
        'signal_dates': signal_dates,  # Add this line

    }

    return stats


def print_stats_open_high_difference_go_short(stats):
    print("Open-High Difference Statistics (Go Short):")
    print(f"  Total trading days: {stats['total_days']}")
    print(f"  Signal days: {stats['signal_count']}")
    print(f"  Percentage of total days: {stats['percentage']:.2f}%")
    print(f"  Average difference: {stats['average_diff']:.4f}"
          if stats['average_diff'] is not None else "  Average difference: N/A")
    print(f"  Standard deviation: {stats['std_dev']:.4f}"
          if stats['std_dev'] is not None else "  Standard deviation: N/A")
    print(f"  Minimum difference observed: {stats['min_diff_observed']:.4f}"
          if stats['min_diff_observed'] is not None else "  Minimum difference observed: N/A")
    print(f"  Maximum difference observed: {stats['max_diff_observed']:.4f}"
          if stats['max_diff_observed'] is not None else "  Maximum difference observed: N/A")
    print(f"  Median difference: {stats['median_diff']:.4f}"
          if stats['median_diff'] is not None else "  Median difference: N/A")
    print("  Signal dates:")
    for date in stats['signal_dates']:
        print(f"    {date}")


def open_low_difference_stats_go_long(db_user, db_password, start_date, end_date, min_diff, max_diff):
    ohlc_data = fetch_heikin_ashi_data(db_user, db_password, start_date, end_date)
    total_days = len(ohlc_data)
    filtered_days = []
    signal_dates = []

    for index, row in ohlc_data.iterrows():
        open_price, low_price, date = row['Open'], row['Low'], row['Date']
        difference = open_price - low_price

        if min_diff < difference < max_diff:
            filtered_days.append(difference)
            signal_dates.append(date)

    signal_count = len(filtered_days)
    percentage = (signal_count / total_days) * 100 if total_days > 0 else 0

    if signal_count > 0:
        average_diff = sum(filtered_days) / signal_count
        std_dev = pd.Series(filtered_days).std()
        min_diff_observed = min(filtered_days)
        max_diff_observed = max(filtered_days)
        median_diff = pd.Series(filtered_days).median()
    else:
        average_diff = None
        std_dev = None
        min_diff_observed = None
        max_diff_observed = None
        median_diff = None

    stats = {
        'total_days': total_days,
        'signal_count': signal_count,
        'percentage': percentage,
        'average_diff': average_diff,
        'std_dev': std_dev,
        'min_diff_observed': min_diff_observed,
        'max_diff_observed': max_diff_observed,
        'median_diff': median_diff,
        'signal_dates': signal_dates,

    }

    return stats


def print_stats_open_low_difference_go_long(stats):
    print("Open-Low Difference Statistics (GO Long):")
    print(f"  Total trading days: {stats['total_days']}")
    print(f"  Signal days: {stats['signal_count']}")
    print(f"  Percentage of total days: {stats['percentage']:.2f}%")
    print(f"  Average difference: {stats['average_diff']:.4f}"
          if stats['average_diff'] is not None else "  Average difference: N/A")
    print(f"  Standard deviation: {stats['std_dev']:.4f}"
          if stats['std_dev'] is not None else "  Standard deviation: N/A")
    print(f"  Minimum difference observed: {stats['min_diff_observed']:.4f}"
          if stats['min_diff_observed'] is not None else "  Minimum difference observed: N/A")
    print(f"  Maximum difference observed: {stats['max_diff_observed']:.4f}"
          if stats['max_diff_observed'] is not None else "  Maximum difference observed: N/A")
    print(f"  Median difference: {stats['median_diff']:.4f}"
          if stats['median_diff'] is not None else "  Median difference: N/A")
    print("  Signal dates:")
    for date in stats['signal_dates']:
        print(f"    {date}")


def main_features_engineering(start_date, end_date, min_diff, max_diff):
    # Call the fetch_heikin_ashi_data function
    db_user = os.environ['DB_USER'] = 'root'
    db_password = os.environ['DB_PASSWORD'] = '2020$2020$ABC'

    # parameters
    start_date = start_date
    end_date = end_date
    min_diff = min_diff
    max_diff = max_diff

    # GO Short
    # Call the open_high_difference_stats_go_short function
    data_open_high_difference_stats_go_short = open_high_difference_stats_go_short(
        db_user, db_password, start_date, end_date, min_diff, max_diff)
    # Call the print_stats_open_high_difference_go_short function
    print_stats_open_high_difference_go_short(data_open_high_difference_stats_go_short)

    # GO Long
    # Call the data_open_low_difference_stats_go_long function
    data_open_low_difference_stats_go_long = open_low_difference_stats_go_long(
        db_user, db_password, start_date, end_date, min_diff, max_diff)
    # Call the print_stats_open_low_difference_go_long function

    print_stats_open_low_difference_go_long(data_open_low_difference_stats_go_long)


if __name__ == "__main__":
    main_features_engineering()
