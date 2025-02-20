import logging
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from data_analyzer import DataAnalyzer

class ModelTrainer:
    def __init__(self, model_file="ml/trading_model.pkl"):
        """
        Initializes the Model Trainer.

        :param model_file: Path to save the trained model.
        """
        self.model_file = model_file
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.data_analyzer = DataAnalyzer()

        # Setup logging
        logging.basicConfig(
            filename="logs/model_training.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def preprocess_data(self, df):
        """
        Prepares historical data for training.

        :param df: Pandas DataFrame with market data.
        :return: Processed feature set and labels.
        """
        df["SMA_10"] = self.data_analyzer.calculate_moving_average(df, period=10)
        df["SMA_50"] = self.data_analyzer.calculate_moving_average(df, period=50)
        df["RSI"] = self.data_analyzer.calculate_rsi(df, period=14)
        df["Volatility"] = self.data_analyzer.analyze_volatility(df, period=10)

        df.dropna(inplace=True)  # Remove missing values

        df["Target"] = np.where(df["Close"].shift(-1) > df["Close"], 1, 0)  # Binary: 1 = Buy, 0 = Sell
        features = ["SMA_10", "SMA_50", "RSI", "Volatility"]
        
        logging.info("Data preprocessed for training with %d samples.", len(df))
        return df[features], df["Target"]

    def train_model(self, df):
        """
        Trains the machine learning model.

        :param df: Pandas DataFrame with historical data.
        """
        X, y = self.preprocess_data(df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        logging.info("Model trained with accuracy: %.2f%%", accuracy * 100)
        print("Model Accuracy:", accuracy)
        print("Classification Report:\n", classification_report(y_test, predictions))

        joblib.dump(self.model, self.model_file)
        logging.info("Trained model saved to %s", self.model_file)

    def load_model(self):
        """ Loads the trained model if available. """
        try:
            self.model = joblib.load(self.model_file)
            logging.info("Model loaded successfully from %s", self.model_file)
        except FileNotFoundError:
            logging.warning("No trained model found. Train a model first.")

    def predict_trade_signal(self, df):
        """
        Predicts buy/sell signals using the trained model.

        :param df: Pandas DataFrame with market data.
        :return: Prediction (1 = Buy, 0 = Sell).
        """
        self.load_model()
        features, _ = self.preprocess_data(df)
        return self.model.predict(features)

# Example Usage
if __name__ == "__main__":
    # Mock historical data
    data = pd.DataFrame({
        "Open": [2100, 2105, 2110, 2103, 2098, 2115, 2120, 2110, 2100, 2095],
        "Close": [2105, 2110, 2103, 2098, 2102, 2125, 2130, 2115, 2105, 2098]
    })

    trainer = ModelTrainer()
    trainer.train_model(data)

    predictions = trainer.predict_trade_signal(data)
    print("Trade Predictions:", predictions)
