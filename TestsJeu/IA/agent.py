import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
import tensorflow as tf
import random, time, json
from CreationJeuDeDonneePourEvaluate import creer_situation_partie
from datetime import datetime

class DQNAgent:
    def __init__(self, learning_rate=0.001, gamma=0.99, epsilon=1, epsilon_decay=0.995, epsilon_min=0.01, memory_size=2000000, batch_size=32):
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
        self.tensorboard = tf.keras.callbacks.TensorBoard(log_dir="logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S"))

    def build_model(self):
        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.Input(shape=self.state_size))  # Input layer with shape (6, 7, 3)
        self.model.add(tf.keras.layers.Flatten())  # Flatten the input
        self.model.add(tf.keras.layers.Dense(512, activation='relu'))
        self.model.add(tf.keras.layers.Dense(256, activation='relu'))
        self.model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))

        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        state = state.reshape(1, 6, 7)  # Redimensionner l'état en (1, 6, 7) pour correspondre à la forme attendue par le modèle
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        return np.argmax(self.model.predict(state, verbose=0)[0])

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
        targets[np.arange(len(targets)), actions] = rewards + self.gamma * np.max(self.model.predict(next_states, verbose=0), axis=1) * ~dones
        self.model.fit(states, targets, epochs=1, verbose=0, callbacks=[self.tensorboard])
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
        
    def save_model_agent(self):
        path = 'TestsJeu/Save_Agent/'
        pathModel = path + f'models/{self.name}'
        pathHyperpara = path + f'hyperparametres/{self.name}.json'

        # Save hyperparameters to JSON
        hyperparameters = {
            "learning_rate": self.learning_rate,
            "gamma": self.gamma,
            "epsilon": self.epsilon,
            "epsilon_decay": self.epsilon_decay,
            "epsilon_min": self.epsilon_min,
            "memory_size": self.memory.maxlen,
            "batch_size": self.batch_size
        }
        with open(pathHyperpara, "w") as f:
            json.dump(hyperparameters, f)

        # Save model
        self.model.save(pathModel)
        print(f"Model saved for {self.name}")

    def load_model_agent(self):
        path = 'TestsJeu/Save_Agent/'
        pathModel = path + f'models/{self.name}'
        pathHyperpara = path + f'hyperparametres/{self.name}.json'

        # Load hyperparameters from JSON
        with open(pathHyperpara, "r") as f:
            hyperparameters = json.load(f)
            self.learning_rate = hyperparameters["learning_rate"]
            self.gamma = hyperparameters["gamma"]
            self.epsilon = hyperparameters["epsilon"]
            self.epsilon_decay = hyperparameters["epsilon_decay"]
            self.epsilon_min = hyperparameters["epsilon_min"]
            self.memory_size = hyperparameters["memory_size"]
            self.batch_size = hyperparameters["batch_size"]

        # Load model
        self.model = tf.keras.models.load_model(pathModel)
        print(f"Model loaded for {self.name}")


    # Méthode pour évaluer le modèle
    def evaluate_model(self, num_episodes=100):
        X_eval = []  # Liste pour stocker les états de jeu
        y_eval = []  # Liste pour stocker les réponses correctes

        # Génération des données d'évaluation
        situations = creer_situation_partie(num_episodes)

        for grille, reponse in situations:
            X_eval.append(grille)
            y_eval.append(reponse)

        X_eval = np.array(X_eval)
        y_eval = np.array(y_eval)

        # Evaluation du modèle
        loss = self.model.evaluate(X_eval, y_eval, verbose=0)

        print("Loss:", loss)

        # Ajout de la perte à TensorBoard avec un pas de temps basé sur l'heure actuelle
        current_time = int(time.time())
        with tf.summary.create_file_writer(f"logs/eval").as_default():
            tf.summary.scalar("loss", loss, step=current_time)