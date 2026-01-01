javascript
// src/index.js

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { createStore, combineReducers, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import reducer from './reducers';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { PersistGate } from 'redux-persist/integration/react';

// Import les composants
import Login from './components/Login';
import Register from './components/Register';
import TodoList from './components/TodoList';
import TodoForm from './components/TodoForm';

// Import les styles
import './index.css';

// Import les librairies
import { TailwindProvider } from 'tailwindcss/react';
import 'tailwindcss/base';
import 'tailwindcss/components';
import 'tailwindcss/utilities';

// Créer le store Redux
const persistConfig = {
  key: 'root',
  storage,
};

const persistedReducer = persistReducer(persistConfig, reducer);

const store = createStore(
  persistedReducer,
  applyMiddleware(thunk)
);

const persistor = persistStore(store);

// Fonction de connexion à la base de données
async function connectToDatabase() {
  try {
    // Connexion à la base de données MongoDB
    const mongoose = require('mongoose');
    await mongoose.connect('mongodb://localhost:27017/todo-list', {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log('Connexion à la base de données réussie');
  } catch (error) {
    console.error('Erreur de connexion à la base de données:', error);
  }
}

// Fonction de déconnexion de la base de données
async function disconnectFromDatabase() {
  try {
    // Déconnexion de la base de données MongoDB
    const mongoose = require('mongoose');
    await mongoose.disconnect();
    console.log('Déconnexion de la base de données réussie');
  } catch (error) {
    console.error('Erreur de déconnexion de la base de données:', error);
  }
}

// Fonction principale
async function main() {
  await connectToDatabase();
  const root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(
    <React.StrictMode>
      <Provider store={store}>
        <PersistGate persistor={persistor}>
          <BrowserRouter>
            <TailwindProvider>
              <App />
            </TailwindProvider>
          </BrowserRouter>
        </PersistGate>
      </Provider>
    </React.StrictMode>
  );
  reportWebVitals();
}

// Exécuter la fonction principale
main();

// Import les routes
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

// Import les composants
import Home from './components/Home';
import Profile from './components/Profile';

// Créer les routes
const routes = (
  <Switch>
    <Route path="/" exact component={Home} />
    <Route path="/login" component={Login} />
    <Route path="/register" component={Register} />
    <Route path="/profile" component={Profile} />
  </Switch>
);

// Créer le composant App
function App() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold">Todo List</h1>
      <Switch>
        <Route path="/login" component={Login} />
        <Route path="/register" component={Register} />
        <Route path="/profile" component={Profile} />
        <Route path="/" exact component={Home} />
      </Switch>
    </div>
  );
}

// Export les composants
export { App, Login, Register, TodoList, TodoForm, Home, Profile };
