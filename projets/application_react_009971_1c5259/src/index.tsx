typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import store from './store/configureStore';
import App from './App';
import 'tailwindcss/base';
import './styles/global.css';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

root.render(
  <Provider store={store}>
    <App />
  </Provider>
);

// API REST
interface Response {
  data: any;
  error: string;
}

async function fetchApiData(url: string): Promise<Response> {
  try {
    const response = await fetch(url);
    const data = await response.json();
    if (response.ok) {
      return { data, error: '' };
    } else {
      return { data: null, error: data.message };
    }
  } catch (error) {
    return { data: null, error: 'Erreur de connexion' };
  }
}

// pagination
class PaginatedList {
  private data: any[];
  private currentPage: number;
  private pageSize: number;
  private totalPages: number;

  constructor(data: any[], pageSize: number) {
    this.data = data;
    this.pageSize = pageSize;
    this.currentPage = 1;
    this.totalPages = this.getTotalPages();
  }

  getTotalPages(): number {
    const totalPages = Math.ceil(this.data.length / this.pageSize);
    return totalPages;
  }

  getCurrentPageData(): any[] {
    const start = (this.currentPage - 1) * this.pageSize;
    const end = start + this.pageSize;
    return this.data.slice(start, end);
  }

  getNextPage(): void {
    if (this.currentPage === this.totalPages) return;
    this.currentPage += 1;
  }

  getPreviousPage(): void {
    if (this.currentPage === 1) return;
    this.currentPage -= 1;
  }
}

// fonctionnalité principale
function fonctionnalitePrincipale(): void {
  const url = 'http://localhost:3000/data'; // exemple d'adresse de l'API
  const fetchResult = fetchApiData(url);
  fetchResult.then((response) => {
    if (response.data) {
      const dataList = response.data;
      const pageSize = 10;
      const paginatedList = new PaginatedList(dataList, pageSize);
      console.log(paginatedList);
    } else if (response.error) {
      console.error(response.error);
    }
  });
}

fonctionnalitePrincipale();
