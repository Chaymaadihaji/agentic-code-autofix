typescript
// src/App.tsx

import React from 'react';
import ReactDOM from 'react-dom';
import AppRouter from './router/AppRouter';
import { Provider } from 'react-redux';
import store from './store/store';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/Toastify.css';
import { SocketContextProvider } from './context/socket';

ReactDOM.render(
  <React.StrictMode>
    <Provider store={store}>
      <SocketContextProvider>
        <AppRouter />
        <ToastContainer />
      </SocketContextProvider>
    </Provider>
  </React.StrictMode>,
  document.getElementById('root')
);
