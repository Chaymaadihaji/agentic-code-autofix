import os
from pathlib import Path

# Définition des chemins relatifs
BASE_DIR = Path(__file__).resolve().parent.parent.parent
GENERATED_CODE_DIR = BASE_DIR / "generated_code"
TESTS_DIR = BASE_DIR / "tests"

# Dictionnaire des extensions par langage
EXTENSIONS = {
    "python": ".py",
    "c": ".c",
    "javascript": ".js",
    "js": ".js",
    "java": ".java",
    "cpp": ".cpp"
}

def ensure_directories_exist():
    """Assure que les répertoires 'generated_code' et 'tests' existent."""
    GENERATED_CODE_DIR.mkdir(exist_ok=True)
    TESTS_DIR.mkdir(exist_ok=True)
    (GENERATED_CODE_DIR / "__init__.py").touch(exist_ok=True)

def write_code(content: str, is_test: bool = False, language: str = "python", filename: str = None):
    """
    Écrit le code dans le fichier approprié avec la bonne extension.
    
    Args:
        content: Code à écrire
        is_test: Si c'est un fichier de test
        language: Langage de programmation
        filename: Nom PERSONNALISÉ du fichier (ex: "todo_list.py", "calculatrice.py")
    """
    lang = language.lower().strip()
    ext = EXTENSIONS.get(lang, ".py")  # .py par défaut si inconnu
    
    # DÉTERMINER LE NOM DE FICHIER
    if filename:
        # Utiliser le nom personnalisé fourni
        # S'assurer qu'il a la bonne extension
        if not filename.endswith(ext):
            filename = filename.rstrip('.') + ext
    else:
        # Nom par défaut (ancien comportement)
        if is_test:
            filename = f"test_generated_code{ext}"
        else:
            filename = f"solution{ext}"
    
    # Pour les tests Python, s'assurer qu'ils commencent par test_
    if is_test and lang == "python" and not filename.startswith("test_"):
        # Garder l'extension
        base_name = os.path.splitext(filename)[0]
        file_ext = os.path.splitext(filename)[1]
        filename = f"test_{base_name}{file_ext}"
    
    # Choisir le dossier
    target_dir = TESTS_DIR if is_test else GENERATED_CODE_DIR
    filepath = target_dir / filename
    
    # Créer les dossiers si nécessaire
    filepath.parent.mkdir(exist_ok=True, parents=True)
    
    # Correctif d'import spécifique à Python pour les tests
    if is_test and lang == "python":
        # Ajouter le chemin d'import si nécessaire
        if "import sys" not in content and ("from generated_code" in content or "import generated_code" in content):
            content = (
                "import sys\nimport os\n"
                "sys.path.append(os.path.join(os.path.dirname(__file__), '..'))\n"
                + content
            )
    
    # Écrire le fichier
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"📄 Fichier [{lang}] créé : {filepath}")
    return str(filepath)

def read_code(is_test: bool = False, language: str = "python", filename: str = None) -> str | None:
    """Lit le contenu du fichier selon le langage et le nom spécifique."""
    lang = language.lower().strip()
    ext = EXTENSIONS.get(lang, ".py")
    
    # Déterminer le nom de fichier
    if filename:
        if not filename.endswith(ext):
            filename = filename.rstrip('.') + ext
    else:
        # Nom par défaut (compatibilité)
        filename = f"test_generated_code{ext}" if is_test else f"solution{ext}"
    
    # Choisir le dossier
    target_dir = TESTS_DIR if is_test else GENERATED_CODE_DIR
    target_file = target_dir / filename
    
    if not target_file.exists():
        return None
    
    with open(target_file, 'r', encoding='utf-8') as f:
        return f.read()

def get_all_generated_files():
    """Retourne tous les fichiers générés."""
    files = []
    
    # Fichiers de code source
    if GENERATED_CODE_DIR.exists():
        for file in GENERATED_CODE_DIR.glob("*"):
            if file.is_file() and file.name != "__init__.py":
                files.append({
                    "type": "code",
                    "name": file.name,
                    "path": str(file),
                    "size": file.stat().st_size
                })
    
    # Fichiers de test
    if TESTS_DIR.exists():
        for file in TESTS_DIR.glob("*"):
            if file.is_file():
                files.append({
                    "type": "test",
                    "name": file.name,
                    "path": str(file),
                    "size": file.stat().st_size
                })
    
    return files

def clean_project():
    """Supprime tous les fichiers de code dans les dossiers générés."""
    for folder in [GENERATED_CODE_DIR, TESTS_DIR]:
        if folder.exists():
            for file in folder.glob("*"):
                if file.is_file() and file.name != "__init__.py":
                    file.unlink()
                    print(f"🗑️ Nettoyage : {file.name} supprimé.")

def rename_file(old_name: str, new_name: str, is_test: bool = False):
    """Renomme un fichier généré."""
    target_dir = TESTS_DIR if is_test else GENERATED_CODE_DIR
    old_path = target_dir / old_name
    new_path = target_dir / new_name
    
    if old_path.exists():
        old_path.rename(new_path)
        print(f"✏️ Renommé: {old_name} → {new_name}")
        return True
    return False

# --- Test rapide du module corrigé ---
if __name__ == '__main__':
    print("--- Test du File Manager CORRIGÉ ---")
    
    # 1. Assurer que les dossiers existent
    ensure_directories_exist()
    
    # 2. Écrire des fichiers avec des noms PERSONNALISÉS
    print("\n1. Création de fichiers personnalisés:")
    
    # Fichier principal TodoList
    todo_content = "class TodoList:\n    def __init__(self):\n        self.taches = []"
    write_code(todo_content, is_test=False, language="python", filename="todo_list.py")
    
    # Fichier de test TodoList
    test_todo = "import unittest\nfrom generated_code.todo_list import TodoList\n\nclass TestTodoList(unittest.TestCase):\n    def test_init(self):\n        todo = TodoList()\n        self.assertEqual(len(todo.taches), 0)"
    write_code(test_todo, is_test=True, language="python", filename="test_todo_list.py")
    
    # Fichier Task
    task_content = "class Task:\n    def __init__(self, name):\n        self.name = name"
    write_code(task_content, is_test=False, language="python", filename="task.py")
    
    # 3. Lister tous les fichiers créés
    print("\n2. Fichiers créés:")
    files = get_all_generated_files()
    for f in files:
        print(f"   - {f['type']}: {f['name']} ({f['size']} bytes)")
    
    # 4. Nettoyer
    clean_project()
    print("\n3. Nettoyage effectué")
    print("--- Test terminé ---")