import streamlit as st
import sys
import os
import subprocess
import difflib
import shutil
from agent.code_manager import CodeManager
from utils.file_manager import read_code, write_code

# Configuration de l'interface
st.set_page_config(page_title="Agent Code Fixer - Dashboard", page_icon="🤖", layout="wide")

st.title("🤖 Agentic Code Autofix : Dashboard de Correction")
st.markdown("---")

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    max_attempts = st.slider("Tentatives maximum", 1, 5, 3)
    st.info("Cet agent détecte le langage, génère des tests et s'auto-corrige en cas d'échec.")

# --- ZONE DE SAISIE ---
objective = st.text_area("🎯 Objectif de programmation :", 
                        placeholder="Ex: Crée une classe 'Banque' avec des méthodes depot et retrait...",
                        height=150)

def run_tests_streamlit(langage):
    """Exécute les tests et retourne (succès, logs)"""
    langage = langage.lower().strip()
    try:
        if langage == "python":
            cmd = [sys.executable, '-m', 'pytest', 'tests/test_generated_code.py', '-v']
        elif langage == "javascript" or langage == "js":
            cmd = ["node", "tests/test_generated_code.js"]
        else:
            return False, f"❌ Langage {langage} non supporté."

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        return (result.returncode == 0), result.stdout + "\n" + result.stderr
    except Exception as e:
        return False, str(e)

# --- LANCEMENT DE L'AGENT ---
if st.button("Lancer l'Agent 🚀"):
    if not objective:
        st.warning("Veuillez entrer un objectif.")
    else:
        manager = CodeManager()
        
        # 1. Génération initiale
        with st.status("🚀 Phase 1 : Génération initiale...", expanded=True) as status:
            manager.generate_initial_solution(objective)
            lang = getattr(manager, 'langage_cible', 'python')
            st.write(f"✅ Langage détecté : **{lang}**")
            
            current_code = read_code(is_test=False, language=lang)
            
            for attempt in range(max_attempts):
                st.markdown(f"### 🔄 Tentative n°{attempt+1}")
                
                # Exécution des tests
                success, test_logs = run_tests_streamlit(lang)
                
                if success:
                    st.success(f"✅ Tentative {attempt+1} : Tous les tests passent !")
                    status.update(label="Succès total !", state="complete")
                    # On affiche le code final réussi
                    st.subheader("📄 Code Final Validé")
                    st.code(current_code, language=lang)
                    break
                else:
                    st.error(f"❌ Tentative {attempt+1} : Échec des tests")
                    
                    # Affichage de l'erreur pour la prof
                    with st.expander("🔍 Voir l'erreur technique (Traceback)"):
                        st.code(test_logs)
                    
                    if attempt < max_attempts - 1:
                        st.write("🧠 L'IA analyse l'erreur pour corriger le code...")
                        
                        # SAUVEGARDE de l'ancien code pour le DIFF
                        old_code = current_code
                        
                        # Correction
                        corrected_code = manager.fix_solution(current_code, test_logs)
                        write_code(corrected_code, is_test=False, language=lang)
                        current_code = corrected_code
                        
                        # --- AFFICHAGE DU DIFF (AMÉLIORATION) ---
                        st.subheader("🛠️ Améliorations apportées :")
                        
                        # Calcul de la différence
                        diff = difflib.ndiff(old_code.splitlines(), current_code.splitlines())
                        # On ne garde que les lignes modifiées pour la clarté
                        diff_filtered = [l for l in diff if l.startswith('+ ') or l.startswith('- ')]
                        
                        if diff_filtered:
                            st.markdown("*( `-` Ancien code | `+` Nouveau code corrigé )*")
                            st.code("\n".join(diff_filtered), language="diff")
                        else:
                            st.write("L'IA a réécrit le code de manière identique ou restructuré l'ensemble.")
                    else:
                        st.warning("🚨 Nombre maximum de tentatives atteint sans succès.")

        # --- CODE DE TEST ---
        st.markdown("---")
        with st.expander("🧪 Voir le code de test généré par l'agent"):
            test_code = read_code(is_test=True, language=lang)
            st.code(test_code, language=lang)