import streamlit as st
import json
import os
from export_github import push_to_github

# --- Initialisation dossiers ---
os.makedirs("data", exist_ok=True)
os.makedirs("rules", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# --- Templates pré-remplis ---
template_files = [f for f in os.listdir("templates") if f.endswith(".json")]
template_choice = st.sidebar.selectbox("Charger un template métier", ["Aucun"] + template_files)

# --- Gestion des datasets ---
dataset_files = [f for f in os.listdir("data") if f.endswith(".json")]
if not dataset_files:
    dataset_files = ["default.json"]
    with open("data/default.json", "w") as f:
        json.dump([], f)
dataset_choice = st.sidebar.selectbox("Choisir un dataset", dataset_files)
DATA_FILE = f"data/{dataset_choice}"

with open(DATA_FILE, "r") as f:
    dataset = json.load(f)

# --- Gestion des règles ---
rules_files = [f for f in os.listdir("rules") if f.endswith(".json")]
if not rules_files:
    rules_files = ["default.json"]
    with open("rules/default.json", "w") as f:
        json.dump({}, f)
rules_choice = st.sidebar.selectbox("Choisir un fichier de règles", rules_files)
RULES_FILE = f"rules/{rules_choice}"

with open(RULES_FILE, "r") as f:
    rules = json.load(f)

# --- Interface ---
st.title("🌟 MicroLLM Studio - No Code Avancé")

# Charger un template
if template_choice != "Aucun":
    with open(f"templates/{template_choice}", "r") as f:
        template_data = json.load(f)
    dataset.extend(template_data.get("dataset", []))
    rules.update(template_data.get("rules", {}))
    with open(DATA_FILE, "w") as f:
        json.dump(dataset, f, indent=4)
    with open(RULES_FILE, "w") as f:
        json.dump(rules, f, indent=4)
    st.success(f"Template {template_choice} chargé avec succès !")

# --- Ajouter Q/R ---
st.header("Ajouter des exemples Q/R")
question = st.text_input("Question")
answer = st.text_input("Réponse")
if st.button("Ajouter au dataset"):
    if question and answer:
        dataset.append({"question": question, "answer": answer})
        with open(DATA_FILE, "w") as f:
            json.dump(dataset, f, indent=4)
        st.success("Exemple ajouté !")

# --- Ajouter règle ---
st.header("Définir une règle simple")
rule_key = st.text_input("Mot clé")
rule_answer = st.text_input("Réponse associée")
if st.button("Ajouter une règle"):
    if rule_key and rule_answer:
        rules[rule_key] = rule_answer
        with open(RULES_FILE, "w") as f:
            json.dump(rules, f, indent=4)
        st.success("Règle ajoutée !")

# --- Tester le modèle avec entraînement automatique ---
st.header("Tester MicroLLM")
user_input = st.text_input("Posez une question")
if st.button("Générer réponse"):
    response = "Je ne sais pas."
    # Vérification règles
    for key, val in rules.items():
        if key.lower() in user_input.lower():
            response = val
            break
    # Vérification dataset
    for item in dataset:
        if item["question"].lower() == user_input.lower():
            response = item["answer"]
            break
    st.info(f"Réponse : {response}")
    
    # Entraînement automatique : si réponse non trouvée, on propose de l'ajouter
    if response == "Je ne sais pas.":
        add_response = st.text_input("Ajouter une réponse pour cette question ?")
        if add_response:
            dataset.append({"question": user_input, "answer": add_response})
            with open(DATA_FILE, "w") as f:
                json.dump(dataset, f, indent=4)
            st.success("Réponse ajoutée et modèle mis à jour automatiquement !")

# --- Dataset et règles actuels ---
st.header("Dataset actuel")
st.json(dataset)
st.header("Règles actuelles")
st.json(rules)

# --- Export GitHub automatique ---
st.header("Sauvegarde GitHub")
if st.button("Push dataset & règles vers GitHub"):
    try:
        push_to_github()
        st.success("Push terminé !")
    except Exception as e:
        st.error(f"Erreur push GitHub : {e}")
