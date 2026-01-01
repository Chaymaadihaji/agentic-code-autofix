```typescript
// src/App.tsx

import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ProjectProvider } from './contexts/ProjectContext';
import { NotificationProvider } from './contexts/NotificationContext';
import AppRouter from './routers/AppRouter';
import './styles/index.css';

interface Props {}

const App: React.FC<Props> = () => {
  return (
    <AuthProvider>
      <ProjectProvider>
        <NotificationProvider>
          <BrowserRouter>
            <AppRouter />
          </BrowserRouter>
        </NotificationProvider>
      </ProjectProvider>
    </AuthProvider>
  );
};

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

// src/contexts/AuthContext.ts

import { createContext, useState, useEffect } from 'react';
import axios from 'axios';

interface AuthContextProps {}

const AuthContext = createContext<AuthContextProps>({} as AuthContextProps);

const AuthProvider: React.FC<AuthContextProps> = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      axios
        .get('/api/auth/user', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          setUser(response.data);
        })
        .catch((error) => {
          console.error(error);
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (loginData: any) => {
    try {
      const response = await axios.post('/api/auth/login', loginData);
      localStorage.setItem('token', response.data.token);
      setUser(response.data.user);
    } catch (error) {
      console.error(error);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthProvider, AuthContext };

// src/contexts/ProjectContext.ts

import { createContext, useState } from 'react';

interface ProjectContextProps {}

const ProjectContext = createContext<ProjectContextProps>({} as ProjectContextProps);

const ProjectProvider: React.FC<ProjectContextProps> = ({ children }) => {
  const [projects, setProjects] = useState([]);

  const addProject = async (projectData: any) => {
    try {
      const response = await axios.post('/api/projects', projectData);
      setProjects([...projects, response.data]);
    } catch (error) {
      console.error(error);
    }
  };

  const updateProject = async (projectId: string, projectData: any) => {
    try {
      const response = await axios.put(`/api/projects/${projectId}`, projectData);
      setProjects(
        projects.map((project) =>
          project._id === projectId ? response.data : project
        )
      );
    } catch (error) {
      console.error(error);
    }
  };

  const deleteProject = async (projectId: string) => {
    try {
      await axios.delete(`/api/projects/${projectId}`);
      setProjects(projects.filter((project) => project._id !== projectId));
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <ProjectContext.Provider value={{ projects, addProject, updateProject, deleteProject }}>
      {children}
    </ProjectContext.Provider>
  );
};

export { ProjectProvider, ProjectContext };

// src/contexts/NotificationContext.ts

import { createContext, useState } from 'react';
import axios from 'axios';

interface NotificationContextProps {}

const NotificationContext = createContext<NotificationContextProps>({} as NotificationContextProps);

const NotificationProvider: React.FC<NotificationContextProps> = ({ children }) => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const socket = io();
    socket.on('new-notification', (notification) => {
      setNotifications([...notifications, notification]);
    });
    return () => {
      socket.disconnect();
    };
  }, []);

  const readNotification = async (notificationId: string) => {
    try {
      await axios.put(`/api/notifications/${notificationId}`, { read: true });
      setNotifications(
        notifications.map((notification) =>
          notification._id === notificationId ? { ...notification, read: true } : notification
        )
      );
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <NotificationContext.Provider value={{ notifications, loading, readNotification }}>
      {children}
    </NotificationContext.Provider>
  );
};

export { NotificationProvider, NotificationContext };

// src/routers/AppRouter.ts

import React from 'react';
import { Route, Switch } from 'react-router-dom';
import Login from './Login';
import Projects from './Projects';
import Project from './Project';

const AppRouter: React.FC = () => {
  return (
    <Switch>
      <Route path="/login" component={Login} />
      <Route path="/projects" component={Projects} />
      <Route path="/projects/:id" component={Project} />
    </Switch>
  );
};

export default AppRouter;

// src/components/Login.tsx

import React, { useState } from 'react';
import axios from 'axios';

interface Props {}

const Login: React.FC<Props> = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const response = await axios.post('/api/auth/login', { email, password });
      localStorage.setItem('token', response.data.token);
    } catch (error) {
      setError(error.response.data.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
      <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
      <button type="submit">Se connecter</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </form>
  );
};

export default Login;

// src/components/Projects.tsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Project from './Project';
import { useProjectContext } from '../contexts/ProjectContext';

interface Props {}

const Projects: React.FC<Props> = () => {
  const { projects, addProject } = useProjectContext();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const projectData = { name: 'Projet 1', description: 'Ce projet est très important' };
      await addProject(projectData);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Projets</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Nom du projet" />
        <input type="text" placeholder="Description du projet" />
        <button type="submit">Ajouter un projet</button>
      </form>
      {projects.map((project) => (
        <Project key={project._id} project={project} />
      ))}
    </div>
  );
};

export default Projects;

// src/components/Project.tsx

import React from 'react';
import axios from 'axios';
import { useProjectContext } from '../contexts/ProjectContext';

interface Props {
  project: any;
}

const Project: React.FC<Props> = ({ project }) => {
  const { updateProject, deleteProject } = useProjectContext();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const projectData = { name: 'Projet 1 modifié', description: 'Ce projet est très important' };
      await updateProject(project._id, projectData);
    } catch (error) {
      console.error(error);
    }
  };

  const handleDelete = async () => {
    try {
      await deleteProject(project._id);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>{project.name}</h1>
      <p>{project.description}</p>
      <form onSubmit={handleSubmit}>
        <input type="text" value={project.name} />
        <input type="text" value={project.description} />
        <button type="submit">Modifier le projet</button>
      </form>
      <button type="button" onClick={handleDelete}>
        Supprimer le projet
      </button>
    </div>
  );
};

export default Project;

// src/api/auth.ts

import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:3001',
});

export const login = (loginData: any) => api.post('/auth/login', loginData);
export const logout = () => api.post('/auth/logout');
export const getUser = () => api.get('/auth/user');

// src/api/projects.ts

import axios from
