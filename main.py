import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity




def nouvelUtilisateur(cos_sim, new_book_tags):
    """Cette fonction recommende des livres en fonction des centre d'intérêts de l'utilisateur ou des livres qu'il a déjà pu lire.
    Cependant, vu que l'on considère ici que c'est un nouvel utilisateur, on peut imaginer que dans la version finale on lui demandera
    ses préférences de genre ou les livres qu'il a lu, en lui proposant parmi une liste.
    Pour le moment, nous allons simplement partir du principe que l'utilisateur indique avoir lu "Harry Potter and the Philosopher's Stone"

    Args:
        cos_sim (numpy.ndarray): Matrice contenant les poids pour calculer les similarités
        new_book_tags(DataFrame) : DataFrame contenant les infos sur la base de livres

    Returns:
    [DataFrame]: Retourne un DataFrame contenant des infos sur les 10 livres les plus adaptés d'après l'algorithme
    
    """
    #Le chiffre 3 correspond ici à l'index du livre "Harry Potter and the Philosopher's Stone"
    harry_id = 3
    harry_recommendation = np.argsort(cos_sim[harry_id])
    harry_top10 = harry_recommendation[-10:][::-1]
    print("Nous partons du principe que le nouvel utilisateur dit avoir lu le premier des Harry Potter")
    return new_book_tags.iloc[harry_top10]


def ancienUtilisateur(cos_sim):
    """[summary]

    Args:
        cos_sim ([type]): [description]

    Returns:
        [type]: [description]
    """
    print(cos_sim)

def main():
    #On calcule la cosine_similarity quand on load le document
    new_book_tags_onehot = pd.read_csv("CSV/new_book_tags_onehot.csv")
    cos_sim = cosine_similarity(new_book_tags_onehot.iloc[:,5:])
    new_book_tags = pd.read_csv("CSV/new_book_tags.csv")

    #On vérifie si l'utilisateur est nouveau ou pas
    utilisateur = 0
    while utilisateur not in [1,2]:             
        utilisateur = int(input("Bonjour, tapez 1 si vous êtes un nouvel utilisateur, tapez 2 sinon : "))
        if utilisateur == 1:
            recommendations = nouvelUtilisateur(cos_sim, new_book_tags)
            print(recommendations)
        elif utilisateur == 2:
            ancienUtilisateur(cos_sim)
        else :
            print("Mauvaise entrée")

    

if __name__ == '__main__':
    main()