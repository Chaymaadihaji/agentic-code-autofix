typescript
// src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, configureStore } from '@reduxjs/toolkit';
import { rootReducer } from './reducers';
import App from './App';
import 'tailwindcss/tailwind.css';
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000/api';

interface RootState {
  reducer: any;
}

const store = configureStore({ reducer: rootReducer });

interface AppProps {
  className?: string;
}

function AppWrapper({ children, className }: AppProps) {
  return (
    <div className={className}>
      {children}
    </div>
  );
}

ReactDOM.render(
  <React.StrictMode>
    <Provider store={store}>
      <AppWrapper className="min-h-screen p-4">
        <App />
      </AppWrapper>
    </Provider>
  </React.StrictMode>,
  document.getElementById('root')
);

// pagination
interface PaginateResponse<T> {
  items: T[];
  metaData: {
    page: number;
    limit: number;
    total: number;
  };
}

const paginate = async <T>(
  fetchFunc: () => Promise<PaginateResponse<T>>,
  limit: number,
  pageNumber: number
): Promise<PaginateResponse<T>> => {
  const response = await fetchFunc();
  if (pageNumber <= response.metaData.page) {
    const metaData = response.metaData;
    const offset = (pageNumber - 1) * metaData.limit;
    return await fetchFunc();
  }
  return response;
};

// exemple d'utilisation
const fetchUsers = async () => {
  const response = await axios.get<PaginateResponse<{ id: number; name: string }>>(
    `/users?limit=10&page=1`
  );
  return response.data;
};

const fetchMoreUsers = (pageNumber = 2) =>
  paginate(fetchUsers, 10, pageNumber);

fetchMoreUsers(2).then((response) => {
  if (response.metaData.total > response.metaData.limit * 2) {
    return fetchMoreUsers(
      parseInt(response.metaData.page.toString()) + 1
    ).then((responseTwo) => {
      console.log(responseTwo);
      return responseTwo;
    });
  }
  console.log(response);
  // Do something with the response
  return response;
});
