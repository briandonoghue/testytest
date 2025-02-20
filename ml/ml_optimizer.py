import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

class MLOptimizer:
    def __init__(self, data_dir="data", model_params_path="config/model_params.json"):
        """Initialize the ML optimizer with paths for data and model parameters."""
        self.data_dir = data_dir
        self.model_params_path = model_params_path
        self.model_params = self.load_model_params()

    def load_model_params(self):
        """Load or create model parameters."""
        if os.path.exists(self.model_params_path):
            with open(self.model_params_path, "r") as f:
                return json.load(f)
        else:
            default_params = {
                "n_estimators": 100,
                "max_depth": 5,
                "min_samples_split": 2,
                "min_samples_leaf": 1
            }
            self.save_model_params(default_params)
            return default_params

    def save_model_params(self, params):
        """Save optimized model parameters to JSON."""
        with open(self.model_params_path, "w") as f:
            json.dump(params, f, indent=4)
        print(f"✅ Updated model parameters saved to {self.model_params_path}")

    def load_training_data(self):
        """Load historical training data from CSV files."""
        file_path = os.path.join(self.data_dir, "training_data.csv")
        if not os.path.exists(file_path):
            print(f"❌ No training data found at {file_path}.")
            return None, None

        df = pd.read_csv(file_path)
        if "Close" not in df.columns or "Volume" not in df.columns:
            print(f"⚠️ Invalid training data format. Expected columns: 'Close', 'Volume'.")
            return None, None

        df.fillna(method="ffill", inplace=True)  # Handle missing values

        X = df[["Close", "Volume"]]
        y = df["Close"].shift(-1).dropna()

        return X[:-1], y  # Remove last row due to shift

    def optimize_model(self):
        """Optimize the machine learning model using GridSearchCV."""
        X, y = self.load_training_data()
        if X is None or y is None:
            return None

        model = RandomForestRegressor()
        param_grid = {
            "n_estimators": [50, 100, 200],
            "max_depth": [3, 5, 10],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4]
        }

        grid_search = GridSearchCV(model, param_grid, cv=3, scoring="neg_mean_absolute_error", n_jobs=-1)
        grid_search.fit(X, y)

        best_params = grid_search.best_params_
        print(f"🎯 Best Model Parameters: {best_params}")
        self.save_model_params(best_params)

        return best_params

    def evaluate_model(self):
        """Evaluate the trained model's performance on test data."""
        X, y = self.load_training_data()
        if X is None or y is None:
            return None

        model = RandomForestRegressor(**self.model_params)
        model.fit(X, y)

        predictions = model.predict(X)
        mae = mean_absolute_error(y, predictions)
        mse = mean_squared_error(y, predictions)

        print(f"📊 Model Evaluation:")
        print(f"   ✅ Mean Absolute Error (MAE): {mae:.4f}")
        print(f"   ✅ Mean Squared Error (MSE): {mse:.4f}")

        return mae, mse

    def run_full_optimization(self):
        """Run full ML optimization: tuning + evaluation."""
        best_params = self.optimize_model()
        if best_params:
            self.evaluate_model()

# ✅ Example Usage
if __name__ == "__main__":
    optimizer = MLOptimizer()
    optimizer.run_full_optimization()
