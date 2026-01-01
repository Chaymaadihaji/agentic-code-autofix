typescript
// src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './store/store';
import { AuthProvider } from './contexts/authContext';
import { SocketProvider } from './contexts/socketContext';
import { ProjectPage } from './pages/projectPage';
import { Login } from './pages/login';
import { Signup } from './pages/signup';
import { Dashboard } from './pages/dashboard';
import { ProjectCreate } from './pages/projectCreate';
import { ProjectDetails } from './pages/projectDetails';
import { Projects } from './pages/projects';
import { Notifications } from './pages/notifications';

function App() {
  return (
    <AuthProvider>
      <SocketProvider>
        <Provider store={store}>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/projects" element={<Projects />} />
              <Route path="/project/:id" element={<ProjectDetails />} />
              <Route path="/project/create" element={<ProjectCreate />} />
              <Route path="/notifications" element={<Notifications />} />
            </Routes>
          </BrowserRouter>
        </Provider>
      </SocketProvider>
    </AuthProvider>
  );
}

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
