# Puissance4IA

Projet de fin d'études

https://github.com/Akunesquik/Puissance4IA.git

  
## Creer un nouvel environnement python et l'activer

pip install virtualenv

python -m virtualenv Puissance4env 

Puissance4env\Scripts\activate

  
## Desactiver le virtualenv créé plus tôt : 

deactivate

  
## Installer tous les packages nécessaires dans le nouvel environnement

pip install -r requirements.txt
  
## Entrainement

Vous pouvez utiliser le fichier NewTrain.py

python TestsJeu/NewTrain.py


Choisissez ensuite le nombre de partie et qui joue contre qui

alea : pour aleatoire

humain : pour une personne qui va cliquer

agent{nom} : {nom} est à remplacer par si vous voulez lui donner un nom, si l'agent{nom} existe, alors il sera chargé, sinon il sera crée

  
## Evaluation des modèles

Pour evaluer tous les modèles, vous pouvez vous servir du fichier evaluate_model.py

le modèle sera évalué grace au jeu de données dans evaluation_data.json

python TestsJeu/evaluate_model.py

  
## Observation de la précision d'un modèle

Pour évaluer la précision d'un modele par rapport à un système de récompenses,

vous pouvez utiliser le fichier JouerPartie.py

ce fichier vous permettra de jouer (en sélectionnant vos agents contre qui vous voulez) et de voir ce que aurais du jouer la premier jouer en fonction des recompenses que vous choisissez dans typeBestMove(ligne 9)
  
python TestsJeu/JouerPartie.py

  
## TensorBoard

Pour observé les résultats obtenus lors des évaluations, nous avons utilisé TensorBoard afin de sauvegarder les scores en fonction du temps

Pour s'en servir utilisé la commande suivante qui hostera la page interne sur : http://localhost:6006
  
tensorboard --logdir=./logs


### A savoir

/TestsJeu : Posséde les dossiers et fichiers utiles pour l'exploitation de nos agents

- /Game : comprend tout ce qui touche au puissance 4 natif

- /IA : comprend tout ce qui touche à l'IA, recompenses.

- /Resultats : Tous les fichiers de résultats en .txt

- /Save_Agent : dossier de sauvegarde d'hyperparamètres et des modèles

/logs : fichier et dossiers permettant l'analyse et l'utilisation de TesnorBoard

/archives : (INUTILE) : Commencement du projet



