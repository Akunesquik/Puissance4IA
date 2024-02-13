
from FonctionsUtiles import *

typeAgent1 = choisir_agent() 
if typeAgent1.startswith('agent'):
        agent1=charger_agent(typeAgent1)

agent1.evaluate_model()