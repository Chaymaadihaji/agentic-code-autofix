"""
💾 Cache pour réduire les appels API
"""

import json
import hashlib
import os

class CacheAPI:
    def __init__(self, cache_dir="cache_api"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_key(self, demande, fichier_info, analyse):
        """Crée une clé de cache unique"""
        data = f"{demande}_{json.dumps(fichier_info, sort_keys=True)}_{json.dumps(analyse, sort_keys=True)}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def get(self, key):
        """Récupère depuis le cache"""
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return None
        return None
    
    def set(self, key, data):
        """Sauvegarde dans le cache"""
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    
    def clear(self):
        """Vide le cache"""
        import shutil
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)