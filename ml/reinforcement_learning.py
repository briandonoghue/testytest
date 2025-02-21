import logging
import numpy as np
import random
import tensorflow as tf
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from core.performance_tracker import PerformanceTracker
from core.market_data import MarketData
from utilities.error_handler import ErrorHandler

class ReinforcementLearningAI:
    """ Reinforcement Learning model for continuous trade strategy improvement """

    def __init__(self, config):
        """
        Initializes the reinforcement learning AI.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.performance_tracker = PerformanceTracker(config)
        self.error_handler = ErrorHandler()

        # Reinforcement Learning Parameters
        self.state_size = 5  # Features: price change %, RSI, MACD, liquidity, volatility
        self.action_size = 3  # Actions: Hold, Buy, Sell
        self.gamma = 0.95  # Discount factor for future rewards
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01  # Minimum exploration probability
        self.epsilon_decay = 0.995  # Decay factor for exploration rate
        self.learning_rate = 0.001
        self.memory = deque(maxlen=2000)
        self.model = self._build_model()

        # Setup logging
        logging.basicConfig(
            filename="logs/reinforcement_learning.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def _build_model(self):
        """
        Builds a Deep Q-Network (DQN) for reinforcement learning.
        :return: Compiled neural network model.
        """
        model = Sequential([
            Dense(64, input_dim=self.state_size, activation="relu"),
            Dense(64, activation="relu"),
            Dense(self.action_size, activation="linear")
        ])
        model.compile(loss="mse", optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def train_rl_model(self, symbol):
        """
        Trains the reinforcement learning model based on past trades.
        :param symbol: Trading asset symbol.
        """
        logging.info(f"Training reinforcement learning model for {symbol}...")

        # Load historical market data
        market_df = self.market_data.get_historical_data(symbol, period="180d")  # 6 months
        if market_df is None:
            logging.warning(f"No historical data available for {symbol}.")
            return

        # Prepare training data
        states, actions, rewards = self._prepare_rl_training_data(market_df)

        # Train using Q-learning
        for i in range(len(states)):
            state = np.reshape(states[i], [1, self.state_size])
            target = self.model.predict(state)

            # Update Q-value based on reward
            target[0][actions[i]] = rewards[i]
            self.model.fit(state, target, epochs=1, verbose=0)

        # Reduce exploration rate
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        logging.info(f"RL model training completed for {symbol}.")

    def _prepare_rl_training_data(self, market_df):
        """
        Processes historical market data for reinforcement learning.
        :param market_df: DataFrame containing price history.
        :return: Processed state-action-reward dataset.
        """
        states, actions, rewards = [], [], []
        market_df["price_change"] = market_df["price"].pct_change()
        market_df["RSI"] = 100 - (100 / (1 + market_df["price"].pct_change().rolling(window=14).mean()))
        market_df["MACD"] = market_df["price"].ewm(span=12, adjust=False).mean() - market_df["price"].ewm(span=26, adjust=False).mean()
        market_df["volatility"] = market_df["price"].rolling(window=20).std()
        market_df.dropna(inplace=True)

        for i in range(len(market_df) - 1):
            state = market_df.iloc[i][["price_change", "RSI", "MACD", "volatility"]].values
            next_price = market_df.iloc[i + 1]["price"]

            # Assign action: 0 = Hold, 1 = Buy, 2 = Sell
            action = random.choice([0, 1, 2])  # Random initial exploration
            reward = (next_price - market_df.iloc[i]["price"]) if action == 1 else (-1 * (next_price - market_df.iloc[i]["price"]) if action == 2 else 0)

            states.append(state)
            actions.append(action)
            rewards.append(reward)

        return np.array(states), np.array(actions), np.array(rewards)

    def predict_trade_action(self, symbol):
        """
        Predicts the optimal trade action (Hold, Buy, Sell) using reinforcement learning.
        :param symbol: Trading asset symbol.
        :return: Suggested action and confidence score.
        """
        market_df = self.market_data.get_historical_data(symbol, period="60d")
        if market_df is None:
            logging.warning(f"No market data available for prediction on {symbol}.")
            return None

        state = market_df.iloc[-1][["price_change", "RSI", "MACD", "volatility"]].values
        state = np.reshape(state, [1, self.state_size])
        q_values = self.model.predict(state)

        action = np.argmax(q_values[0])  # Select the action with the highest Q-value
        confidence = q_values[0][action] / sum(q_values[0])  # Normalize confidence

        action_map = {0: "Hold", 1: "Buy", 2: "Sell"}
        logging.info(f"RL Trade Prediction for {symbol}: {action_map[action]} (Confidence: {confidence:.2f})")

        return {"symbol": symbol, "action": action_map[action], "confidence": round(confidence, 2)}
