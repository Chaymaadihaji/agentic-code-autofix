"""
 Détecteur de Bugs Intelligent - Version Améliorée
Détecte les erreurs à plusieurs niveaux : syntaxe, logique, performance, sécurité
"""

import ast
import astroid
import pylint
import bandit
import radon
from radon.complexity import cc_visit
import lizard
import safety
import subprocess
import json
import os
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class BugSeverity(Enum):
    CRITICAL = "CRITICAL"      
    HIGH = "HIGH"              
    MEDIUM = "MEDIUM"          
    LOW = "LOW"               
    INFO = "INFO"            

@dataclass
class BugReport:
    """Rapport structuré de bug"""
    severity: BugSeverity
    category: str
    description: str
    location: Tuple[str, int, int]  
    suggestion: str
    code_snippet: str
    metrics: Dict[str, Any] = None

class DetecteurBugsAmeliore:
    def __init__(self):
        self.known_patterns = self._load_known_patterns()
        self.metrics_history = []
    
    def detecter_bugs_complet(self, chemin_projet: str) -> List[BugReport]:
        """
        Détection multi-niveaux de bugs
        """
        print(f" Détection approfondie dans {chemin_projet}")
        
        bugs = []
        
        # 1. Analyse statique de base
        bugs.extend(self._analyse_statique_basique(chemin_projet))
        
        # 2. Analyse de complexité
        bugs.extend(self._analyse_complexite(chemin_projet))
        
        # 3. Détection de patterns problématiques
        bugs.extend(self._detecter_patterns_problematiques(chemin_projet))
        
        # 4. Analyse de sécurité
        bugs.extend(self._analyse_securite(chemin_projet))
        
        # 5. Vérification des dépendances
        bugs.extend(self._analyser_dependances(chemin_projet))
        
        # 6. Métriques de qualité
        bugs.extend(self._calculer_metriques_qualite(chemin_projet))
        
        # Trier par sévérité
        severity_order = {BugSeverity.CRITICAL: 0, BugSeverity.HIGH: 1, 
                         BugSeverity.MEDIUM: 2, BugSeverity.LOW: 3, BugSeverity.INFO: 4}
        bugs.sort(key=lambda x: severity_order[x.severity])
        
        return bugs
    
    def _analyse_statique_basique(self, chemin_projet: str) -> List[BugReport]:
        """Analyse syntaxique et sémantique de base"""
        bugs = []
        
        for root, _, files in os.walk(chemin_projet):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            code = f.read()
                        
                       
                        try:
                            tree = ast.parse(code, filename=filepath)
                        except SyntaxError as e:
                            bugs.append(BugReport(
                                severity=BugSeverity.CRITICAL,
                                category="SyntaxError",
                                description=f"Erreur de syntaxe: {e.msg}",
                                location=(filepath, e.lineno or 1, e.offset or 1),
                                suggestion="Corriger la syntaxe Python",
                                code_snippet=self._get_code_context(code, e.lineno)
                            ))
                            continue
                        
                       
                        bugs.extend(self._analyser_ast(tree, filepath, code))
                        
                    except Exception as e:
                        print(f" Erreur analyse {filepath}: {e}")
        
        return bugs
    
    def _analyser_ast(self, tree: ast.AST, filepath: str, code: str) -> List[BugReport]:
        """Analyse AST pour détecter des patterns problématiques"""
        bugs = []
        
        class BugVisitor(ast.NodeVisitor):
            def __init__(self, filepath, code):
                self.filepath = filepath
                self.code = code
                self.bugs = []
                self.lines = code.split('\n')
            
            def visit_Assign(self, node):
                
                if isinstance(node.value, ast.Call):
                    if isinstance(node.value.func, ast.Name):
                        if node.value.func.id == 'eval':
                            self.bugs.append(BugReport(
                                severity=BugSeverity.HIGH,
                                category="Security",
                                description="Utilisation dangereuse de eval()",
                                location=(self.filepath, node.lineno, node.col_offset),
                                suggestion="Remplacer eval() par une alternative sécurisée",
                                code_snippet=self._get_line(node.lineno)
                            ))
                self.generic_visit(node)
            
            def visit_Call(self, node):
                
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'execute' and 'sql' in str(node.func.value).lower():
                       
                        for arg in node.args:
                            if isinstance(arg, ast.Str):
                                if any(keyword in arg.s.lower() for keyword in ['select', 'insert', 'delete']):
                                    if '%s' in arg.s or '{' in arg.s:
                                        self.bugs.append(BugReport(
                                            severity=BugSeverity.HIGH,
                                            category="SQL Injection",
                                            description="Injection SQL potentielle",
                                            location=(self.filepath, node.lineno, node.col_offset),
                                            suggestion="Utiliser des requêtes paramétrées",
                                            code_snippet=self._get_line(node.lineno)
                                        ))
                self.generic_visit(node)
            
            def visit_While(self, node):
                
                if isinstance(node.test, ast.Constant):
                    if node.test.value is True:
                        self.bugs.append(BugReport(
                            severity=BugSeverity.MEDIUM,
                            category="Logic",
                            description="Boucle while True sans condition de sortie claire",
                            location=(self.filepath, node.lineno, node.col_offset),
                            suggestion="Ajouter une condition de sortie ou un break conditionnel",
                            code_snippet=self._get_line(node.lineno)
                        ))
                self.generic_visit(node)
            
            def _get_line(self, lineno):
                if 0 <= lineno-1 < len(self.lines):
                    return self.lines[lineno-1]
                return ""
        
        visitor = BugVisitor(filepath, code)
        visitor.visit(tree)
        return visitor.bugs
    
    def _analyse_complexite(self, chemin_projet: str) -> List[BugReport]:
        """Analyse de complexité cyclomatique"""
        bugs = []
        
        for root, _, files in os.walk(chemin_projet):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            code = f.read()
                        
                      
                        try:
                            results = cc_visit(code)
                            for block in results:
                                if block.complexity > 10:  
                                    bugs.append(BugReport(
                                        severity=BugSeverity.MEDIUM,
                                        category="Complexity",
                                        description=f"Fonction trop complexe: {block.name} (CC={block.complexity})",
                                        location=(filepath, block.lineno, 1),
                                        suggestion="Refactoriser la fonction en sous-fonctions plus simples",
                                        code_snippet=block.fullname,
                                        metrics={"complexity": block.complexity}
                                    ))
                        except Exception as e:
                            print(f" Erreur analyse complexité {filepath}: {e}")
                    
                    except Exception as e:
                        print(f"  Erreur lecture {filepath}: {e}")
        
        return bugs
    
    def _detecter_patterns_problematiques(self, chemin_projet: str) -> List[BugReport]:
        """Détection de patterns connus comme problématiques"""
        bugs = []
        
        problematic_patterns = [
            {
                "pattern": r"open\([^)]*\)\.read\(\)",
                "category": "Resource Management",
                "description": "Fichier ouvert sans fermeture explicite",
                "suggestion": "Utiliser with open() as f:",
                "severity": BugSeverity.MEDIUM
            },
            {
                "pattern": r"\.append\(\[.*\]\)",
                "category": "Performance",
                "description": "Append de liste dans une boucle peut être lent",
                "suggestion": "Utiliser list comprehension ou extend()",
                "severity": BugSeverity.LOW
            },
            {
                "pattern": r"except:",
                "category": "Error Handling",
                "description": "Exception trop générale",
                "suggestion": "Spécifier les exceptions à catcher",
                "severity": BugSeverity.MEDIUM
            },
            {
                "pattern": r"print\(.*\)",
                "category": "Code Quality",
                "description": "Debug print dans le code",
                "suggestion": "Utiliser logging ou supprimer",
                "severity": BugSeverity.INFO
            }
        ]
        
        for root, _, files in os.walk(chemin_projet):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                        
                        for i, line in enumerate(lines):
                            for pattern_info in problematic_patterns:
                                if re.search(pattern_info["pattern"], line):
                                    bugs.append(BugReport(
                                        severity=pattern_info["severity"],
                                        category=pattern_info["category"],
                                        description=pattern_info["description"],
                                        location=(filepath, i+1, 1),
                                        suggestion=pattern_info["suggestion"],
                                        code_snippet=line.strip()
                                    ))
                    
                    except Exception as e:
                        print(f" Erreur analyse patterns {filepath}: {e}")
        
        return bugs
    
    def _get_code_context(self, code: str, lineno: int, context_lines: int = 3) -> str:
        """Retourne le contexte autour d'une ligne"""
        lines = code.split('\n')
        start = max(0, lineno - context_lines - 1)
        end = min(len(lines), lineno + context_lines)
        
        context = []
        for i in range(start, end):
            prefix = ">>> " if i == lineno - 1 else "    "
            context.append(f"{i+1:4}{prefix}{lines[i]}")
        
        return '\n'.join(context)
    
    def _load_known_patterns(self) -> Dict:
        """Charge les patterns de bugs connus"""
        return {
            "security": [
                {"pattern": "eval\\(", "risk": "HIGH", "description": "Évaluation de code dynamique"},
                {"pattern": "exec\\(", "risk": "HIGH", "description": "Exécution de code dynamique"},
                {"pattern": "pickle\\.loads", "risk": "HIGH", "description": "Désérialisation non sécurisée"}
            ],
            "performance": [
                {"pattern": "for.*for", "risk": "MEDIUM", "description": "Boucles imbriquées"},
                {"pattern": "list\\.append\\(list\\)", "risk": "LOW", "description": "Append inefficace"}
            ]
        }

# Test
if __name__ == "__main__":
    detecteur = DetecteurBugsAmeliore()
    
  
    test_code = """
def dangerous_function():
    import os
    eval("os.system('ls')")  # DANGER!
    
def complex_function(x):
    if x > 0:
        if x < 10:
            if x % 2 == 0:
                for i in range(x):
                    for j in range(x):
                        print(i * j)
    
def read_file():
    f = open("test.txt").read()  # Problème de ressource
    
try:
    result = 1 / 0
except:
    pass  # Exception trop générale
"""
    
    import tempfile
    import os
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "buggy.py")
        with open(test_file, "w") as f:
            f.write(test_code)
        
        bugs = detecteur._analyse_statique_basique(tmpdir)
        print(f"\n🐛 {len(bugs)} bugs détectés:")
        for bug in bugs:
            print(f"\n  {bug.severity.value} - {bug.category}")
            print(f"  {bug.description}")
            print(f"  Suggestion: {bug.suggestion}")