typescript
// src/App.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import { Provider } from 'react-redux';
import { store } from './store';
import SocketManager from './services/SocketManager';
import Upload from './components/Upload';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

type Props = {
  store: any;
};

function Root(props: Props) {
  return (
    <Provider store={props.store}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="register" element={<Register />} />
          <Route path="dashboard" element={<Dashboard />} />
        </Routes>
      </BrowserRouter>
      <SocketManager />
      <Upload />
    </Provider>
  );
}

root.render(
  <React.StrictMode>
    <Root store={store} />
  </React.StrictMode>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
