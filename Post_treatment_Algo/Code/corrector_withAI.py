#import sgf
import numpy as np
from sgf_to_numpy import *
import itertools
import sys
sys.path.append("Post_treatment_AI/Code")
from Fill_gaps_model import *

def indices_to_sgf_coords(x, y, board_size):
    """Convert array indices to SGF coordinates."""
    return f"{chr(y + ord('a'))}{chr(board_size - x - 1 + ord('a'))}"


def get_possible_moves(initial_state, final_state):
    """
    Get possible moves in a gap by subtracting the final state from the initial state.
    
    Args:
        initial_state (np.array): The initial board state.
        final_state (np.array): The final board state.
    Returns:
        black_moves (list of tuple): List of moves made by black.
        white_moves (list of tuple): List of moves made by white.
    """
    # Calculate the difference between states
    difference = final_state - initial_state
    
    # Find all black moves (difference == 1)
    black_moves = np.argwhere(difference == 1)
    black_moves = [tuple(move) for move in black_moves]
    
    # Find all white moves (difference == 2)
    white_moves = np.argwhere(difference == 2)
    white_moves = [tuple(move) for move in white_moves]
    
    return black_moves, white_moves

def differences(tab1,tab2):
    pierres_noires_ajoutées=[]
    pierres_noires_retirées=[]
    pierres_blanches_ajoutées=[]
    pierres_blanches_retirées=[]
    nb_ajouts=0
    for ligne in range(19):
        for col in range(19):
            if tab2[ligne,col]==1 and tab1[ligne,col] ==0:
                pierres_noires_ajoutées.append((ligne,col,1))
                nb_ajouts+=1
            
            if tab2[ligne,col]==0 and tab1[ligne,col] ==1:
                pierres_noires_retirées.append((ligne,col,1))
            
            if tab2[ligne,col]==2 and tab1[ligne,col] ==0:
                pierres_blanches_ajoutées.append((ligne,col,2))
                nb_ajouts+=1
            
            if tab2[ligne,col]==0 and tab1[ligne,col] ==2:
                pierres_blanches_retirées.append((ligne,col,2))
           
            if tab2[ligne,col]==2 and tab1[ligne,col] ==1:
                pierres_noires_retirées.append((ligne,col,1))
                pierres_blanches_ajoutées.append((ligne,col,2))
                nb_ajouts+=1
            
            if tab2[ligne,col]==1 and tab1[ligne,col] ==2:
                pierres_blanches_retirées.append((ligne,col,2))
                pierres_noires_ajoutées.append((ligne,col,1))
                nb_ajouts+=1
    return {1 : {"ajout" : pierres_noires_ajoutées, "retire" : pierres_noires_retirées}, 
            2 : {"ajout" :pierres_blanches_ajoutées, "retire" : pierres_blanches_retirées}}, nb_ajouts

def sequence_to_sgf(sequence, board_size=19):
    """
    Convert a sequence of Go board states back to SGF format.
    
    Args:
        sequence (list of np.array): Sequence of board states.
        board_size (int): Size of the Go board.
    
    Returns:
        sgf_string (str): SGF representation of the game.
    """
    sgf_moves = []
    prev_board = np.zeros_like(sequence[0])
    
    for board in sequence[1:]:
        diff = board - prev_board
        move = np.where(diff != 0)
        if len(move[0]) > 0:  # There is a move
            x, y = move[0][0], move[1][0]
            color = 'B' if board[x, y] == 1 else 'W'
            sgf_moves.append(f";{color}[{indices_to_sgf_coords(x, y, board_size)}]")
        prev_board = board
    
    sgf_string = f"(;GM[1]SZ[{board_size}]" + "".join(sgf_moves) + ")"
    return sgf_string

def get_last_index(L,e):
    index=-1
    for i in range (len(L)):
        if L[i]==e:
            index=i
    return index



def correcteur2(liste_tableaux):
    liste_coups=[]
    #liste[i] contient la position du coup i sous la forme d'un tuple (ligne_coup,colonne_coup,n°pierre) ou n°pierre=1 si c'est noir qui joue et 2
    # si c'est blanc qui joue
    Nb_frames = len(liste_tableaux)

    turn=1 #contient 1 si c'est à noir de jouer, 2 si c'est à blanc de jouer
    notturn=2
    for index in range(1,Nb_frames):
        D,nb_ajouts=differences(liste_tableaux[index-1],liste_tableaux[index])
        #pierres_noires_ajoutées=D[1]["ajout"]
        #pierres_noires_retirées=D[1]["retire"]
        #pierres_blanches_ajoutées=D[2]["ajout"]
        #pierres_blanches_retirées=D[2]["retire"]
        
        
        if nb_ajouts!=0: # s'il il y a des pierres ajoutées, on les cherche pour les mettre dans la liste des coups
            
            # On vérifie que le nombre de pierres ajoutées est cohérent du point de vue du fait que les joueurs jouent à tour de rôle 
            # CAS N°1
            if len(D[turn]["ajout"])==1 and len(D[notturn]["ajout"])==0: 
                liste_coups.append(D[turn]["ajout"][0])
                print("player ", turn, " played at ", D[turn]["ajout"][0])
                temp=turn # On change le tour du joueur pour la prochaine iteration
                turn=notturn
                notturn=temp
            elif (len(D[turn]["ajout"])==0 and len(D[notturn]["ajout"])==0): 
                continue
            else:
                b,w = get_possible_moves(liste_tableaux[index],liste_tableaux[index-1])
                liste_tableaux=fill_gaps(model,liste_tableaux,index-1,index,b, w).copy()
                index-=1
                
               
                
            
          
    return liste_coups

#fichier=open("TenukiGo2/TenukiGo/Go-Game-Streaming-WebApp-main/partie_vs_organos _8k_.sgf", "r")

    



                

   

            
            

            

















