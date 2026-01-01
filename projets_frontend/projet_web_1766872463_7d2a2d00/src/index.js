javascript
// src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, configureStore } from '@reduxjs/toolkit';
import axios from 'axios';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import App from './App';
import reducers from './reducers';

const theme = createMuiTheme({
  palette: {
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#f44336',
    },
  },
});

const store = configureStore({
  reducer: reducers,
});

axios.defaults.baseURL = 'https://jsonplaceholder.typicode.com';

const handleError = (error) => {
  console.error(error);
};

const Index = () => {
  return (
    <Provider store={store}>
      <MuiThemeProvider theme={theme}>
        <App />
      </MuiThemeProvider>
    </Provider>
  );
};

ReactDOM.render(
  <React.StrictMode>
    <Index />
  </React.StrictMode>,
  document.getElementById('root')
);
