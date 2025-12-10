
# MicroLLM-NoCode 🌟

**MicroLLM-NoCode** est une plateforme légère et privée de modèles linguistiques (MicroLLM) basée sur ARSLM.  
Elle permet de générer du texte et des réponses conversationnelles via un modèle neuronal minimaliste, avec une interface **no-code** accessible à tous.  
Le projet inclut des **templates métiers pré-remplis** et un **mini-entraînement automatique**, permettant aux utilisateurs de spécialiser le modèle sans aucune expérience en codage.

---

## Fonctionnalités principales

- Interface graphique intuitive pour ajouter Q/R et définir des règles métiers.  
- Templates pré-remplis pour RH, juridique, médical, support client.  
- Mini-entraînement automatique : le modèle apprend en temps réel à partir des nouvelles questions/réponses ajoutées.  
- Multi-datasets et multi-règles pour gérer plusieurs domaines métiers.  
- Export automatique des datasets et règles vers GitHub.  
- Déploiement simple sur **Replit**, sans installation complexe.

---

## Structure du projet

MicroLLM-NoCode/ ├─ app.py                 # Interface principale Streamlit ├─ export_github.py       # Script pour push dataset et règles sur GitHub ├─ requirements.txt       # Dépendances Python ├─ .replit                # Configuration Replit pour lancer l'app ├─ data/                  # Contient le ou les datasets │  └─ default.json ├─ rules/                 # Contient les règles initiales │  └─ default.json └─ templates/             # Templates pré-remplis pour différents métiers ├─ rh.json ├─ juridique.json ├─ medical.json └─ support.json

- **data/** → datasets personnalisables par l’utilisateur  
- **rules/** → règles métiers simples pour adapter le modèle  
- **templates/** → exemples pré-remplis pour RH, juridique, médical et support  
- **app.py** → interface no-code pour ajouter Q/R, définir des règles et tester le modèle  
- **export_github.py** → sauvegarde automatique vers GitHub  

---

## Démarrage rapide sur Replit

1. Importer le projet depuis GitHub ou téléverser le ZIP sur Replit.  
2. Vérifier que le fichier `.replit` est présent (configure le lancement Streamlit).  
3. Cliquer sur **Run** → MicroLLM Studio s’ouvre automatiquement.  
4. Charger un **template métier** pour démarrer rapidement.  
5. Ajouter des Q/R ou des règles directement dans l’interface.  
6. Tester le modèle et, si nécessaire, ajouter de nouvelles réponses pour le mini-entraînement automatique.  
7. Sauvegarder les datasets et règles sur GitHub via le bouton “Push dataset & règles vers GitHub”.  

---

## Templates et mini-entraînement automatique

- Templates pré-remplis pour RH, juridique, médical et support client, prêts à l’emploi.  
- Le mini-entraînement automatique permet au modèle de **s’adapter aux nouvelles questions/réponses ajoutées** par l’utilisateur, sans aucune intervention technique.  
- Les utilisateurs peuvent créer leurs propres datasets et règles pour spécialiser MicroLLM dans n’importe quel domaine.

---

## Licence

Copyright (c) 2025 Benjamin Amaad Kama

Tous droits réservés. MicroLLM-NoCode est la propriété exclusive de Benjamin Amaad Kama.

L'utilisation est autorisée uniquement pour usage personnel ou interne à votre organisation. Aucune redistribution, modification ou usage commercial n'est autorisé sans accord écrit préalable.

---

## Contact

- **Adresse :** Nguekhokh, Mbour, Sénégal  
- **Email :** flywithjesus@outlook.com  

---

MicroLLM-NoCode transforme les modèles linguistiques complexes en outils accessibles, sécurisés et adaptables pour tous les métiers, **sans codage**.

