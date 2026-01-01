from setuptools import setup, find_packages

setup(
    name='bibliotheque',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask_jwt_extended',
        'streamlit',
        'PyPDF2',
        'requests',
        'sqlite3',
        'pandas',
        'numpy'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'flake8',
            'black'
        ]
    },
    author='Nom de l\'auteur',
    author_email='email@domaine.com',
    description='Application de gestion de bibliothèque'
)
