import pygame
import sys
import numpy as np

# Initialisation de Pygame
pygame.init()

# Dimensions de la grille

nb_colonnes = 7
nb_lignes = 6
taille_case = 100
rayon_jetons = taille_case // 2 - 5
largeur_fenetre = nb_colonnes * taille_case
hauteur_fenetre = (nb_lignes +1) * taille_case

# Couleurs
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
JAUNE = (255, 255, 0)
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Puissance 4")

# Création de la grille
grille = np.zeros((nb_lignes, nb_colonnes), dtype=int)

# Fonction pour dessiner la grille
def dessiner_grille(): 
    for colonne in range(nb_colonnes):
        for ligne in range(nb_lignes):
            pygame.draw.rect(fenetre, BLEU, (colonne * taille_case, (ligne + 1) * taille_case, taille_case, taille_case))
            pygame.draw.circle(fenetre, NOIR, (int(colonne*taille_case+taille_case/2), int(ligne*taille_case+taille_case+taille_case/2)), rayon_jetons)
            if grille[ligne][colonne] == 1:
                pygame.draw.circle(fenetre, ROUGE, (colonne * taille_case + taille_case // 2, (ligne + 1) * taille_case + taille_case // 2), rayon_jetons)
            elif grille[ligne][colonne] == 2:
                pygame.draw.circle(fenetre, JAUNE, (colonne * taille_case + taille_case // 2, (ligne + 1) * taille_case + taille_case // 2), rayon_jetons)
    pygame.display.update()

# Fonction pour placer un jeton dans la colonne choisie
def placer_jeton(colonne, joueur):
    for ligne in range(nb_lignes - 1, -1, -1):
        if grille[ligne][colonne] == 0:
            grille[ligne][colonne] = joueur
            return True
    return False

# Fonction pour vérifier s'il y a une victoire
def victoire(joueur):
    # Vérification horizontale
    for ligne in range(nb_lignes):
        for colonne in range(nb_colonnes - 3):
            if np.all(grille[ligne, colonne:colonne+4] == joueur):
                return True

    # Vérification verticale
    for colonne in range(nb_colonnes):
        for ligne in range(nb_lignes - 3):
            if np.all(grille[ligne:ligne+4, colonne] == joueur):
                return True

    # Vérification diagonale ascendante
    for colonne in range(nb_colonnes - 3):
        for ligne in range(3, nb_lignes):
            if np.all(grille[ligne-3:ligne+1, colonne:colonne+4].diagonal() == joueur):
                return True

    # Vérification diagonale descendante
    for colonne in range(nb_colonnes - 3):
        for ligne in range(nb_lignes - 3):
            if np.all(np.fliplr(grille[ligne:ligne+4, colonne:colonne+4]).diagonal() == joueur):
                return True

    return False

def message_victoire(message,tour):

    if tour == 0:
        couleur = ROUGE
    else: 
        couleur = JAUNE

    font = pygame.font.Font(None, 42)
    texte = font.render(message, True, couleur)
    texte_rect = texte.get_rect()

    # Centrez le rectangle du texte au milieu en haut du bandeau noir
    texte_rect.centerx = largeur_fenetre // 2  # Centre horizontalement
    texte_rect.top = texte.get_height() // 2  # Alignez le haut du texte au haut du bandeau noir

    # Créez une surface blanche de la même taille que la surface de texte
    fond_blanc = pygame.Surface(texte.get_size())
    fond_blanc.fill(BLANC)  # Remplit le fond avec la couleur blanche

    # Affichez le fond blanc puis le texte sur la fenêtre
    fenetre.blit(fond_blanc, texte_rect.topleft)  # Positionnez le fond blanc aux mêmes coordonnées que le texte
    fenetre.blit(texte, texte_rect)

def dessiner_rectangle_sous_souris(event,tour):
    pygame.draw.rect(fenetre, NOIR, (0,0, largeur_fenetre, taille_case))
    posx = event.pos[0]
    if tour == 0:
        pygame.draw.circle(fenetre, ROUGE, (posx, int(taille_case/2)), rayon_jetons)
    else: 
        pygame.draw.circle(fenetre, JAUNE, (posx, int(taille_case/2)), rayon_jetons)
    pygame.display.update()


# Fonction principale du jeu
def jouer():
    tour = 0
    jeu_termine = False
    dessiner_grille()
    while not jeu_termine:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                dessiner_rectangle_sous_souris(event,tour)

            if event.type == pygame.MOUSEBUTTONDOWN:
                dessiner_rectangle_sous_souris(event,tour-1)
            
                x = event.pos[0]
                colonne = x // taille_case
            
                if placer_jeton(colonne, tour % 2 + 1):
                    dessiner_grille()
                    if victoire(tour % 2 + 1):
                        if tour % 2 + 1 == 1:
                            message = "Joueur Rouge gagne !"
                        else:
                            message = "Joueur Jaune gagne !"

                        message_victoire(message,tour)

                        pygame.display.update()
                        pygame.time.wait(2000)
                        jeu_termine = True
                    tour += 1
                    tour = tour % 2

    pygame.quit()
    sys.exit()

# Lancement du jeu
if __name__ == "__main__":
    jouer()
