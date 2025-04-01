from probleme_affectation import matrice_etu,matrice_spe,capacite_spe
import numpy as np

def plne_create(nom_file,ce,cp,cap_e,k=3):
    """Fonction qui crée un fichier .lp avec les condition du PLNE Q11"""
    if len(ce)==0 or len(cp)==0:
        return
    
    #Création de la matrice qui permet de savoir si un parcour fait partie des K premier choix d'un etudiant
    matrice = []
    for i in range(len(ce)):
        ligne = [0 for s in range(len(cp))]
        for j in range(k):
            ligne[ce[i][j]]=1
        matrice.append(ligne)
    monFichier=open(nom_file,"w")
    monFichier.write("Maximize\n")
    
    #On crée ici la fonction objectif qui est la somme de tous les marriages possible
    monFichier.write("obj : x0")
    for s in range(1,len(matrice[0])*len(matrice)):
        monFichier.write(" + x"+str(s))
    monFichier.write("\n")
    monFichier.write("st\n")
    
    #Création des conditions du PLNE pour que les etudiants n'est que les k premier choix
    for i in range(len(matrice)):
        first=True
        monFichier.write("c"+str(i+1)+": ")
        for j in range(len(matrice[i])):
            if matrice[i][j]==1:
                if not(first):
                    monFichier.write(" + ")
                first=False
                monFichier.write("x"+str(j+i*len(matrice[i])))
        monFichier.write(" = 1\n")
        
    #Créations des conditions pour que les parcours respectent leur capacite maximal
    for i in range(len(matrice[0])):
        first=True
        monFichier.write("c"+str(len(matrice)+i+1)+": ")
        for j in range(len(matrice)):
            if not(first):
                monFichier.write(" + ")
            first=False
            monFichier.write("x"+str(i+9*j))
        monFichier.write(" = "+str(cap_e[i])+"\n")

    #Création des conditions pour que les étudiants ne soient pas mis avec des parcours qui ne sont pas dans leur k premier choix
    for i in range(len(matrice)):
        if 0 in matrice[i]:
            first=True
            monFichier.write("c"+str(i+1+len(matrice)+len(matrice[0]))+": ")
            for j in range(len(matrice[i])):
                if matrice[i][j]==0:
                    if not(first):
                        monFichier.write(" + ")
                    first=False
                    monFichier.write("x"+str(j+i*len(matrice[i])))
            monFichier.write(" = 0\n")
    
    #Pour assuré que chaque variable ne soient égal a 0 ou 1
    monFichier.write("Binary\n")
    
    for s in range(0,len(matrice[0])*len(matrice[0])):
        monFichier.write("x"+str(s)+" ")

    monFichier.write("\n")
    monFichier.write("end")
    monFichier.close()

def utilite(ce,cp):
    """Fonction qui renvoie la matrice d'utilité Parcours/Etudiant"""
    matrice=np.zeros((11,9)).tolist()
    for i in range(len(ce)):
        for j in range(len(cp)):
            matrice[i][j]=(9-ce[i].index(j))+(11-cp[j].index(i))
    return matrice

def utilite_etu(ce):
    """Fonction qui renvoie la matrice d'utilité Etudiant"""
    matrice=np.zeros((11,9)).tolist()
    for i in range(len(ce)):
        for j in range(len(ce[0])):
            matrice[i][j]=(9-ce[i].index(j))
    return matrice

plne_create("plne.lp",matrice_etu("PrefEtu.txt"),matrice_spe("PrefSpe.txt"),capacite_spe("PrefSpe.txt"))