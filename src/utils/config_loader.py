# src/utils/config_loader.py

import os
from dotenv import load_dotenv

def load_config():
    """
    Charge les variables d'environnement à partir du fichier .env
    et configure la clé d'API pour le fournisseur LLM choisi.
    """
    # Charge le fichier .env (à la racine du projet)
    load_dotenv()

    # --- Choix du Fournisseur LLM ---
    llm_provider = os.getenv("LLM_PROVIDER", "groq").lower()  # Par défaut: groq
    
    # --- Récupération des Clés API ---
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    groq_api_key = os.getenv("GROQ_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # --- Configuration selon le Fournisseur ---
    if llm_provider == "gemini":
        if not gemini_api_key:
            raise ValueError("Erreur : GEMINI_API_KEY non définie pour le fournisseur 'gemini'.")
        os.environ["GEMINI_API_KEY"] = gemini_api_key
        llm_model = os.getenv("LLM_MODEL", "gemini-2.5-flash")
        active_api_key = gemini_api_key
        
    elif llm_provider == "groq":
        if not groq_api_key:
            raise ValueError("Erreur : GROQ_API_KEY non définie pour le fournisseur 'groq'.")
        # Groq n'a pas besoin de variable d'environnement globale
        llm_model = os.getenv("LLM_MODEL", "llama3-70b-8192")
        active_api_key = groq_api_key
        
    elif llm_provider == "openai":
        if not openai_api_key:
            raise ValueError("Erreur : OPENAI_API_KEY non définie pour le fournisseur 'openai'.")
        os.environ["OPENAI_API_KEY"] = openai_api_key
        llm_model = os.getenv("LLM_MODEL", "gpt-4-turbo")
        active_api_key = openai_api_key
        
    else:
        raise ValueError(f"Fournisseur LLM non supporté: {llm_provider}")

    # Retourne les configurations clés
    return {
        "LLM_PROVIDER": llm_provider,
        "LLM_MODEL": llm_model,
        "API_KEY": active_api_key,
        "GEMINI_API_KEY": gemini_api_key,  # Gardé pour compatibilité
        "GROQ_API_KEY": groq_api_key,
        "OPENAI_API_KEY": openai_api_key
    }

if __name__ == '__main__':
    # Test simple pour vérifier le fonctionnement
    try:
        config = load_config()
        print("✅ Configuration chargée avec succès.")
        print(f"Fournisseur LLM : {config['LLM_PROVIDER']}")
        print(f"Modèle LLM : {config['LLM_MODEL']}")
        # Affichage sécurisé de la clé
        api_key = config['API_KEY']
        if api_key:
            print(f"Clé API (cachée) : {api_key[:4]}...{api_key[-4:]}")
    except ValueError as e:
        print(f"❌ {e}")