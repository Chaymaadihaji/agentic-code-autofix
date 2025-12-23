def est_palindrome(mot):
    """
    Vérifie si un mot est le même à l'endroit et à l'envers.

    Args:
        mot (str): Le mot à vérifier.

    Returns:
        bool: True si le mot est un palindrome, False sinon.
    """
    return mot == mot[::-1]

# Tests
print(est_palindrome("radar"))  # True
print(est_palindrome("python"))  # False
print(est_palindrome("level"))  # True
