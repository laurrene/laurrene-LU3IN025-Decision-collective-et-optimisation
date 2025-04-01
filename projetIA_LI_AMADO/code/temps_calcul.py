import time
import numpy as np
import matplotlib.pyplot as plt

from probleme_affectation import *

        #Evolution du temps de calcul

    #Q.7

# Fonction pour générer une matrice des préférences de parcours des étudiants
def genere_mat_etu(n,spe=9):
    """
    Génère une matrice de préférences pour n étudiants.
    Chaque étudiant a une liste de préférences aléatoires pour les spe parcours.
    
    Args:
        n (int): Nombre d'étudiants.
        spe (int): Nombre de parcours (par défaut 9).

    Return:
        list: Une matrice de préférences des étudiants.
    """
    mat=[]
    for _ in range (n):
        liste_pref=np.arange(spe) # crée une liste de 0 à spe-1
        np.random.shuffle(liste_pref) # mélange la liste pour avoir des préférences aléatoires
        mat.append(liste_pref.tolist()) # ajoute la liste mélangée à la matrice
            
    return mat

# Fonction pour générer une matrice de préférences d'étudiants des parcours
def genere_mat_spe(n,spe=9):
    """
    Génère une matrice de préférences pour spe parcours.
    Chaque parcours a une liste de préférences aléatoires pour les n étudiants.
    
    Args:
        n (int): Nombre d'étudiants.
        spe (int): Nombre de parcours (par défaut 9).

    Returns:
        list: Une matrice de préférences des parcours.
    
    """
    mat=[]
    for _ in range (spe): 
        liste_pref=np.arange(n) # crée une liste de 0 à n-1
        np.random.shuffle(liste_pref)  # mélange la liste pour avoir des préférences aléatoires
        mat.append(liste_pref.tolist()) # ajoute la liste mélangée à la matrice
            
    return mat

    #Q.8

# Fonction pour définir les capacités des parcours
def capacite(n):
    """
    Définit la capacité de chaque parcours en fonction du nombre d'étudiants n.
    La capacité est répartie équitablement entre les 9 parcours.
    
    Args:
        n (int): Nombre d'étudiants.

    Return:
        list: Une liste des capacités des parcours.
    """
    nb = n//9 # capacité de base pour chaque parcours
    
    cap = [nb] * 9 # liste des capacités initialisées avec la capacité de base
    reste = n%9 # reste à répartir
   
    for i in range(reste): #répartit le reste dans la liste des capacités
        cap[i] +=1

    return cap

# Fonction pour mesurer les temps d'exécution des algorithmes de Gale Shapley 
def temps(nb_test=10):
    """
    Mesure le temps moyen d'exécution et le nombre d'itérations moyens des algorithmes GS étudiants et GS parcours
    pour différentes valeurs de n (nombre d'étudiants).
    
    Args:
        nb_test (int): Nombre de tests à effectuer pour chaque valeur de n (par défaut 10).

    Return:
        tuple: Deux listes contenant les temps moyens d'exécution pour GS étudiants et GS parcours.
    """
    tps_ce = 0 # temps total pour GS étudiants
    tps_cp = 0 # temps total pour GS parcours
    iter_ce = 0  # nombre total d'itérations pour GS étudiants
    iter_cp = 0  # nombre total d'itérations pour GS parcours

    t_moy_ce=[] # liste pour stocker les temps moyens de GS étudiants
    t_moy_cp=[] # liste pour stocker les temps moyens de GS parcours
    iter_moy_ce = []  # liste pour stocker les nombres moyens d'itérations de GS étudiants
    iter_moy_cp = []  # liste pour stocker les nombres moyens d'itérations de GS parcours

    # teste GS avec différents valeurs de n
    for n in range(200,2001,200):

        # génère des matrices de préférences
        mat_etu = genere_mat_etu(n)
        mat_spe = genere_mat_spe(n)

        # répétition de nb_test pour avoir une moyenne de temps
        for _ in range(nb_test):

            #calcul des capacités
            cap = capacite(n)

            tps_ce = 0 # temps total pour GS étudiants
            tps_cp = 0 # temps total pour GS parcours
            iter_ce = 0  # nombre total d'itérations pour GS étudiants
            iter_cp = 0  # nombre total d'itérations pour GS parcours
            
            # mesure le temps pour GS étudiants
            debut_ce = time.perf_counter()
            _,iterations_ce = gale_shapley_ce(mat_etu, mat_spe, cap.copy())
            fin_ce = time.perf_counter()
            tps_ce += fin_ce - debut_ce
            iter_ce += iterations_ce
            

            # mesure le temps pour GS parcours
            debut_spe = time.perf_counter()
            _,iterations_cp = gale_shapley_cp(mat_etu,mat_spe,cap.copy())
            fin_spe = time.perf_counter()
            tps_cp += fin_spe-debut_spe
            iter_cp += iterations_cp
            

        # calcul des temps moyens et ajout aux listes
        t_moy_ce.append(tps_ce/nb_test)
        t_moy_cp.append(tps_cp/nb_test)
        iter_moy_ce.append(iter_ce / nb_test)
        iter_moy_cp.append(iter_cp / nb_test)

    return t_moy_ce,t_moy_cp,iter_moy_ce, iter_moy_cp

# Fonction pour tracer les graphiques des temps d'exécution
def graphe_tps():
    """
    Trace deux graphiques montrant l'évolution du temps de calcul
    pour GS étudiants et GS parcours en fonction du nombre d'étudiants.
    """
    x = range(200, 2001, 200)
    t_ce, t_cp, iter_moy_ce, iter_moy_cp = temps()

    # création de la figure et des sous-graphiques
    plt.figure(figsize=(12, 5))

    # premier graphique : GS étudiants (temps)
    plt.subplot(1, 2, 1)
    plt.plot(x, t_ce, label="GS étudiants", color='blue')
    plt.xlabel("Nombre d'étudiants (n)")
    plt.ylabel("Temps de calcul (s)")
    plt.title("Temps de calcul pour GS Étudiants")
    plt.legend()

    # deuxième graphique : GS parcours (temps)
    plt.subplot(1, 2, 2)
    plt.plot(x, t_cp, label="GS parcours", color='red')
    plt.xlabel("Nombre d'étudiants (n)")
    plt.ylabel("Temps de calcul (s)")
    plt.title("Temps de calcul pour GS Parcours")
    plt.legend()

    # affiche les graphiques
    plt.tight_layout()
    #plt.show()

graphe_tps()

# Fonction pour tracer les graphiques de nombres ditérations
def graphe_it():
    """
    Trace deux graphiques montrant l'évolution du nombre d'itérations
    pour GS étudiants et GS parcours en fonction du nombre d'étudiants.
    """
    x = range(200, 2001, 200)
    t_ce, t_cp, iter_moy_ce, iter_moy_cp = temps()

    # création de la figure et des sous-graphiques
    plt.figure(figsize=(12, 5))

    # premier graphique : GS étudiants (itérations)
    plt.subplot(1, 2, 1)
    plt.plot(x, iter_moy_ce, label="GS étudiants", color='blue')
    plt.xlabel("Nombre d'étudiants (n)")
    plt.ylabel("Nombre d'itérations")
    plt.title("Nombre d'itérations pour GS Étudiants")
    plt.legend()

    # deuxième graphique : GS parcours (itérations)
    plt.subplot(1, 2, 2)
    plt.plot(x, iter_moy_cp, label="GS parcours", color='red')
    plt.xlabel("Nombre d'étudiants (n)")
    plt.ylabel("Nombre d'itérations")
    plt.title("Nombre d'itérations pour GS Parcours")
    plt.legend()

    # affiche les graphiques
    plt.tight_layout()
    plt.show()

graphe_it()