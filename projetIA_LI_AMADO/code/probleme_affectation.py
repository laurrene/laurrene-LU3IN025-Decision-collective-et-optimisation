from collections import deque

    #PROBLEME ET AFFECTATION

    #Q.1

# Fonction qui génère une matrice de préférences de parcours des étudiants 
def matrice_etu(fichier):
    """
    Lit un fichier contenant les préférences des étudiants et retourne une matrice de préférences.
    
    Args :
        fichier (str): le chemin du fichier 
    
    Return :
        list: une matrice où chaque ligne correspond aux préférences d'un étudiant.
    """
    # lecture du fichier
    f = open(fichier,"r")
    contenu= f.readlines()     
    f.close()

    # séparation des lignes en éléments
    mots = []
    for i in range (1,len(contenu)): # ignore la première ligne (nombre d'étudiants)
        mots.append(contenu[i].split("\t"))

    # mise en forme de la matrice en ignorant les 2 premiers éléments (identifiants)
    matrice =[]
    for j in range(0, len(mots)): 
        matrice.append(mots[j][2:])
    
    # conversion de chaines de caractères en entiers
    for i in range(0,len(matrice)):
        for j in range (0,len(matrice[i])):
            matrice[i][j] = int(matrice[i][j])
    return matrice


# Fonction qui génère une matrice de préférences d'étudiants des parcours à partir d'un fichier
def matrice_spe(fichier):
    """
    Lit un fichier contenant les préférences des parcours et retourne une matrice de préférences.
    
    Args :
        fichier (str): le chemin du fichier 
    
    Return :
        list: une matrice où chaque ligne correspond aux préférences d'un parcours.
    """
    # lecture du fichier
    f = open(fichier,"r")
    contenu= f.readlines()     
    f.close()

    # séparation des lignes en éléments
    mots = []
    for i in range (2,len(contenu)): # ignore les 2 lignes (nombre d'étudiants et capacités)
        mots.append(contenu[i].split("\t"))
    
    # mise en forme de la matrice en ignorant les 2 premiers éléments (identifiants
    matrice =[]
    for j in range(0, len(mots)):
        matrice.append(mots[j][2:])
    
    # conversion de chaines de caractères en entiers
    for i in range(0,len(matrice)):
        for j in range (0,len(matrice[i])):
            matrice[i][j] = int(matrice[i][j])
    return matrice

# Fonction pour définir les capacités des parcours à partir d'un fichier
def capacite_spe(fichier):
    """
    Lit un fichier et retourne une liste des capacités d'accueil des parcours.
    Args:
        fichier (str): le chemin du fichier 

    Return:
        list: une liste des capacités des parcours.
    
    """
    # lecture du fichier
    f = open(fichier,"r")
    contenu= f.readlines()     
    f.close()

    # extraction des capacités (2e ligne du fichier)
    cap = []
    mots = contenu[1].split(" ")
    for i in range(1,len(mots)): #ignorer le premier élément (nom de la colonne)
        cap.append(int(mots[i])) 
    return cap 
 
#Q.3
# Fonction pour appliquer l'algorithme de Gale Shapley coté étudiant
def gale_shapley_ce(ce, cp, cap):
    """
    Algorithme de Gale-Shapley côté étudiants.

    Args:
        ce (list): matrice des préférences des étudiants.
        cp (list): matrice des préférences des parcours.
        cap (list): liste des capacités des parcours.

    Return:
        list: Une liste de tuples (étudiant, [parcours affecté]).
    """
      
    libre = deque(range(len(ce))) #file des étudiants libres (initialement tous libres)
    proposition = [0] * len(ce)   # nombre de propositions envoyées par chaque étudiant
    affectations = {} # dictionnaire des affectations {étudiant: parcours}
    
    prefEtuIndices = [{etu: id for id, etu in enumerate(prefs)} for prefs in cp]
    parcours_affectes = [[] for _ in range(len(cp))]

    iteration = 0

    while libre:
        iteration += 1
        etu_libre = libre.popleft()  #extraire le 1er étudiant libre
        
        spe = ce[etu_libre][proposition[etu_libre]]  # parcours le plus préféré non encore propososé
       
        proposition[etu_libre] += 1 
                
        
        if cap[spe] > 0: #reste des places dans le parcours
            affectations[etu_libre] = spe  # affecte l'étudiant
            parcours_affectes[spe].append(etu_libre)
            cap[spe] -= 1 
           
            
        else:
            
            etu_affecte =parcours_affectes[spe][0] 
          
            # vérifie la préférence du parcours
            if prefEtuIndices[spe][etu_libre] < prefEtuIndices[spe][etu_affecte]:
                affectations.pop(etu_affecte) #enleve l'ancian étudiant
                affectations[etu_libre] = spe #ajoute l'étudiant libre
                libre.appendleft(etu_affecte) #mettre l'ancian étudiant dans la liste de étudiants libres
                parcours_affectes[spe][0] = etu_libre
            else:
                libre.appendleft(etu_libre) #étudiant reste libre
   
    return sorted((k, [v]) for k, v in affectations.items()),iteration

#Q.4
# Fonction pour appliquer l'algorithme de Gale Shapley coté parcours
def gale_shapley_cp(ce, cp, cap):
    """
    Algorithme de Gale-Shapley côté parcours.

    Args:
        ce (list): matrice des préférences des étudiants.
        cp (list): matrice des préférences des parcours.
        cap (list): liste des capacités des parcours.

    Returns:
        list: une liste de tuples (parcours, [étudiants affectés]).
    """
    deja_prise = set()  #étudiants déja affectés
    proposition = [0] * len(cp)  # nombre de propositions envoyées par chaque parcours
    affectations = {}  # {parcours: [étudiants]}
    etu_affecte_par = {}   # {étudiant: parcours}

    parcours_libres = deque([i for i, x in enumerate(cap) if x > 0])  # file des parcours ayant de places

    iteration = 0
    while parcours_libres:
        iteration += 1
        parcours_libre = parcours_libres.popleft()  # extraire le 1er parcours libre
        etu = cp[parcours_libre][proposition[parcours_libre]] # etudiant le plus préféré non encore propososé
        proposition[parcours_libre] += 1  

        if cap[parcours_libre] > 0 and etu not in deja_prise:
            affectations.setdefault(parcours_libre, []).append(etu)
            deja_prise.add(etu)
            etu_affecte_par[etu] = parcours_libre
            cap[parcours_libre] -= 1

        else:  

            if etu in etu_affecte_par:
                parcours_affecte = etu_affecte_par[etu]   # parcours actuel de l'étudiant

                #vérifie les préférences
                if ce[etu].index(parcours_libre) < ce[etu].index(parcours_affecte):
                    affectations[parcours_affecte].remove(etu)  
                    cap[parcours_affecte] += 1  
                    parcours_libres.append(parcours_affecte)

                    affectations.setdefault(parcours_libre, []).append(etu)
                    etu_affecte_par[etu] = parcours_libre  
                    cap[parcours_libre] -= 1      
                        
        if cap[parcours_libre] > 0:
            parcours_libres.append(parcours_libre)  

    return sorted(affectations.items()),iteration


#Q.6     
# Fonction qui recherche les paires instables dans un mariage
def paires_instables(mariage, cote_h, cote_f):
    """
    Détecte les paires instables dans un mariage donné en comparant les préférences des hommes et des femmes.

    Args:
        mariage (list): Liste de tuples (homme, [femme]) représentant le mariage.
        cote_h (list): Matrice des préférences des hommes.
        cote_f (list): Matrice des préférences des femmes.

    Return:
        set: Ensemble des paires instables.
    """
    instables = set() # ensemple pour les paires instables
    
    dict = {h: f[0] for h, f in mariage}  # transforme le mariage en dictionnaire

    # parcours chaque homme et sa femme actuelle dans le mariage
    for h_actuel, liste_f_actuel in mariage:

        for i in range (len(liste_f_actuel)):
            f_actuelle = liste_f_actuel[i]  
            
            indice_f_actuel = cote_h[h_actuel].index(f_actuelle) # indice de la femme actuelle dans les préférences de l'homme
            femmes_plus_pref = cote_h[h_actuel][:indice_f_actuel] # liste des femmes que l'homme préfère à sa femme actuelle
            
            # parcours chaque femme préférée par l'homme
            for f_pref in femmes_plus_pref:
                
                h_affecte = next((h for h, f in dict.items() if f == f_pref), None) # homme actuellement marié à cette femme préférée
                
                if h_affecte is not None:
                    
                    indice_h_affecte = cote_f[f_pref].index(h_affecte) # indice de l'homme actuel dans les préférences de la femme 
                    hommes_plus_pref = cote_f[f_pref][:indice_h_affecte] # liste des hommes que la femme préfère à son mari actuel
                    
                    # si l'homme actuel est préféré par la femme, la paire est instable
                    if h_actuel in hommes_plus_pref:
                        instables.add((h_actuel, f_pref))
    
    return instables


