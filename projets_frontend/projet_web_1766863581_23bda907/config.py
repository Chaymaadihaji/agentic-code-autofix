import os
import random
import json

# Chemin vers le fichier de config
config_file = 'config.json'

# Chemin vers le répertoire de données
data_dir = 'data'

# Chemin vers le fichier de mots
word_file = 'mots.json'

# Nombre maximal d'essais
max_attempts = 6

# Fonction pour générer un mot au hasard
def generate_word():
    with open(word_file, 'r') as f:
        mots = json.load(f)
    return random.choice(mots)

# Fonction pour afficher la lettre choisie
def display_letter(letter, word, guesses):
    result = ''
    for i, l in enumerate(word):
        if l == letter:
            result += letter + ' '
        elif letter in guesses:
            result += '_ '
        else:
            result += '_ '
    return result

# Fonction pour compter le nombre d'essais
def count_attempts(attempts, max_attempts):
    return max_attempts - attempts

# Fonction pour sauvegarder le jeu
def save_game(state):
    with open(config_file, 'w') as f:
        json.dump(state, f)

# Fonction pour charger le jeu
def load_game():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        return {'word': '', 'guesses': '', 'attempts': 0}

# Fonction pour lancer le jeu
def start_game():
    state = load_game()
    word = generate_word()
    state['word'] = word
    state['guesses'] = ''
    state['attempts'] = 0
    save_game(state)
    return state

# Fonction pour jouer au jeu
def play_game(state):
    while True:
        print(display_letter(state['guesses'], state['word'], state['guesses']))
        letter = input("Entrez une lettre: ")
        if letter in state['word']:
            state['guesses'] += letter
        else:
            state['attempts'] += 1
            if state['attempts'] >= max_attempts:
                print("Vous avez perdu ! Le mot était : " + state['word'])
                break
        if '_' not in display_letter(state['guesses'], state['word'], state['guesses']):
            print("Vous avez gagné ! Le mot était : " + state['word'])
            break
        save_game(state)

if __name__ == "__main__":
    start_game()
    play_game(load_game())
