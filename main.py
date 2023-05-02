# main.py

from one_data_collection_and_heikin_conversion import main_data_collection_and_heikin_conversion
from two_features_engineering import main_features_engineering


def main():
    """
    The main function runs the data collection, Heikin-Ashi conversion, and features engineering.
    It calls the respective main functions from the imported modules.
    """

    # Call main_data_collection_and_heikin_conversion with the specified parameters.
    # ticker: The stock symbol for which data will be collected and converted to Heikin-Ashi format.
    # start_date: The start date for the data collection.
    # end_date: The end date for the data collection.
    # initial_ha_open, initial_ha_high, initial_ha_low, initial_ha_close: Initial Heikin-Ashi candlestick
    # values of the first day which must be added to the Heikin ashi database.
    main_data_collection_and_heikin_conversion(ticker="MSFT",
                                               start_date='2020-01-01',
                                               end_date='2023-04-29',
                                               initial_ha_open=158.21,
                                               initial_ha_high=158.21,
                                               initial_ha_low=156.45,
                                               initial_ha_close=157.17)

    # Call main_features_engineering with the specified parameters.
    # start_date: The start date for the features engineering process.
    # end_date: The end date for the features engineering process.
    # min_diff, max_diff as stop loss: The range of differences between consecutive
    # Heikin-Ashi candlesticks to filter data.
    main_features_engineering(start_date='2020-01-01',
                              end_date='2024-01-01',
                              min_diff=0.0,
                              max_diff=0.21)


if __name__ == "__main__":
    main()

# MSFT first Heikin Ashi data O 158.21 H 158.21 L 156.45 C 157.17
# (ticker="MSFT",
#                                                start_date='2020-01-01',
#                                                end_date='2023-04-29',
#                                                initial_ha_open=158.21,
#                                                initial_ha_high=158.21,
#                                                initial_ha_low=156.45,
#                                                initial_ha_close=157.17)


# # TSLA
# (ticker="TSLA",
#                                                start_date='2020-01-01',
#                                                end_date='2023-04-29',
#                                                initial_ha_open=28.24,
#                                                initial_ha_high=28.24,
#                                                initial_ha_low=26.81,
#                                                initial_ha_close=27.44)

