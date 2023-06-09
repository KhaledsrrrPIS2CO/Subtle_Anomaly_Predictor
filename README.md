# Subtle Anomaly Predictor

Subtle Anomaly Predictor is a Python-based project that uses machine learning algorithms to predict anomalies in time-series data. The project includes two main modules, data collection, and feature engineering.

The data collection module collects time-series data for a specified ticker from Yahoo Finance and stores it in a MySQL database. The module then applies the Heikin-Ashi candlestick charting technique to the data, which is a popular way of filtering out noise in financial data.

The feature engineering module processes the data generated by the data collection module and creates features for machine learning models. The module creates features such as rolling averages, moving standard deviations, and rolling correlations to identify patterns and anomalies in the data.

Subtle Anomaly Predictor is a powerful tool for anyone interested in predicting subtle anomalies in time-series data. The project is designed to be easy to use, with simple command-line interfaces for both modules.

## Getting Started

To get started with Subtle Anomaly Predictor, you will need to install Python 3 and MySQL. You can then clone the repository and install the required dependencies by running the following commands:

```
$ git clone https://github.com/your_username/Subtle_Anomaly_Predictor.git
$ cd Subtle_Anomaly_Predictor
$ pip install -r requirements.txt
```

## Usage

To use Subtle Anomaly Predictor, simply run the `main.py` script in the project's root directory. This script will call the data collection and feature engineering modules and generate predictions for anomalies in the data.

You can customize the project by changing the parameters in the `main.py` script, such as the start and end dates for data collection and the initial values for the Heikin-Ashi candlestick charting technique.

## Contributing

If you would like to contribute to Subtle Anomaly Predictor, feel free to submit a pull request or open an issue on the project's GitHub page. We welcome contributions from developers of all skill levels, and we are happy to help you get started with the project.

## License

Subtle Anomaly Predictor is licensed under the MIT License. See the `LICENSE` file for more information.
