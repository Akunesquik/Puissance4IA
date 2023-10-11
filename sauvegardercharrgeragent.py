import pickle

# Enregistrez l'agent dans un fichier
with open('agent.pkl', 'wb') as agent_file:
    pickle.dump(votre_agent, agent_file)


# Chargez l'agent à partir du fichier
with open('agent.pkl', 'rb') as agent_file:
    agent_charge = pickle.load(agent_file)