import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from surprise import dump


#On charge ici en mémoire les données dont on va avoir besoin pour recommender des modèles 

print("Chargement des CSV")
books = pd.read_csv("CSV/books.csv")
ratings = pd.read_csv("CSV/ratings.csv")   
new_book_tags = pd.read_csv("CSV/new_book_tags.csv")
print("Chargement des CSV fini")

print("Chargement des modèles")
_, KNN_with_means = dump.load("Models/KNNWithMeans")
cv = CountVectorizer()
count_matrix = cv.fit_transform(new_book_tags["tag_concat"])
cos_sim = cosine_similarity(count_matrix)
print("Chargement des modèles fini")

def collaborative_generation(user_id, num_recommendations=100):
    """Cette fonction génère des candidats et de les ordonner pour un système de recommendation grâce à du collaborative filtering

    Args:
        user_id (int): L'id de l'utilisateur pour lequel on veut faire des prédictions
        num_recommendations (int, optional): Le nombre de candidats à générer. Defaults to 100.

    Returns:
        [DataFrame]: Un DataFrame donnant les IDs, titre, et note prédite pour chacun des candidats
    """
    #Le dictionnaire qui permettra de récupérer les notes prédites dans un premier temps 
    predictions = {}
    #On détermine quels sont les livres qui n'ont pas été lus par l'utilisateur
    user_data = ratings[ratings["user_id"] == user_id]
    non_read_books = books[~books['book_id'].isin(user_data['book_id'])]
    #On fait une prédiction pour chacun de ces livres pour cet utilisateur 
    for book_id in non_read_books["book_id"].values:
        predictions[book_id] = KNN_with_means.predict(user_id,book_id).est

    #On va faire un DataFrame du dictionnaire de prédictions
    predictions_df = pd.DataFrame.from_dict(predictions, orient="index", columns=["prediction"])
    predictions_df.reset_index(drop=False, inplace=True)
    #On merge les dataframes pour avoir un rendu qui nous donne le titre et les ID du film
    non_read_books = non_read_books.merge(predictions_df, how="left", left_on="book_id", right_on="index")
    non_read_books = non_read_books[["book_id", "goodreads_book_id", "original_title", "prediction"]]
    #Et on récupère autant de candidats que demandé 
    non_read_books = non_read_books.sort_values("prediction", ascending=False)
    non_read_books_recommendations = non_read_books[:num_recommendations]

    return non_read_books_recommendations

def content_based_generation(book_id):
    """Cette fonction génère des scores de similarité entre un livre donné et tous les autres en fonction de leurs tags.

    Args:
        book_id (int): L'ID du livre dont on veut trouver les semblables 

    Returns:
        [DataFrame]: Un DataFrame contenant les livres du jeu de données avec une colonne "similarity" se référant au livre qui nous intéresse 
    """
    #On récupère l'index du livre grâce à son ID
    book_id_index = new_book_tags[new_book_tags["book_id"] == book_id].index
    #On calcule les similarités entre le livre donné et les autres
    similar_movies = list(enumerate(cos_sim[book_id_index[0]]))
    list_similarities = [element[1] for element in similar_movies]
    #On les ajoute dans une colonne "similarity"
    similar_df = new_book_tags.copy()
    similar_df["similarity"] = list_similarities
    
    return similar_df

def user_content_based_generation(user_id, note_threshold=2):
    """Cette fonction prend les livres qu'un utilisateur a noté au delà du seuil donné et crée des scores de similarités entre ces livres et tous les autres du jeu de données.


    Args:
        user_id (int): L'id de l'utilisateur pour lequel on veut générer des résultats 
        note_threshold (int) : Le seuil au delà duquel on considère que la note est "bonne" et qui nous permet de décider quel livre prendre
        
    Returns:
        [DataFrame]: Le DataFrame avec les recommendations
    """
    #On regarde quels sont les livres lus par l'utilisateur, et nous ceux qui ont été noté au dessus du seuil
    user_data = ratings[ratings["user_id"] == user_id]
    books_for_content_based = user_data[user_data["rating"] > note_threshold]
    list_df = []

    #Pour chacun de ces livres, on calcule les scores de similarités
    for book_id in books_for_content_based.book_id.values:
        df = content_based_generation(book_id)
        list_df.append(df)

    #On concatène les dataframes qui résultent de cette génération 
    new_df = pd.concat(list_df)
    #on groupe par livre, et on fait la moyenne des similarités obtenues 
    new_df = new_df.groupby("book_id").agg({"similarity" : "mean"})
    new_df.reset_index(inplace=True)

    return new_df

def merge_recommendations(content_based, collaborative, content_importance=2.0):
    """Cette fonction permet de merger deux dataframes, un content based et un collaborative, et en donne la note finale

    Args:
        content_based ([DataFrame]): DataFrame provenant de la fonction user_content_based_generation
        collaborative ([DataFrame]): DataFrame provenant de la fonction collaborative_generation
        content_importance (float, optional): L'importance que l'on voudra donner au score de similarité. Pour comparaison, la note prédite pour le collaboratif a une importance de 5. Defaults to 2.0.


    Returns:
        [DataFrame]: DataFrame comprenant les recommendations finales pour un utilisateur
    """
    #On merge les deux types de DataFrame sur le book_id, on ajoute les notes attribuées par et pour les deux systèmes en mettant la similarité à l'échelle de la valeur donnée
    recommendations_merges = collaborative.merge(content_based[["book_id", "similarity"]], how="left", on="book_id")
    recommendations_merges["similarity"] = recommendations_merges["similarity"] * content_importance
    final_note = recommendations_merges["prediction"] + recommendations_merges["similarity"]
    recommendations_merges["final_note"] = final_note
    #Et pour finir on trie ce dataframe par la note finale obtenue S
    recommendations_merges.sort_values("final_note", ascending=False, inplace=True)
    return recommendations_merges

def nouvelUtilisateur():
    """Cette fonction s'adresse à un nouvel utilisateur et lui demande un livre qu'il a pu apprécier pour commencer à lui recommander des livres
    similaires

    Returns:
        [DataFrame]: Un DataFrame contenant des recommendations pour cet utilisateur en fonction du livre indiqué
    """

    book_id = input("Veuillez indiquer l'ID d'un livre que vous avez lu ou qui pourrait vous intéresser (l'ID 1 correspond au premier livre Hunger Games pour le test) : ")
    books_with_similarities = content_based_generation(int(book_id))
    books_with_similarities.sort_values("similarity", ascending=False, inplace=True)
    return books_with_similarities[:15]


def ancienUtilisateur(user_id):

    collaborative_candidates = collaborative_generation(user_id)
    content_based_candidates = user_content_based_generation(user_id)
    recommendations = merge_recommendations(content_based_candidates, collaborative_candidates)
    return recommendations

def main():
    #On vérifie si l'utilisateur est nouveau ou pas
    utilisateur = 0
    while utilisateur not in [1,2]:
        utilisateur = int(input("Bonjour, tapez 1 si vous êtes un nouvel utilisateur, tapez 2 sinon : "))
        if utilisateur == 1:
            recommendations = nouvelUtilisateur()
            print(recommendations[:15])

        elif utilisateur == 2:
            user_id = input("Veuillez entrer votre ID utilisateur(pour le test, 49348 est un utilisateur qui aime les livres pour enfant, et l'heroic fantasy pour les jeunes ados, il a par exemple lu et bien noté Hunger Games)")
            recommendations = ancienUtilisateur(int(user_id))
            print(recommendations[:15])
        else :
            print("Mauvaise entrée")

if __name__ == '__main__':
    main()

