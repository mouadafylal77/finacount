# FINACOUNT — Guide de démarrage

## Contenu
- `app.py` : application interactive Streamlit
- `requirements.txt` : bibliothèques nécessaires

## Pré-requis
- Windows 10/11 64-bit
- Python 3.11 ou 3.12 recommandé

Téléchargement officiel de Python : https://www.python.org/downloads/windows/

Pendant l'installation, cochez **Add python.exe to PATH**.

## Lancer l'application sous Windows
1. Décompressez `FINACOUNT.zip` dans un dossier facile à retrouver, par exemple `Documents`.
2. Ouvrez le dossier `FINACOUNT`.
3. Cliquez sur la barre d'adresse de l'Explorateur de fichiers, tapez `cmd`, puis Entrée.
4. Dans la fenêtre noire, exécutez les commandes suivantes une par une :

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

5. Le navigateur devrait s'ouvrir automatiquement. Sinon, copiez l'adresse locale affichée dans le terminal (généralement `http://localhost:8501`).

## Utilisation
- **Dashboard** : indicateurs et graphique.
- **Gestion des revenus** : ajouter et modifier des opérations.
- **Contrôle IAS 18** : check-list pédagogique.
- **États financiers (IAS 1)** : compte de résultat simplifié et contrôle arithmétique du bilan.
- **Rapports & export** : télécharger les tableaux CSV et le rapport TXT.

## À savoir
- Les données de démonstration sont fictives.
- Les données saisies sont conservées pendant la session Streamlit, pas dans une base de données permanente.
- Le contrôle IAS 18 est une check-list simplifiée, pas une validation automatique de conformité.
- IAS 18 a été remplacée par IFRS 15 pour les exercices ouverts à compter du 1er janvier 2018. Si le cours demande IAS 18, conservez le module comme exercice historique et signalez ce point.
- IAS 1 sera remplacée par IFRS 18 pour les périodes annuelles ouvertes à compter du 1er janvier 2027. Vérifiez avec l'enseignant le référentiel attendu pour le projet.
- Ce prototype ne produit pas des états financiers certifiés et ne remplace pas un professionnel comptable.

## Dépannage
- Si `python` n'est pas reconnu, réinstallez Python en cochant **Add python.exe to PATH**, puis fermez et rouvrez CMD.
- Si `streamlit` n'est pas reconnu, activez `.venv` puis exécutez `python -m pip install -r requirements.txt`.
- Pour arrêter le serveur : revenez au terminal et appuyez sur `Ctrl + C`.
