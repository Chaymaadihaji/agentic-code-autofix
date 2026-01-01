import streamlit as st
import sys
import os
import shutil
import time
from io import StringIO

from main import AutoCoderBugTest

st.set_page_config(page_title="Terminal AutoCoder", page_icon="", layout="wide")


st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .terminal-container {
        background-color: #000000;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #444;
        height: 600px;
        overflow-y: auto;
        font-size: 14px;
        line-height: 1.4;
        box-shadow: inset 0 0 15px #000;
    }
    /* Palette de couleurs du Terminal */
    .t-normal { color: #00ff00; }  /* Vert classique */
    .t-error { color: #ff3333; font-weight: bold; background-color: rgba(255,0,0,0.1); } /* Rouge vif pour erreurs */
    .t-success { color: #00e676; font-weight: bold; } /* Vert brillant */
    .t-info { color: #00d4ff; } /* Bleu pour l'analyse et l'info */
    .t-warning { color: #ffab00; } /* Orange pour les warnings */
</style>
""", unsafe_allow_html=True)

class RealTimeTerminal(StringIO):
    """Capture les prints et applique des couleurs HTML selon le contenu"""
    def __init__(self, placeholder):
        super().__init__()
        self.placeholder = placeholder
        self.lines = []

    def write(self, s):
        if s.strip():
            new_lines = s.splitlines()
            for line in new_lines:
               
                if any(err in line.upper() for err in ["", "ERREUR", "ERROR", "EXCEPTION", "FAILED", "✗"]):
                    styled = f'<span class="t-error">{line}</span>'
              
                elif any(succ in line.upper() for succ in ["", "SUCCÈS", "SUCCESS", "✓", "TERMINÉ"]):
                    styled = f'<span class="t-success">{line}</span>'
                
                elif any(info in line.upper() for info in ["", "ANALYSE", "ARCHITECTURE", "INITIALISATION"]):
                    styled = f'<span class="t-info">{line}</span>'
               
                elif "" in line or "WARNING" in line.upper():
                    styled = f'<span class="t-warning">{line}</span>'
                
                else:
                    styled = f'<span class="t-normal">{line}</span>'
                
                self.lines.append(styled)

            full_html = "<br>".join(self.lines)
            self.placeholder.markdown(f'<div class="terminal-container">{full_html}</div>', unsafe_allow_html=True)

def main():
    st.title(" Agent Développeur Autonome")
    st.caption("Terminal synchronisé - Mode Debugging Actif")

    # Zone de saisie
    demande = st.text_area(" Demande pour le robot :", height=100, placeholder="Décrivez votre projet ici...")

    col1, col2 = st.columns([1, 4])
    with col1:
        tentatives = st.number_input("Tentatives de correction", 1, 10, 4)
    
    if st.button(" LANCER L'EXÉCUTION", type="primary", use_container_width=True):
        if not demande.strip():
            st.error("Veuillez saisir une demande.")
            return

        # Zone Terminal
        terminal_placeholder = st.empty()
        terminal_stream = RealTimeTerminal(terminal_placeholder)
        
        # Redirection
        old_stdout = sys.stdout
        sys.stdout = terminal_stream

        try:
            
            autocoder = AutoCoderBugTest(max_tentatives=tentatives)
            resultat = autocoder.generer_avec_bugs(demande)
            
            sys.stdout = old_stdout

            
            st.markdown("---")
            if resultat and 'chemin' in resultat:
                st.success(f" Processus terminé avec succès. Score final : {resultat.get('score_final', 0)}/100")
                
                chemin = resultat['chemin']
                if os.path.exists(chemin):
                    shutil.make_archive(chemin, 'zip', chemin)
                    with open(f"{chemin}.zip", "rb") as f:
                        st.download_button(
                            label=" TÉLÉCHARGER LE PROJET (.ZIP)",
                            data=f,
                            file_name=f"{os.path.basename(chemin)}.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                

        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"Erreur critique : {str(e)}")

if __name__ == "__main__":
    main()