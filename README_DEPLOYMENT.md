# 🚀 Guide de Déploiement Streamlit - MicroLLM NoCode

## 📋 Pré-requis

✅ Un compte GitHub  
✅ Un compte Streamlit Cloud (gratuit sur [share.streamlit.io](https://share.streamlit.io))  
✅ Les fichiers corrigés de ce projet

---

## 🗂️ Structure du Projet Corrigée

Votre dépôt GitHub doit avoir cette structure **EXACTE** :

```
MicroLLM_NoCode/
├── streamlit_app.py          # ✅ Fichier principal (NOM EXACT!)
├── requirements.txt           # ✅ Dépendances Python
├── .gitignore                 # ✅ Fichiers à ignorer
├── README.md                  # Documentation
├── .streamlit/
│   └── config.toml           # ✅ Configuration Streamlit
├── data/
│   └── default.json          # Dataset vide au départ
├── rules/
│   └── default.json          # Règles vides au départ
├── templates/                 # ✅ UN SEUL dossier templates
│   ├── support.json
│   ├── rh.json
│   └── juridique.json
└── Export/                    # Dossier pour exports
```

---

## 🛠️ Étapes de Correction sur GitHub

### 1️⃣ Nettoyer la Structure

**SUPPRIMER ces dossiers/fichiers :**
```bash
❌ Template/
❌ Templates/
❌ template/
❌ app.py (si vous gardez streamlit_app.py)
❌ .replit (configuration Replit)
```

**GARDER uniquement :**
```bash
✅ streamlit_app.py
✅ templates/ (un seul, en minuscules)
✅ data/
✅ rules/
```

### 2️⃣ Remplacer les Fichiers

1. **Supprimez** l'ancien `app.py` ou `streamlit_app.py`
2. **Créez** un nouveau `streamlit_app.py` avec le contenu fourni
3. **Remplacez** `requirements.txt` avec la nouvelle version
4. **Créez** le dossier `.streamlit/` et ajoutez `config.toml`
5. **Ajoutez** le fichier `.gitignore`

### 3️⃣ Créer les Fichiers JSON par Défaut

**Créez `data/default.json` :**
```json
[]
```

**Créez `rules/default.json` :**
```json
[]
```

**Créez `templates/support.json` :**
```json
{
  "description": "Template Support Client",
  "dataset": [
    {
      "question": "Comment réinitialiser mon mot de passe ?",
      "reponse": "Pour réinitialiser votre mot de passe, cliquez sur 'Mot de passe oublié' sur la page de connexion.",
      "categorie": "Support"
    }
  ],
  "rules": [
    {
      "nom": "Politesse",
      "description": "Toujours commencer par une formule de politesse",
      "type": "Contenu",
      "active": true
    }
  ]
}
```

---

## 🚀 Déploiement sur Streamlit Cloud

### Étape 1 : Préparer GitHub

```bash
# Dans votre terminal (ou via l'interface GitHub)
git add .
git commit -m "Fix: Structure corrigée pour Streamlit Cloud"
git push origin main
```

### Étape 2 : Déployer sur Streamlit Cloud

1. **Allez sur** [share.streamlit.io](https://share.streamlit.io)
2. **Connectez-vous** avec votre compte GitHub
3. **Cliquez** sur "New app"
4. **Sélectionnez** :
   - Repository : `benjaminpolydeq/MicroLLM_NoCode`
   - Branch : `main`
   - Main file path : `streamlit_app.py`
5. **Cliquez** sur "Deploy!"

### Étape 3 : Vérifier le Déploiement

L'application va se construire (2-5 minutes). Vous verrez :

✅ **Succès** : L'app s'ouvre dans votre navigateur  
❌ **Erreur** : Consultez les logs ci-dessous

---

## 🐛 Résolution des Erreurs Courantes

### Erreur : "ModuleNotFoundError: No module named 'streamlit'"

**Solution :** Vérifiez que `requirements.txt` contient :
```
streamlit>=1.28.0
```

### Erreur : "FileNotFoundError: [Errno 2] No such file or directory: '/app/data/default.json'"

**Solution :** Les dossiers `data/`, `rules/`, `templates/` doivent exister dans GitHub avec au moins un fichier `.json` vide

**Créez ces fichiers :**
```bash
data/default.json       → []
rules/default.json      → []
templates/.gitkeep      → (fichier vide)
```

### Erreur : "Streamlit app not found"

**Causes possibles :**
1. Le fichier ne s'appelle pas exactement `streamlit_app.py`
2. Le fichier n'est pas à la racine du dépôt
3. Mauvais chemin configuré dans Streamlit Cloud

**Solution :** Renommez en `streamlit_app.py` et mettez à la racine

### Erreur : "AttributeError" ou "ImportError"

**Solution :** Votre ancien code utilise des imports incompatibles. Utilisez la version corrigée de `streamlit_app.py`

---

## ✅ Checklist Finale

Avant de déployer, vérifiez :

- [ ] ✅ Le fichier s'appelle exactement `streamlit_app.py` (pas `app.py`)
- [ ] ✅ `requirements.txt` existe et contient `streamlit>=1.28.0`
- [ ] ✅ Un seul dossier `templates/` (pas de doublons)
- [ ] ✅ Les dossiers `data/`, `rules/`, `Export/` existent
- [ ] ✅ Fichiers JSON par défaut créés (`data/default.json`, `rules/default.json`)
- [ ] ✅ Le fichier `.streamlit/config.toml` existe
- [ ] ✅ Pas de chemins absolus dans le code
- [ ] ✅ Tous les fichiers sont bien poussés sur GitHub
- [ ] ✅ Pas de fichier `.replit` (configuration Replit)

---

## 🔍 Tester Localement Avant de Déployer

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'app localement
streamlit run streamlit_app.py
```

Si ça marche localement, ça devrait marcher sur Streamlit Cloud !

---

## 📞 Support

Si le problème persiste après avoir suivi ce guide :

1. **Consultez les logs** dans Streamlit Cloud (bouton "Manage app" → onglet "Logs")
2. **Copiez le message d'erreur complet**
3. **Partagez-le** pour obtenir de l'aide

---

## 🎉 Félicitations !

Une fois déployé, votre application sera accessible via une URL publique :
```
https://your-app-name.streamlit.app
```

Vous pourrez la partager avec n'importe qui ! 🚀
