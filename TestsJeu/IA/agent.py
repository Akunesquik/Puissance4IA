import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, Reshape, Dropout
from keras.optimizers import Adam
import tensorflow as tf
import random, time, json
from CreationJeuDeDonneePourEvaluate import creer_situation_partie
from datetime import datetime
from CreationJeuDeDonneePourEvaluate import TrouveMeilleureActionAvecReward

class DQNAgent:
    def __init__(self, learning_rate=None, gamma=None, epsilon=1.0, epsilon_decay=0.999, epsilon_min=None, memory_size=None, batch_size=None):
        self.state_size = (6, 7)
        self.action_size = 7
        self.learning_rate = learning_rate if learning_rate is not None else random.uniform(1e-5, 1e-1)
        self.gamma = gamma if gamma is not None else random.uniform(0.9, 0.999)
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay 
        self.epsilon_min = epsilon_min if epsilon_min is not None else random.uniform(0.01, 0.1)
        self.memory_size = memory_size if memory_size is not None else random.randint(10000, 2000000)
        self.batch_size = batch_size if batch_size is not None else random.randint(16, 128)
        self.memory = deque(maxlen=self.memory_size)
        self.model = Sequential()
        self.tensorboard = tf.keras.callbacks.TensorBoard(log_dir="logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S"))

    def build_model(self):
        self.model = Sequential([
            Reshape((6, 7, 1), input_shape=self.state_size),  # Reshape to add a channel dimension
            Conv2D(64, (3, 3), activation='relu'),
            Conv2D(32, (3, 3), activation='relu'),
            Flatten(),
            Dense(128, activation='relu'),
            Dense(self.action_size, activation='linear')
        ])

        self.model.compile(optimizer=Adam(learning_rate=self.learning_rate), loss='mse') 

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        state = state.reshape(1, 6, 7)  # Redimensionner l'état en (1, 6, 7) pour correspondre à la forme attendue par le modèle
        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.action_size)
        q_values = self.model.predict(state,verbose=0)
        return np.argmax(q_values[0])

    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        minibatch = random.sample(self.memory, self.batch_size)
        states, targets = [], []
        for state, action, reward, next_state, done in minibatch:
            state = state.reshape(1, 6, 7)
            next_state = next_state.reshape(1, 6, 7)  
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state,verbose=0)[0]))
            target_f = self.model.predict(state,verbose=0)
            target_f[0][action] = target
            states.append(state[0])
            targets.append(target_f[0])
        self.model.fit(np.array(states), np.array(targets), epochs=1, verbose=0 )# , callbacks=[self.tensorboard])
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
    def evaluate_model(self):
        # Chargement des données d'évaluation à partir du fichier JSON
        with open('evaluation_data.json', 'r') as f:
            evaluation_data = json.load(f)

        X_eval = []  # Liste pour stocker les états de jeu
        y_eval = []  # Liste pour stocker les réponses correctes

        # Parcours des données d'évaluation chargées
        for grille, meilleure_colonne in evaluation_data:
            X_eval.append(grille)
            y_eval.append(meilleure_colonne)

        X_eval = np.array(X_eval)
        y_eval = np.array(y_eval)

        bonpoint = 0
        for i in range(len(X_eval)): 
            # Evaluation du modèle
            reponseBot = self.act(X_eval[i])
            if reponseBot == y_eval[i]: 
                bonpoint += 1
            # else:
            #     print(X_eval[i])
            #     print(f"Act Bot {reponseBot + 1}")
            #     print(f"Bonne reponse {y_eval[i] +1}" )
        print(f"Nombre bonne reponse {bonpoint} / {len(X_eval)}")

        loss = self.model.evaluate(X_eval, y_eval, verbose=0)

        #print("Loss:", loss)

        # Ajout de la perte à TensorBoard avec un pas de temps basé sur l'heure actuelle
        current_time = int(time.time())
        with tf.summary.create_file_writer(f"logs/{self.name}/eval").as_default():
            tf.summary.scalar("score", bonpoint, step=current_time)