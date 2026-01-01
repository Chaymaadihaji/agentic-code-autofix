# tests.py

import unittest
from unittest.mock import MagicMock
from app import db, create_app
from app.models import Livre, Membre, Emprunt
from app.services import LivreService, MembreService, EmpruntService
from app.utils import generate_jwt

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_livre_service(self):
        service = LivreService(db.session)
        livre = Livre titre='Le Seigneur des Anneaux', auteur='J.R.R. Tolkien'
        db.session.add(livre)
        db.session.commit()
        livre = service.get_by_id(livre.id)
        self.assertEqual(livre.titre, 'Le Seigneur des Anneaux')

    def test_membre_service(self):
        service = MembreService(db.session)
        membre = Membre nom='Jean Dupont', email='jean.dupont@example.com'
        db.session.add(membre)
        db.session.commit()
        membre = service.get_by_email(membre.email)
        self.assertEqual(membre.nom, 'Jean Dupont')

    def test_emprunt_service(self):
        service = EmpruntService(db.session)
        livre = Livre titre='Le Seigneur des Anneaux', auteur='J.R.R. Tolkien'
        membre = Membre nom='Jean Dupont', email='jean.dupont@example.com'
        db.session.add(livre)
        db.session.add(membre)
        db.session.commit()
        emprunt = service.create(livre.id, membre.id)
        self.assertIsNotNone(emprunt)

    def test_authentification_jwt(self):
        jwt = generate_jwt('jean.dupont@example.com')
        self.assertIsNotNone(jwt)

class TestApi(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_api_livres(self):
        client = self.app.test_client()
        response = client.get('/livres')
        self.assertEqual(response.status_code, 200)

    def test_api_membres(self):
        client = self.app.test_client()
        response = client.get('/membres')
        self.assertEqual(response.status_code, 200)

    def test_api_emprunts(self):
        client = self.app.test_client()
        response = client.get('/emprunts')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
