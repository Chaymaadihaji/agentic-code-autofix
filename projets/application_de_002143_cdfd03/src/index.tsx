typescript
// src/index.tsx

import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { Provider } from 'react-redux';
import store from './store/store';
import { BrowserRouter } from 'react-router-dom';
import { SocketProvider } from './components/contexts/SocketContext';
import SocketIO from 'socket.io-client';

// Configuration Socket
const socketUrl = 'http://localhost:8080';
const io = SocketIO(socketUrl);

// Configuration du store Redux
const initialState = {
  auth: {
    token: localStorage.getItem('token'),
    user: JSON.parse(localStorage.getItem('user')),
  },
};

// Code principal
ReactDOM.render(
  <React.StrictMode>
    <Provider store={store}>
      <SocketProvider socket={io}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </SocketProvider>
    </Provider>
  </React.StrictMode>,
  document.getElementById('root')
);

// Configuration Express
import express, { Request, Response, NextFunction } from 'express';
const app = express();
const port = 3000;

// Gestion des erreurs Express
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err);
  res.status(500).send({ message: 'Erreur serveur' });
});

// Gestion des requêtes Express
app.get('/api/health', (req: Request, res: Response) => {
  res.send({ message: 'Server en marche' });
});

app.listen(port, () => {
  console.log(`Server en écoute sur le port ${port}`);
});

// Configuration Node
import mongoose from 'mongoose';

mongoose.connect('mongodb://localhost/projet', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});
mongoose.Promise = global.Promise;

const db = mongoose.connection;

db.on('error', (err) => {
  console.error(err);
});

db.once('open', () => {
  console.log('Base de données connectée');
});

// Configuration authentification
import auth from './controllers/auth';

app.post('/auth', auth.login);
