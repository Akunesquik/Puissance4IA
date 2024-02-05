import random
import numpy as np
from collections import deque
from keras.layers import Dense
from keras.optimizers import Adam
import tensorflow as tf

class DQNAgent:
    def __init__(
        self,
        learning_rate=0.0001,
        gamma=0.99,
        epsilon=0.1,
        epsilon_decay=0.995,
        epsilon_min=0.01,
        memory_size=10000,
        batch_size=32,
        name="",
    ):
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.memory = deque(maxlen=memory_size)
        self.batch_size = batch_size
        self.state_size = (7,6,3)  # Input state dimensions
        self.action_size = 7  # Output action dimension
        self.name = name
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.optimizer = Adam(lr=self.learning_rate)
        self.update_target_freq = 200

    def _build_model(self,):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(256, activation='relu'))
        model.add(tf.keras.layers.Dense(128, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation="softmax"))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model
    
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state)
        return np.argmax(q_values) % self.action_size
    
    def learn(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        q_target = self.target_model.predict(next_state)
        y = reward + self.gamma * np.max(q_target) * (1 - done)

        q_values = self.model.predict(state)
        q_values[0, action] = y

        self.model.fit(state, q_values, epochs=1, verbose=0)

        # Mise à jour du réseau cible
        # Update target network, considering stability and transfer learning
        self.update_target_model()
    
    def update_target_model(self):
        # Soft update for stability, optionally explore hard updates
        tau = 0.99  # Adjustment parameter
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i, (w, tw) in enumerate(zip(weights, target_weights)):
            target_weights[i] = tau * w + (1 - tau) * tw
        self.target_model.set_weights(target_weights)


    ##def replay(self):
    ##    if len(self.memory) < self.batch_size:
    ##        return
    ##    minibatch = random.sample(self.memory, self.batch_size)
    ##    states, actions, rewards, next_states, done = zip(*minibatch)
    ##    
    ##    # One-hot encode actions for better learning (consider alternatives)
    ##    actions_one_hot = tf.keras.utils.to_categorical(actions, self.action_size)

    ##    # Predict Q-values for current states
    ##    q_values = self.model.predict(states)

    ##    # Calculate target Q-values for each action using Bellman equation
    ##    target_q_values = rewards + self.gamma * np.max(self.target_model.predict(next_states), axis=1) * (1 - done)

    ##    # Update Q-values in the minibatch for the chosen actions
    ##    q_values[np.arange(self.batch_size), actions] = target_q_values

    ##    # Fit the model on the minibatch
    ##    self.model.fit(np.expand_dims(states, axis=0), np.expand_dims(q_values, axis=0), epochs=1, verbose=0)

    ##    # Update target network, considering stability and transfer learning
    ##    self.update_target_model()