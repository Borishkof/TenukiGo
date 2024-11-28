import sente
from sente import sgf
import numpy as np
from tests_numpy_vers_sgf import *

"""
On a une liste de tableaux numpy représentant les états de la partie. L'idée de base est de retrouver les cops en regaradnt les différneces
entre deux états consécutifs.

On suppose que c'est à blanc de jouer.

Cas N° 1.1 (principal) : 
pierres_noires_ajoutées : 0 
pierres_noires_retirées : 0
pierres_blanches_ajoutées : +1
pierres_blanches_retirées : 0

Correction : Entre 2 états, on ajoute une pierre de la bonne couleur. Dans ce cas, on ajoute le coup à la liste de coups.

Cas N° 1.2 : 2 coups rapides 
pierres_noires_ajoutées : +1 
pierres_noires_retirées : 0
pierres_blanches_ajoutées : +1
pierres_blanches_retirées : 0

Correction : On interprète ça comme un coup joué rapidement. On ajoute les 2 coups dans la liste des coups.


Cas N° 1.3 : + de 2 coups rapides 
pierres_noires_ajoutées : +(x-1) 
pierres_noires_retirées : 0
pierres_blanches_ajoutées : +x, x>1
pierres_blanches_retirées : 0

Correction : On interprète ça comme plusieurs coup joués rapidement ou bien une ocultation du plateau. 
On utilise l'IA pour reconstituer si on peut, sinon on ajoute les coups au hasard et on SIGNALE.


Cas N° 2.1 : joueur qui joue plusieurs coup de suite
pierres_noires_ajoutées : 0 
pierres_noires_retirées : 0
pierres_blanches_ajoutées : y, y>1 
pierres_blanches_retirées : 0

Correction : On ne peut l'interpréter que comme une violation des règles : Blanc a joué plusieurs fois de suite
BLOCAGE!!!!!! -> Attendre de revenir dans un des autres cas pour agir (regarder les frames suivantes)

Cas N° 2.2 : joueur qui joue plusieurs coup de suite
pierres_noires_ajoutées : +x 
pierres_noires_retirées : 0
pierres_blanches_ajoutées : 0 
pierres_blanches_retirées : 0

Correction : On ne peut l'interpréter que comme une violation des règles : Noir a joué plusieurs fois de suite
BLOCAGE!!!!!! -> Attendre de revenir dans un des autres cas pour agir (regarder les frames suivantes)

Cas N° 3 : déplacement de pierres
pierres_noires_ajoutées : +x
pierres_noires_retirées : -x
pierres_blanches_ajoutées : +y 
pierres_blanches_retirées : -y

Correction : On interprète cette variation comme le fait que des pierres noires ou blanches ont été déplacées.
Cas x=1 : on modifie le coup dans la liste des coups
Cas x>1 : IA ou bien pas de modification ou bien modifications au hasard de la liste des coups. À signaler !!! 
Idem pour y.


Cas N° 4.1 : capture de pierres
pierres_noires_ajoutées : 0 
pierres_noires_retirées : -x
pierres_blanches_ajoutées : 0 
pierres_blanches_retirées : -y

Correction : On interprète cette variation comme la capture d'un groupe de pierres noires/ de pierres blanches. Pas de modification de la liste
des coups.

Cas N° 4.2 : capture de pierres et 1 coup rapide
pierres_noires_ajoutées : 0 
pierres_noires_retirées : 0
pierres_blanches_ajoutées : +1 
pierres_blanches_retirées : -y

Correction : On interprète cette variation comme la capture d'un groupe de pierres blanches avec un coup rapide. On ajoute le coup à la liste des 
coups.

Cas N° 4.3 : capture de pierres et 2 coups rapides
pierres_noires_ajoutées : +1 
pierres_noires_retirées : -x
pierres_blanches_ajoutées : +1 
pierres_blanches_retirées : -y

Correction : On interprète cette variation comme la capture d'un groupe de pierres blanches avec 2 coups rapide. On ajoute les 2 coups à la liste des 
coups.

Cas N° 4.4 : capture de pierres et + de 2 coups rapides
pierres_noires_ajoutées : + (z-1) 
pierres_noires_retirées : -x
pierres_blanches_ajoutées : + z , z>1
pierres_blanches_retirées : -y

Correction : On interprète ça comme plusieurs coup joués rapidement ou bien une ocultation du plateau. 
On utilise l'IA pour reconstituer is on peut, sinon on ajoute les coups au hasard et on SIGNALE.

"""

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



def get_last_index(L,e):
    index=-1
    for i in range (len(L)):
        if L[i]==e:
            index=i
    return index



def correcteur1(liste_tableaux):
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
            if len(D[turn]["ajout"])-len(D[notturn]["ajout"])==1: 
                liste_coups.append(D[turn]["ajout"][0])
                for k in range(len(D[notturn]["ajout"])):
                    liste_coups.append(D[notturn]["ajout"][k])
                    liste_coups.append(D[turn]["ajout"][k+1])
                temp=turn # On change le tour du joueur pour la prochaine iteration
                turn=notturn
                notturn=temp
            if len(D[turn]["ajout"])-len(D[notturn]["ajout"])==0 and len(D[turn]["ajout"])>=1: 
                print(index)
                for k in range(len(D[notturn]["ajout"])):
                    liste_coups.append(D[turn]["ajout"][k])
                    liste_coups.append(D[notturn]["ajout"][k])
     
            else:
                #On traite le cas où une seule pierre a été déplacée en modifiant la liste des coups

                if len(D[turn]["ajout"])==len(D[turn]["retire"]) and len(D[turn]["ajout"])==1:
                    (x,y,c)=D[turn]["retire"][0]
                    index=get_last_index(liste_coups,(x,y,c))
                    print("index",index, "\n\n\n")
                    if index!=-1:
                        liste_coups[index]=D[turn]["ajout"][0]
                
                if len(D[notturn]["ajout"])==len(D[notturn]["retire"]) and len(D[notturn]["ajout"])==1:
                    (x,y,c)=D[notturn]["retire"][0]
                    index=get_last_index(liste_coups,(x,y,c))
                    if index!=-1:
                        liste_coups[index]=D[notturn]["ajout"][0]
        
    return liste_coups

#fichier=open("TenukiGo2/TenukiGo/Go-Game-Streaming-WebApp-main/partie_vs_organos _8k_.sgf", "r")

liste_tableaux=sgf_to_numpy("/home/luc/Documents/imt_atlantique/commande_entreprise/projet_go/TenukiGo2/TenukiGo/Go-Game-Streaming-WebApp-main/partie_vs_organos _8k_.sgf")

"""

Test sur un plateau sans erreurs : OK

"""

liste_coups=correcteur1(liste_tableaux)
print(liste_coups)
print("\n\n")

"""

Test en supprimant une frame (erreur liée à un coup rapide) : OK

"""

liste_tableaux=np.delete(liste_tableaux,2,0)
liste_coups=correcteur1(liste_tableaux)
print(liste_coups)
print("\n\n")

"""

Test en supprimant deux frames (erreur liée à des coup rapide ou a une ocultation) : 
L'ordre des coups perdu remis au hasard, on a une inversion des premiers coups

"""

liste_tableaux=np.delete(liste_tableaux,2,0)

liste_coups=correcteur1(liste_tableaux)
print(liste_coups)
print("\n\n")



# On modifie le premier coup de blanc (simulation de déplacement de pierre)
liste_tableaux=sgf_to_numpy("/home/luc/Documents/imt_atlantique/commande_entreprise/projet_go/TenukiGo2/TenukiGo/Go-Game-Streaming-WebApp-main/partie_vs_organos _8k_.sgf")

tab=np.copy(liste_tableaux[2])
tab[15,3]=0
tab[15,4]=2

liste_tableaux=np.insert(liste_tableaux,3,tab,0)

print(liste_tableaux[2])
print(liste_tableaux[3])

liste_coups=correcteur1(liste_tableaux)
print(liste_coups)
print("\n\n")



    



                

   

            
            

            

















