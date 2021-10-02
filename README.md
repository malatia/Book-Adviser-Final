# Book-Adviser-Final

Ceci est un projet mettant en oeuvre des systèmes de recommendation grâce à des algorithmes d'intelligence artificielle.
Il a été réalisé dans le cadre de la promotion 2021 de Développeur en IA par Simplon de Cannes. 
Ce projet s'appuie sur des livres ayant été noté par des utilisateurs du site goodreads. 
On peut y trouver à la fois : 
- un algorithme "Content based" basé sur les tags mis par les utilisateurs aux différents livres
- et un "Collaborative Filtering" basé sur les notes attribuées aux livres par les utilisateurs

## Dépendances 

Pour les dépendances il suffit de lancer la commande ``pip install -r requirements.txt``

## Pour la base de données

Pour installer la base de données, il faut exécuter le script "script_bdd.sql" sur MySQL-Workbench ou directement MySql,
ce qui permettras la création de la structure de la base de données.

Pour insérer les données dans la table il faut exécuter le script "nettoyage_insertion_donnees.ipynb", 
mettre ses identifiant de base de données dans la première cellule et ensuite executer le programme 
(une seule fois seulement sous peine d'écrire plusieurs fois dans la base de données).

Bien pensé à executer la commande SQL "SET GLOBAL FOREIGN_KEY_CHECKS=1;" après l'insertion des données pour rétablir le chek des clef étrangères.

## Lancement rapide

Il faut télécharger le modèle entraîné car il est trop gros pour aller sur github.  
Vous pourrez le trouver à cette adresse : https://www.transfernow.net/dl/20211002R6jcX8rO  
Il suffira ensuite de créer un dossier "Models" à la racine, et de mettre le fichier téléchargé à l'intérieur.  
Une fois ceci fait et les dépendances installées, il suffit de lancer le fichier "main.py" et de suivre les instructions de la console!  

## Explication des fichiers 

"script_bdd.sql" est le script sql de la structure de la base de données
"nettoyage_insertion_donnees.ipynb" est le script python (jupyter) de l'insertion des données dans la base de données
Le compte rendu est ... comme son nom l'indique notre compte rendu!
Les fichiers de dossier "Data" y sont décrits. 
