import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
import tensorflow as tf
import random
import json

class DQNAgent:
    def __init__(self,learning_rate=0.001, gamma=0.99, epsilon=1.0, epsilon_decay=0.98, epsilon_min=0.01, memory_size=2000, batch_size=32):
        self.state_size = (6,7)
        self.action_size = 7
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.memory = deque(maxlen=memory_size)
        self.batch_size = batch_size
        self.model = Sequential()

    def build_model(self):
        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.Input(shape=self.state_size))  # Input layer with shape (6, 7, 3)
        self.model.add(tf.keras.layers.Flatten())  # Flatten the input
        self.model.add(tf.keras.layers.Dense(2048, activation='relu'))
        self.model.add(tf.keras.layers.Dense(1024, activation='relu'))
        self.model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))

        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        state = state.reshape(1, 6, 7)  # Redimensionner l'état en (1, 6, 7) pour correspondre à la forme attendue par le modèle
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        return np.argmax(self.model.predict(state,verbose=0)[0])

    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        minibatch = random.sample(self.memory, self.batch_size)
        
        # Extraire chaque élément de la mémoire
        states = np.array([transition[0] for transition in minibatch])
        actions = np.array([transition[1] for transition in minibatch])
        rewards = np.array([transition[2] for transition in minibatch])
        next_states = np.array([transition[3] for transition in minibatch])
        dones = np.array([transition[4] for transition in minibatch])
        
        targets = self.model.predict(states, verbose=0)
        targets[np.arange(len(targets)), actions] = rewards + self.gamma * np.max(self.model.predict(next_states,verbose =0), axis=1) * ~dones
        self.model.fit(states, targets, epochs=1, verbose=0)
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
        

    def save_model_agent(self):
        """
        Sauvegarde le modèle et les hyperparamètres d'un agent DQN.

        Args:
            agent: L'agent DQN à sauvegarder.
            model_path: Le chemin d'accès au fichier où le modèle sera sauvegardé.
            hyperparameters_path: Le chemin d'accès au fichier où les hyperparamètres seront sauvegardés.
        """
        path='TestsJeu/Save_Agent/' 
        pathModel = path + f'models/{self.name}'
        pathHyperpara = path + f'hyperparametres/{self.name}.json'
        # Sauvegarde du modèle
        self.model.save(pathModel)
        print(f"Model Saved for {self.name}")

        # Sauvegarde des hyperparamètres
        with open(pathHyperpara, "w") as f:
            json.dump({"learning_rate": self.learning_rate, "gamma": self.gamma, "epsilon": self.epsilon}, f)

    def load_model_agent(self):
        """
        Charge un agent DQN à partir d'un fichier de sauvegarde.

        Args:
            model_path: Le chemin d'accès au fichier où le modèle est sauvegardé.
            hyperparameters_path: Le chemin d'accès au fichier où les hyperparamètres sont sauvegardés.

        Returns:
            Un agent DQN avec les paramètres chargés.
        """
        path='TestsJeu/Save_Agent/' 
        pathModel = path + f'models/{self.name}'
        pathHyperpara = path + f'hyperparametres/{self.name}.json'

        # Chargement des hyperparamètres
        with open(pathHyperpara, "r") as f:
            hyperparameters = json.load(f)
            
        self.model = tf.keras.models.load_model(pathModel)
        print(f"Model loaded for {self.name}")
