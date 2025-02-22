import logging
import numpy as np
import random
from collections import deque
from sklearn.linear_model import LinearRegression
from core.performance_tracker import PerformanceTracker
from core.market_data import MarketData
from utilities.error_handler import ErrorHandler

class ReinforcementLearningAI:
    """ Reinforcement Learning model for continuous trade strategy improvement using basic Q-learning """

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

        # Q-table for Q-learning (simpler alternative to deep learning models)
        self.q_table = {}

        # Setup logging
        logging.basicConfig(
            filename="logs/reinforcement_learning.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

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
            state = tuple(states[i])  # Convert to tuple for hashability in the Q-table
            if state not in self.q_table:
                self.q_table[state] = np.zeros(self.action_size)

            # Choose action based on the epsilon-greedy policy
            if random.random() < self.epsilon:
                action = random.choice([0, 1, 2])  # Explore action space
            else:
                action = np.argmax(self.q_table[state])  # Exploit learned values

            # Update Q-value based on reward
            reward = rewards[i]
            old_q_value = self.q_table[state][action]
            future_q_value = np.max(self.q_table[tuple(states[i + 1])]) if i + 1 < len(states) else 0

            # Q-learning formula
            self.q_table[state][action] = old_q_value + self.learning_rate * (reward + self.gamma * future_q_value - old_q_value)

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
        Predicts the optimal trade action (Hold, Buy, Sell) using Q-learning.
        :param symbol: Trading asset symbol.
        :return: Suggested action and confidence score.
        """
        market_df = self.market_data.get_historical_data(symbol, period="60d")
        if market_df is None:
            logging.warning(f"No market data available for prediction on {symbol}.")
            return None

        state = market_df.iloc[-1][["price_change", "RSI", "MACD", "volatility"]].values
        state = tuple(state)  # Convert to tuple for hashability in the Q-table

        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.action_size)

        # Choose action based on the epsilon-greedy policy
        if random.random() < self.epsilon:
            action = random.choice([0, 1, 2])  # Explore action space
        else:
            action = np.argmax(self.q_table[state])  # Exploit learned values

        confidence_score = self.q_table[state][action]  # Use the Q-value as confidence score

        logging.info(f"Predicted action for {symbol}: {['Hold', 'Buy', 'Sell'][action]} with confidence: {confidence_score:.2f}")
        return action, confidence_score
