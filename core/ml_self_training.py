# core/ml_self_training.py

import logging
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from market_data import MarketData


class MLSelfTrainer:
    """ Self-training AI model for continuous learning in trading strategies """

    def __init__(self, config):
        """
        Initializes the self-training module.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.model = None
        self.market_data = MarketData(config)
        self.training_interval = config["settings"]["ml_training"].get("training_interval", 30)  # in minutes
        self.model_performance_threshold = config["settings"]["ml_training"].get("performance_threshold", 0.75)
        self.retraining_needed = False

        # Initialize logger
        logging.basicConfig(
            filename="logs/ml_self_training.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
    
    def check_retraining_need(self):
        """
        Check whether the model needs retraining based on performance.
        :return: True if retraining is needed, False otherwise.
        """
        if self.retraining_needed:
            logging.info("Model retraining required based on performance threshold.")
            return True

        # Simulate performance check (can be replaced with actual performance evaluation logic)
        current_performance = self.evaluate_model_performance()

        if current_performance < self.model_performance_threshold:
            logging.info(f"Model performance below threshold: {current_performance}. Retraining triggered.")
            self.retraining_needed = True
            return True
        return False
    
    def evaluate_model_performance(self):
        """
        Evaluate the model's performance on the latest data.
        This function could compare the model's predictions with actual market data.
        :return: Model accuracy score (as an example).
        """
        data = self.market_data.get_historical_data()
        features, labels = self.preprocess_data(data)

        if self.model is not None:
            predictions = self.model.predict(features)
            accuracy = accuracy_score(labels, predictions)
            logging.info(f"Model accuracy: {accuracy:.2f}")
            return accuracy
        else:
            logging.warning("Model not yet trained, skipping evaluation.")
            return 0.0

    def preprocess_data(self, data):
        """
        Preprocess the data for model training.
        :param data: Raw market data
        :return: Processed features and labels.
        """
        features = data.drop(columns=["target"])
        labels = data["target"]

        # Normalize or scale features if necessary (optional)
        # For example: features = self.scale_features(features)
        return features, labels

    def train_model(self):
        """
        Train or retrain the model using the latest market data.
        The model can be a simple supervised classifier or more complex models (e.g., RL models).
        """
        logging.info("Retraining AI model...")

        # Fetch latest market data for training
        data = self.market_data.get_historical_data()

        # Preprocess data for training
        features, labels = self.preprocess_data(data)

        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

        # Initialize the model (Random Forest Classifier as an example)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

        # Hyperparameter tuning (optional)
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, None],
            'min_samples_split': [2, 5, 10]
        }

        grid_search = GridSearchCV(self.model, param_grid, cv=5)
        grid_search.fit(X_train, y_train)

        # Use the best estimator
        self.model = grid_search.best_estimator_

        # Evaluate performance
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        logging.info(f"Model retrained with accuracy: {accuracy:.2f}")

        # If performance is below the threshold, set retraining flag
        if accuracy < self.model_performance_threshold:
            logging.warning("Model retraining did not meet performance criteria.")
            self.retraining_needed = True
        else:
            self.retraining_needed = False

        # Save the model (optional, for persistent use)
        self.save_model()

    def save_model(self):
        """
        Save the trained model to disk for future use.
        """
        from joblib import dump
        dump(self.model, "models/trading_model.joblib")
        logging.info("Model saved successfully.")
    
    def load_model(self):
        """
        Load a pre-trained model from disk.
        """
        from joblib import load
        try:
            self.model = load("models/trading_model.joblib")
            logging.info("Model loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading model: {str(e)}")
            self.model = None
