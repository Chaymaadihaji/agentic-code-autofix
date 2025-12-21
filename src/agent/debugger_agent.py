# agents/debugger_agent.py
import re

class DebuggerAgent:
    """Agent qui analyse et corrige les bugs."""
    
    def __init__(self, llm_client):
        self.client = llm_client
        self.error_patterns = self._load_error_patterns()
    
    def analyze_failure(self, code: str, error_output: str, context: dict = None) -> dict:
        """
        Analyse une erreur et propose des corrections.
        
        Returns:
            {
                "error_type": "ImportError|AssertionError|...",
                "root_cause": "cause probable",
                "affected_files": ["file1.py", ...],
                "suggested_fix": "description de la correction",
                "priority": "high|medium|low"
            }
        """
        print("🐛 DebuggerAgent: Analyse de l'erreur...")
        
        analysis = {
            "error_type": "Unknown",
            "root_cause": "À déterminer",
            "affected_files": [],
            "suggested_fix": "",
            "priority": "medium",
            "confidence": 0.5
        }
        
        # Identifier le type d'erreur
        for pattern, error_type in self.error_patterns.items():
            if re.search(pattern, error_output, re.IGNORECASE):
                analysis["error_type"] = error_type
                analysis["confidence"] = 0.8
                break
        
        # Analyser avec l'IA pour plus de détails
        system_prompt = """
        Tu es un expert en débogage. Analyse les erreurs et trouve la cause racine.
        
        Réponds en JSON avec:
        {
            "root_cause": "cause principale",
            "affected_files": ["fichiers concernés"],
            "suggested_fix": "solution recommandée",
            "priority": "high|medium|low"
        }
        """
        
        user_prompt = f"""
        ANALYSE D'ERREUR:
        
        CODE:
        {code[:2000]}  # Limiter la taille
        
        SORTIE D'ERREUR:
        {error_output}
        
        CONTEXTE: {context or 'Aucun contexte supplémentaire'}
        
        Fournis une analyse précise et des recommandations de correction.
        """
        
        try:
            response = self.client.generate(system_prompt, user_prompt)
            
            # Extraire le JSON de la réponse
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                ai_analysis = eval(json_match.group(0))  # Attention: utiliser json.loads serait mieux
                
                # Fusionner avec l'analyse de base
                analysis.update({
                    k: v for k, v in ai_analysis.items() 
                    if k in analysis and v
                })
        
        except Exception as e:
            print(f"   ⚠️  Analyse IA échouée: {e}")
        
        print(f"   ✓ Erreur identifiée: {analysis['error_type']}")
        return analysis
    
    def generate_fix(self, code: str, analysis: dict, language: str = "python") -> str:
        """
        Génère le code corrigé basé sur l'analyse.
        
        Returns:
            Code corrigé complet
        """
        print(f"🐛 DebuggerAgent: Génération de correction...")
        
        system_prompt = f"""
        Expert en correction de bugs {language}.
        Corrigez le code en vous basant sur l'analyse fournie.
        Répondez UNIQUEMENT avec le code corrigé complet.
        """
        
        user_prompt = f"""
        CORRECTION REQUISE:
        
        ANALYSE DU BUG:
        - Type: {analysis.get('error_type')}
        - Cause: {analysis.get('root_cause')}
        - Priorité: {analysis.get('priority')}
        
        CODE ORIGINAL (À CORRIGER):
        {code}
        
        RECOMMANDATION: {analysis.get('suggested_fix', 'Aucune recommandation spécifique')}
        
        RÈGLES DE CORRECTION:
        1. Corriger TOUTES les erreurs identifiées
        2. Maintenir la même interface
        3. Ajouter des commentaires si les changements sont complexes
        4. Tester mentalement la correction
        
        Fournissez le CODE COMPLET CORRIGÉ.
        """
        
        try:
            corrected_code = self.client.generate(system_prompt, user_prompt)
            print(f"   ✓ Correction générée ({len(corrected_code)} caractères)")
            return corrected_code
            
        except Exception as e:
            print(f"   ❌ Échec de génération: {e}")
            # Fallback: retourner le code original
            return code
    
    def _load_error_patterns(self) -> dict:
        """Charge les patterns d'erreur courantes."""
        return {
            r"ImportError": "ImportError",
            r"ModuleNotFoundError": "ImportError",
            r"AssertionError": "AssertionError",
            r"AttributeError.*has no attribute": "AttributeError",
            r"NameError.*is not defined": "NameError",
            r"TypeError.*takes.*arguments": "TypeError",
            r"SyntaxError": "SyntaxError",
            r"IndentationError": "IndentationError",
            r"KeyError": "KeyError",
            r"ValueError": "ValueError",
            r"IndexError": "IndexError",
            r"FileNotFoundError": "FileNotFoundError",
            r"PermissionError": "PermissionError"
        }
    
    def validate_fix(self, original_code: str, fixed_code: str, error_type: str) -> bool:
        """
        Valide rapidement si la correction semble correcte.
        (Validation complète nécessite l'exécution des tests)
        """
        # Vérifications basiques
        checks = []
        
        # 1. Le code corrigé ne doit pas être vide
        checks.append(bool(fixed_code and fixed_code.strip()))
        
        # 2. Pour ImportError, vérifier que les imports sont présents
        if error_type == "ImportError":
            imports_original = re.findall(r'^import\s+\w+|^from\s+\w+\s+import', original_code, re.MULTILINE)
            imports_fixed = re.findall(r'^import\s+\w+|^from\s+\w+\s+import', fixed_code, re.MULTILINE)
            checks.append(len(imports_fixed) >= len(imports_original))
        
        # 3. La longueur doit être raisonnable (pas 3x plus long)
        checks.append(len(fixed_code) < len(original_code) * 3)
        
        return all(checks)