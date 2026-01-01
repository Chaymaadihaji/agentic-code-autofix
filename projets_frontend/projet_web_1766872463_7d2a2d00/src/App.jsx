javascript
// src/App.jsx

import React from 'react';
import { Provider } from 'react-redux';
import store from './store';
import axios from 'axios';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MuiThemeProvider, createTheme } from '@mui/material/styles';
import theme from './theme';
import Home from './pages/Home';
import ErrorPage from './pages/ErrorPage';

axios.defaults.headers.common['Authorization'] = 'Bearer votre-clé-d\'autorisation';

const App = () => {
  return (
    <Provider store={store}>
      <MuiThemeProvider theme={theme}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/erreur" element={<ErrorPage />} />
            <Route path="*" element={<ErrorPage />} />
          </Routes>
        </BrowserRouter>
      </MuiThemeProvider>
    </Provider>
  );
};

export default App;
