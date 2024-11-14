import sente
from sente import sgf
import numpy as np

"""
Méthode :


Dernière étape : reconstituer le sgf à partir des tableaux numpy et de sente

"""


#Dernière étape
game = sgf.load("Go-Game-Streaming-WebApp/partie_test2.sgf", ignore_illegal_properties=True)
tab_coups=game.numpy(["black_stones", "white_stones"])
tab_coups_noir=game.numpy(["black_stones"])
tab_coups_blanc=game.numpy(["white_stones"])

print(np.shape(tab_coups_noir))

tab_coups=np.zeros(np.shape(tab_coups_noir))





