# main.py

def est_palindrome(mot):
    return mot == mot[::-1]

if __name__ == "__main__":
    print(est_palindrome("radar"))  # True
    print(est_palindrome("python"))  # False
    print(est_palindrome("a"))  # True
    print(est_palindrome(""))  # True
