import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from surprise import dump


new_book_tags_onehot = pd.read_csv("CSV/new_book_tags_onehot.csv")
books = pd.read_csv("CSV/books.csv")   
new_book_tags = pd.read_csv("CSV/new_book_tags.csv")
#preds_df = pd.read_csv("CSV/preds_df.csv")
#ratings = pd.read_csv("CSV/ratings.csv")


def recommend_books_SVD(user_id, num_recommendations=100):
    #Ordonner les prédictions pour l'utilisateur donné
    #sorted_user_predictions = preds_df.iloc[user_id].sort_values(ascending=False)
    #user_data = ratings[ratings["user_id"] == user_id]
    #non_read_books = books[~books['book_id'].isin(user_data['book_id'])]
    #non_read_books = non_read_books.merge(sorted_user_predictions, how="left", on="book_id")
    #non_read_books.rename(columns={user_id : "Predictions"}, inplace=True)
    #non_read_books = non_read_books[["book_id", "goodreads_book_id", "original_title", "Predictions"]]
    #non_read_books = non_read_books.sort_values("Predictions", ascending=False)
    #non_read_books_recommendations = non_read_books[:num_recommendations]
    
    #return non_read_books_recommendations
    return "Ok"

def nouvelUtilisateur(cos_sim, book_id = 3):
    """Cette fonction recommende des livres en fonction des centre d'intérêts de l'utilisateur ou des livres qu'il a déjà pu lire.
    Cependant, vu que l'on considère ici que c'est un nouvel utilisateur, on peut imaginer que dans la version finale on lui demandera
    ses préférences de genre ou les livres qu'il a lu, en lui proposant parmi une liste.
    Pour le moment, nous allons simplement partir du principe que l'utilisateur indique avoir lu "Harry Potter and the Philosopher's Stone"
    et gardons donc la valeur par défaut pour "book_id"

    Args:
        cos_sim (numpy.ndarray): Matrice contenant les poids pour calculer les similarités
        new_book_tags(DataFrame) : DataFrame contenant les infos sur la base de livres
        book_id (int, optional): L'id du livre dont on veut les recommendations. On le met par défaut à l'id du premier livre Harry Potter

    Returns:
    [DataFrame]: Retourne un DataFrame contenant des infos sur les 10 livres les plus adaptés d'après l'algorithme
    
    """
    #On calcule ici les livres les plus proches de celui demandé 
    book_recommendation = np.argsort(cos_sim[book_id])
    book_top10 = book_recommendation[-10:][::-1]
    print("Nous partons du principe que le nouvel utilisateur dit avoir lu le premier des Harry Potter")
    return new_book_tags.iloc[book_top10]


def ancienUtilisateur(cos_sim, user_id):

    return "ok"

def main():
    #On calcule la cosine_similarity quand on load le document    
    cos_sim = cosine_similarity(new_book_tags_onehot.iloc[:,5:])
 

    #On vérifie si l'utilisateur est nouveau ou pas
    utilisateur = 0
    while utilisateur not in [1,2]:
        utilisateur = int(input("Bonjour, tapez 1 si vous êtes un nouvel utilisateur, tapez 2 sinon : "))
        if utilisateur == 1:
            recommendations = nouvelUtilisateur(cos_sim, new_book_tags)
            print(recommendations)
        elif utilisateur == 2:
            recommend_books_SVD(1)
            #ancienUtilisateur(cos_sim, 42)
        else :
            print("Mauvaise entrée")

    

if __name__ == '__main__':
    main()