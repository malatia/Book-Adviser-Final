CREATE DATABASE IF NOT EXISTS reco_livre CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE reco_livre;

CREATE TABLE IF NOT EXISTS reco_livre.tags ( 
  tag_id INT AUTO_INCREMENT NOT NULL UNIQUE,
  tag_name VARCHAR(100) NOT NULL,
  PRIMARY KEY (tag_id));
  
CREATE TABLE IF NOT EXISTS reco_livre.books (
	book_id INT AUTO_INCREMENT NOT NULL UNIQUE,
    goodreads_book_id INT NOT NULL UNIQUE,
    best_book_id INT NOT NULL,
    work_id INT NOT NULL,
    books_count INT NOT NULL,
    isbn VARCHAR(15) NULL,
    isbn13 VARCHAR(30) NULL,
    authors TEXT NOT NULL,
    original_publication_year FLOAT NULL,
    original_title VARCHAR(255) NULL,
    title VARCHAR(255) NOT NULL,
    language_code VARCHAR(20) NULL,
    average_rating FLOAT NOT NULL,
    ratings_count INT NOT NULL,
    work_ratings_count INT NOT NULL,
    work_text_reviews_count INT NOT NULL,
    ratings_1 INT NOT NULL,
    ratings_2 INT NOT NULL,
    ratings_3 INT NOT NULL,
    ratings_4 INT NOT NULL,
    ratings_5 INT NOT NULL,
    image_url VARCHAR(150) NOT NULL,
    small_image_url VARCHAR(150) NOT NULL,
    PRIMARY KEY (book_id));


CREATE TABLE IF NOT EXISTS reco_livre.ratings (
	ratings_id INT AUTO_INCREMENT NOT NULL UNIQUE,
	user_id INT NOT NULL,
    book_id INT NOT NULL,
    rating INT NOT NULL,
    PRIMARY KEY (ratings_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id));
    
    
CREATE TABLE IF NOT EXISTS reco_livre.to_read (
  to_read_id INT AUTO_INCREMENT NOT NULL UNIQUE,
  user_id INT NOT NULL,
  book_id INT NOT NULL,
  PRIMARY KEY (to_read_id),
  FOREIGN KEY (book_id) REFERENCES books(book_id));
  
  
CREATE TABLE IF NOT EXISTS reco_livre.book_tags (
	tag_id INT NOT NULL,
	book_id INT NOT NULL,
    count INT NOT NULL,
    CONSTRAINT book_tags_pk PRIMARY KEY (tag_id, book_id), 
    CONSTRAINT books_book_tags_fk FOREIGN KEY (tag_id) REFERENCES tags (tag_id),
    CONSTRAINT book_tags_books_fk FOREIGN KEY (book_id) REFERENCES books (book_id));
  
    
    
SET GLOBAL FOREIGN_KEY_CHECKS=0;

