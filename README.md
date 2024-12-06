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
- [Contributions](#contributions)
- [Licence](#licence)

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
