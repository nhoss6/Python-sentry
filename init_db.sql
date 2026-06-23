CREATE DATABASE IF NOT EXISTS magasin;

USE magasin;

CREATE TABLE IF NOT EXISTS produits (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  prix DECIMAL(10,2) NOT NULL,
  stock INT NOT NULL
);

INSERT INTO produits (nom, prix, stock) VALUES
('Clavier', 49.99, 10),
('Souris', 19.99, 25),
('Écran', 149.99, 8);
