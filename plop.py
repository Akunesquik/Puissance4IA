import tensorflow as tf

# Définition de la fonction de perte personnalisée
def custom_loss(y_true, y_pred):
    # Comparaison entre les prédictions et les vraies étiquettes
    incorrect_predictions = tf.cast(tf.not_equal(tf.round(y_pred), tf.cast(y_true, dtype=tf.float32)), dtype=tf.float32)
    
    # Retourner 1 pour les prédictions incorrectes et 0 pour les prédictions correctes
    return incorrect_predictions

# Test de la fonction de perte personnalisée
y_true = tf.constant([0., 1., 1., 0.])  # Vraies étiquettes
y_pred = tf.constant([0.2, 0.8, 0.6, 0.3])  # Prédictions du modèle

loss = custom_loss(y_true, y_pred)
print(loss.numpy())  