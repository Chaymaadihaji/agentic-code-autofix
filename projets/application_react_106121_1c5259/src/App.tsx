typescript
// src/App.tsx

import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';

import AppRouter from './routes/AppRouter';
import { store } from './store/configureStore';

import './styles/tailwind.css';

interface IError {
  code: number;
  message: string;
}

interface IRessource {
  id: number;
  titre: string;
  contenu: string;
}

interface IResponse {
  data: IRessource[];
  meta: IMeta;
}

interface IMeta {
  page: number;
  per_page: number;
  total: number;
  links: Links;
}

interface Links {
  first: string;
  last: string;
  next: string;
  prev: string;
}

const App = () => {
  const [resources, setResources] = React.useState<IRessource[]>([]);
  const [load, setLoad] = React.useState(false);
  const [hasPrev, setHasPrev] = React.useState(false);
  const [hasNext, setHasNext] = React.useState(false);
  const [page, setPage] = React.useState(1);
  const [perPage, setPerPage] = React.useState(10);
  const [total, setTotal] = React.useState(0);
  const [error, setError] = React.useState<IError | null>(null);

  const getResource = React.useCallback(async (page: number, perPage: number) => {
    try {
      setLoad(true);
      setError(null);
      const response: IResponse = await fetch(`https://api.example.com/resources?page=${page}&per_page=${perPage}`)
        .then(response => response.json())
        .catch((e: any) => {
          setError({ code: e.status, message: e.statusText });
          throw e;
        });

      setResources(response.data);
      setTotal(response.meta.total);
      setPerPage(perPage);
      setPage(page);
      setLoad(false);
      setHasPrev(response.meta.links.prev !== null);
      setHasNext(response.meta.links.next !== null);
    } catch {
      setError({ code: 500, message: 'Erreur serveur' });
    }
  }, []);

  const handlePrev = () => {
    if (hasPrev) getResource(page - 1, perPage);
  };

  const handleNext = () => {
    if (hasNext) getResource(page + 1, perPage);
  };

  const loadResources = React.useCallback(() => getResource(page, perPage), [page, perPage, getResource]);

  React.useEffect(() => {
    loadResources();
  }, [loadResources]);

  const handleRefresh = () => {
    loadResources();
  };

  const [refreshState, setRefreshState] = React.useState(false);

  const refresh = () => {
    setRefreshState(true);
    loadResources();
    setTimeout(() => setRefreshState(false), 2000);
  };

  const handleDelete = (id: number) => {
    // Gestion de la suppression de l'entité
    getResource(page, perPage);
  };

  const handleEdit = (id: number) => {
    // Gestion de l'édition de l'entité
    getResource(page, perPage);
  };

  const refreshData = React.useCallback(() => {
    getResource(page, perPage);
  }, [page, perPage, getResource]);

  return (
    <Provider store={store}>
      <BrowserRouter>
        <main className="container mx-auto p-4 mt-10">
          <h1 className="text-3xl font-bold my-4">Liste des ressources</h1>
          <div className="my-4">{error && <p>Error code: {error.code} - {error.message}</p>}</div>
          <div className="flex justify-between">
            <button
              onClick={handleRefresh}
              className={({ loading, active }) => loading ? 'bg-gray-700 text-white cursor-not-allowed' : active ? 'bg-blue-500 hover:bg-blue-700 text-white' : 'bg-gray-100 hover:bg-gray-200 text-gray-900'}
            >
              {refreshState ? 'Chargement...' : 'Recharger'}
            </button>
            <div>
              <p>page {page}</p>
              <p>{hasPrev ? <a onClick={handlePrev}>Précédante</a> : <span>Précédante</span>}</p>
              <p>{hasNext ? <a onClick={handleNext}>Suivante</a> : <span>Suivante</span>}</p>
            </div>
          </div>
          <ul>
            {resources.map(r => (
              <li key={r.id}>
                {r.titre} - {r.contenu}
              </li>
            ))}
          </ul>
        </main>
      </BrowserRouter>
    </Provider>
  );
};

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
