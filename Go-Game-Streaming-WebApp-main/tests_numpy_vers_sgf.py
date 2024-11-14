import sente
from sente import sgf
import numpy as np

"""
Méthode :


Dernière étape : reconstituer le sgf à partir des tableaux numpy et de sente

"""


#Dernière étape
"""
game = sgf.load("Go-Game-Streaming-WebApp/partie_test2.sgf", ignore_illegal_properties=True)
tab_coups=game.numpy(["black_stones", "white_stones"])
tab_coups_noir=game.numpy(["black_stones"])
tab_coups_blanc=game.numpy(["white_stones"])
board=game.get_board()

print(np.shape(tab_coups_noir))
"""

tab_coups=np.zeros((19,19,1))

def sgf_to_numpy(fic_sgf):
    game=sgf.load(fic_sgf)
    moves=game.get_default_sequence()
    nb_coups=len(moves)
    result=np.zeros((nb_coups+1,19,19)) # result[i] = photographie du goban au moment i de la partie = tableau numpy 19x19
    #0 représente un emplacement où il n'ay pas de pierre
    #1 représente un emplacement où il y a une pierre noire
    #2 représente un emplacement où il y a une pierre blanche
    for i in range(1,nb_coups+1):
        game.play(moves[i-1])
        tab_coups_noir=game.numpy(["black_stones"])
        #print(tab_coups_noir)
        tab_coups_noir=game.numpy(["black_stones"])
        tab_coups_blanc=game.numpy(["white_stones"])
        for ligne in range(19):
            for colonne in range(19):
                if tab_coups_noir[ligne][colonne][0]==1:
                    result[i,ligne,colonne]=1
                if tab_coups_blanc[ligne][colonne][0]==1:
                    result[i,ligne,colonne]=2
    return result

result=sgf_to_numpy("/home/luc/Documents/imt_atlantique/commande_entreprise/projet_go/TenukiGo2/TenukiGo/Go-Game-Streaming-WebApp-main/partie_vs_organos _8k_.sgf")
print(result[4])

def liste_coups_to_sgf(liste):
    #liste[i] contient la position du coup i sous la forme d'un tuple (ligne_coup,colonne_coup,n°pierre) ou n°pierre=1 si c'est noir qui joue et 2
    # si c'est blanc qui joue
    game=sente.Game()
    for i in range(len(liste)):
        game.play(liste[i][0],liste[i][1])
    return sgf.dumps(game)


liste=[(17,4,1),(17,16,2),(4,4,1),(4,16,2)]

sgf=liste_coups_to_sgf(liste)

fichier=open("sgf_test_fonction_liste_coups_to_sgf.sgf", "w")
fichier.write(sgf)
fichier.close()

game = sgf.load("/home/luc/Documents/imt_atlantique/commande_entreprise/projet_go/TenukiGo2/TenukiGo/sgf_test_fonction_liste_coups_to_sgf.sgf", ignore_illegal_properties=True)
game.play_default_sequence()
print(game.get_board())
game.play_default_sequence()
print(game.get_board())
game.play_default_sequence()
print(game.get_board())
game.play_default_sequence()
print(game.get_board())

