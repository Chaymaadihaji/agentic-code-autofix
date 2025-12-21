# utils/llm_client.py
import os
import time
from dotenv import load_dotenv  # <-- AJOUT CRITIQUE
from groq import Groq
from google import genai
from google.genai import types

# CHARGER LE .env AVANT TOUT
load_dotenv()

class LLMClient:
    """Client LLM partagé par tous les agents."""
    
    def __init__(self, provider="groq", model=None):
        self.provider = provider
        
        # Configuration par défaut
        if model is None:
            self.model = "llama-3.3-70b-versatile" if provider == "groq" else "gemini-1.5-pro"
        else:
            self.model = model
        
        # Récupérer la clé API depuis .env
        self.api_key = os.getenv("API_KEY")  # Maintenant ça devrait fonctionner
        
        if not self.api_key:
            # Afficher un message d'erreur détaillé
            print("❌ ERREUR: API_KEY non trouvée")
            print("🔍 Variables d'environnement disponibles:")
            for key in os.environ:
                if 'API' in key or 'KEY' in key:
                    value = os.getenv(key)
                    masked = value[:8] + "..." if value and len(value) > 8 else "***"
                    print(f"   {key}: {masked}")
            raise ValueError("❌ API_KEY non définie. Vérifiez votre fichier .env")
        
        # Masquer partiellement la clé pour l'affichage
        masked_key = self.api_key[:8] + "..." + self.api_key[-4:] if len(self.api_key) > 12 else "***"
        print(f"🔑 Clé API détectée: {masked_key}")
        
        # Initialiser le client selon le fournisseur
        if provider == "groq":
            self.client = Groq(api_key=self.api_key)
            print(f"🤖 Client Groq initialisé - Modèle: {self.model}")
            
        elif provider == "gemini":
            # Pour Gemini, définir la variable d'environnement
            os.environ["GOOGLE_API_KEY"] = self.api_key
            self.client = genai.Client()
            print(f"🤖 Client Gemini initialisé - Modèle: {self.model}")
            
        else:
            raise ValueError(f"Provider non supporté: {provider}")
    
    def generate(self, system_prompt: str, user_prompt: str, max_retries: int = 3) -> str:
        """Génère du texte avec gestion des erreurs."""
        
        for attempt in range(max_retries):
            try:
                if self.provider == "groq":
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                    
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        temperature=0.7,
                        max_tokens=2000,
                        top_p=1,
                        stream=False
                    )
                    content = response.choices[0].message.content
                
                elif self.provider == "gemini":
                    config = types.GenerateContentConfig(system_instruction=system_prompt)
                    response = self.client.models.generate_content(
                        model=self.model,
                        contents=[user_prompt],
                        config=config
                    )
                    content = response.text
                
                # Nettoyer le résultat
                content = content.strip()
                
                # Retirer les balises de code si présentes
                if content.startswith('```'):
                    lines = content.split('\n')
                    if len(lines) > 2 and lines[0].startswith('```') and lines[-1] == '```':
                        content = '\n'.join(lines[1:-1]).strip()
                
                return content
                
            except Exception as e:
                error_msg = str(e)
                
                # Logique de retry pour les erreurs temporaires
                if attempt < max_retries - 1:
                    if "429" in error_msg or "503" in error_msg or "overloaded" in error_msg.lower():
                        wait_time = 5 * (attempt + 1)  # Backoff exponentiel
                        print(f"⚠️  Serveur surchargé (Tentative {attempt+1}/{max_retries}). "
                              f"Nouvel essai dans {wait_time}s...")
                        time.sleep(wait_time)
                    elif "401" in error_msg or "invalid api key" in error_msg.lower():
                        # Erreur de clé API - pas la peine de retry
                        raise ValueError(f"❌ Clé API invalide: {error_msg}")
                    else:
                        print(f"⚠️  Erreur API (tentative {attempt+1}/{max_retries}): {error_msg}")
                        time.sleep(2)  # Petit délai avant de réessayer
                else:
                    # Dernière tentative échouée
                    raise Exception(f"🚨 Échec après {max_retries} tentatives: {error_msg}")
        
        # Ne devrait jamais arriver ici
        raise Exception("Erreur inattendue dans generate()")

# Test rapide
if __name__ == "__main__":
    try:
        print("🧪 Test du LLMClient...")
        
        # Vérifier la clé API
        api_key = os.getenv("API_KEY")
        if api_key:
            masked = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
            print(f"✅ Clé API trouvée: {masked}")
        else:
            print("❌ Clé API non trouvée")
            print("💡 Vérifiez que votre .env contient: API_KEY=votre_clé")
        
        # Tester l'initialisation
        client = LLMClient(provider="groq")
        
        # Petit test de génération
        print("\n🧠 Test de génération...")
        test_response = client.generate(
            system_prompt="Tu es un assistant utile.",
            user_prompt="Dis 'Bonjour' en une phrase.",
            max_retries=1
        )
        
        print(f"✅ Test réussi: {test_response[:50]}...")
        
    except Exception as e:
        print(f"❌ Erreur de test: {e}")