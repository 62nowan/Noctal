# Noctal Blockchain
 
 **Noctal** est une implémentation simplifiée d'une blockchain en Python avec un explorateur blockchain via le module Flask.
 Ce projet s'inspire directement du mécanisme de consensus et de la structure de la chaîne du **Bitcoin**. Le consensus est basé sur l'**algorithme de preuve de travail (Proof-of-Work)**, 
 où les mineurs doivent résoudre des problèmes cryptographiques complexes pour valider de nouveaux blocs et les ajouter à la chaîne. Le processus de validation utilise une fonction de 
 hachage cryptographique (SHA-256) pour garantir l'intégrité des données de chaque bloc. Chaque bloc contient un hachage du bloc précédent, créant ainsi une chaîne de blocs sécurisée et 
 immuable. 

 En reprenant ce mécanisme, notre projet simule l'ajout de transactions dans un bloc, la recherche du bon "nonce" pour résoudre le problème cryptographique, et la gestion du consensus à 
 travers un réseau décentralisé d'acteurs. Cependant c'est un prototype très peu sécurisé et pour le moment non résistante aux attaques, le but étant d'essayer de reproduire fidèlement le 
 fonctionnement d'une blockchain POW.


## 📝 Table des matières

- [À propos](#À-propos)
- [Fonctionnalités](#fonctionnalités)
- [Technologies utilisées](#technologies-utilisées)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Versions](#versions)

---

## À propos

Ce projet vise à acquérir de l'expèrience mais aussi à démontrer le fonctionnement d'une blockchain en partant des bases : 
- Création et validation de blocs.
- Implémentation d'un consensus simple.
- Une interface web pour visualiser et interagir avec la blockchain.

## Fonctionnalités

- **Ajout de transactions** : Les utilisateurs peuvent soumettre des transactions via l'interface Flask.
- **Création de blocs** : Les mineurs peuvent valider et ajouter des blocs à la chaîne.
- **Exploration de la blockchain** : Les utilisateurs peuvent suivre l'état actuel de la blockchain via l'explorer.

## Technologies utilisées

- **Python** : Langage principal pour la logique de la blockchain.
- **Flask** : Framework web pour l'interface utilisateur.
- **HTML/CSS/JavaScript** : Pour l'interface utilisateur.
- **Fichiers python externes** : Pour les calculs crptographiques.
- **Bibliothèques Python** : 
  - `flask`
  - `hashlib`
  - `json`
  - `pycryptodome`
  - `configparser`
  - `...`

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- Python 3.7 ou supérieur
- Pip (gestionnaire de paquets Python)
- Un navigateur web
- Un IDE

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/shash64/Noctal.git
   cd Noctal

2. Créez un environnement virtuel et activez-le dans le terminal :
   ```bash
   python -m venv venv # Ou python3
   source env/bin/activate # (Sous Windows : .\env\Scripts\activate)

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt

## Utilisation

 1. Lancez le fichier account.py pour générer une clé privée et une clé publique :
    ```bash
    python account.py

 2. Ajoutez vos clés dans le fichier tx.py pour commencer pouvoir miner des blocks

 3. Commencer à miner à l'aide du fichier blockchain.py :
    ```bash
    python blockchain.py

 4. Vous pouvez accéder à l'explorateur via l'url :
    ```bash
    http://127.0.0.1:5900


## Versions

### Version actuelle

- **Version** : 1.2
- **Date** : Décembre 2024

**Changements majeurs** :
- Implémentation complète de la blockchain avec un mécanisme de consensus basé sur la preuve de travail (Proof-of-Work) inspiré de Bitcoin.
- Développement de l'interface utilisateur Flask permettant l'interaction avec la blockchain : ajout des pages de transactions, des détails de blocs et exploration complète de la chaîne.
- Mise en place des fondations du projet avec des commentaires et une structure de code plus claire.
- Création d'une ébauche d'un réseau P2P.
- Création d'un serveur local et traitement des requêtes
- Synchronisation des réquêtes et envoie du fichier json de la blockchain aux mineurs. (Problèmes de synchronisation du temps à résoudre)

### Versions précédentes

#### Version 1.1
- **Date** : Juin 2024

**Changements** :
- Prototype initial de la blockchain : minage des blocs, visualisation des blocs, visualisation des adresses,... 
- Première ébauche de l'interface utilisateur Flask pour la visualisation de la chaîne.
- Création du principe de transactions, de la memory pool, des transactions en attentes et supression des transactions dépensées.
- Creation du principe de signature des transactions et de verification.
- Implémentation des frais de transactions, modification autonome de la difficultée de minage et calcul de la taille des blocs

#### Version 1.0
- **Date** : Mars 2024

**Changements** :
- Création du dépôt et de la structure de base du projet.
- Implémentation d'un simple modèle de bloc dans un fichier json avec des fonctions de hachage basiques.
- Première version sans interface utilisateur, uniquement la logique de la blockchain en Python via le terminal.
- Implémentation des adresses ainsi que des clés privées et publique.
- Stockage des données sur le disque.

---




