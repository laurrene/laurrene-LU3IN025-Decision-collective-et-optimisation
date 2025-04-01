import unittest
from probleme_affectation import *
from temps_calcul import *

class Test(unittest.TestCase):

    def test_matrice_etu(self):
        ce = matrice_etu("PrefEtu.txt")
        mat_e = [[5, 7, 6, 8, 3, 2, 0, 1, 4], 
                 [6, 5, 0, 4, 7, 2, 8, 3, 1], 
                 [4, 0, 7, 2, 8, 3, 1, 6, 5], 
                 [6, 5, 7, 0, 8, 4, 3, 1, 2], 
                 [1, 6, 7, 5, 0, 2, 4, 8, 3], 
                 [0, 7, 4, 2, 8, 3, 1, 6, 5], 
                 [5, 7, 6, 2, 8, 3, 0, 1, 4], 
                 [7, 0, 4, 2, 8, 3, 1, 6, 5], 
                 [5, 7, 6, 2, 8, 3, 0, 1, 4], 
                 [2, 6, 5, 8, 3, 1, 4, 7, 0], 
                 [6, 4, 0, 8, 3, 1, 5, 2, 7]]
        self.assertEqual(ce, mat_e)
    
    def test_matrice_spe(self):
        cp = matrice_spe("PrefSpe.txt")
        mat_spe = [[7, 9, 5, 4, 3, 1, 0, 10, 6, 8, 2], 
                   [7, 5, 9, 4, 3, 1, 0, 10, 8, 6, 2], 
                   [3, 9, 5, 4, 7, 6, 1, 0, 10, 8, 2], 
                   [7, 9, 5, 4, 3, 1, 0, 6, 10, 8, 2], 
                   [10, 3, 0, 4, 5, 6, 7, 8, 9, 1, 2], 
                   [1, 0, 3, 4, 5, 6, 7, 2, 9, 10, 8], 
                   [0, 1, 3, 4, 5, 6, 7, 2, 8, 10, 9], 
                   [7, 6, 9, 5, 4, 3, 1, 0, 10, 8, 2], 
                   [1, 0, 3, 4, 5, 6, 7, 2, 9, 10, 8]]
        self.assertEqual(cp, mat_spe)

    def test_capacite(self):
        cap = capacite_spe("PrefSpe.txt")
        res_attendu = [2, 1, 1, 1, 1, 1, 1, 1, 2]
        self.assertEqual(cap,res_attendu)
    
    #Q.5
    def test_gs(self):
        ce = matrice_etu("PrefEtu.txt")
        cp = matrice_spe("PrefSpe.txt")
        cap = capacite_spe("PrefSpe.txt")

        affect_ce, _ = gale_shapley_ce(ce,cp,cap.copy())
        res_attendu_ce =  [(0, [5]), (1, [6]), (2, [8]), (3, [0]), (4, [1]), (5, [0]), (6, [8]), (7, [7]), (8, [3]), (9, [2]), (10, [4])]

        affect_cp, _ = gale_shapley_cp(ce,cp,cap.copy())
        res_attendu_cp = [(0, [5, 3]), (1, [4]), (2, [9]), (3, [8]), (4, [10]), (5, [1]), (6, [0]), (7, [7]), (8, [6, 2])]

        self.assertEqual(affect_ce,res_attendu_ce)
        self.assertEqual(affect_cp,res_attendu_cp)

    def test_paires_instables_m_instable(self):
        matH = [[0,1,2],
                [1,0,2],
                [0,1,2]]
        
        matF = [[0,1,2],
                [0,1,2],
                [1,0,2]]
        
        mariage =  [(0, [2]), (1, [1]), (2, [0])]  # Mariage instable
        self.assertEqual(paires_instables(mariage, matH, matF), {(0, 1), (0, 0)})  # Aucun couple instable

    def test_paires_instables_gs(self):
        ce = matrice_etu("PrefEtu.txt")
        cp = matrice_spe("PrefSpe.txt")
        cap = capacite_spe("PrefSpe.txt")

        affect_ce,_ = gale_shapley_ce(ce,cp,cap.copy())
        affect_cp,_ = gale_shapley_cp(ce,cp,cap.copy())
        res_attendu_ce = paires_instables(affect_ce,ce,cp)
        res_attendu_cp = paires_instables(affect_cp,cp.copy(),ce)
        
        self.assertEqual(res_attendu_ce,set())
        self.assertEqual(res_attendu_cp,set())

    def test_genere_mat(self):
        print("\n===== TEST GENERE MATRICES =====")
        print(f"Génère une matrice de préférences de 5 étudiants sur les parcours : \n{genere_mat_etu(5)}")
        print(f"Génère une matrice de préférences des 9 parcours sur 5 étudiants  : \n{genere_mat_spe(5)}")
        print("==========================\n")

    def test_genere_cap(self):
        print("\n===== TEST GENERE CAP =====")
        print(f"Capacité de chaque parcours en fonction du nombre d'étudiants n: \n{capacite(5)}")
        print("==========================\n")

    def test_temps(self):
        print("\n===== TEST TEMPS =====")
        print(f"temps moyens de GS étudiants, temps moyens et nombres itérations de GS parcours sur 10 test: \n{temps()}")
        print("==========================\n")

if __name__ == '__main__':
    unittest.main()