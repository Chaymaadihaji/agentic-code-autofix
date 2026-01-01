typescript
// src/App.tsx

import React, { useState, useEffect } from 'react';
import './App.css';

interface Post {
  id: number;
  title: string;
  body: string;
  userId: number;
}

const API_URL = 'https://jsonplaceholder.typicode.com/posts';

const App = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [perPage, setPerPage] = useState(10);

  const fetchPosts = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}?_page=${page}&_limit=${perPage}`);
      const data = await response.json();
      setPosts(data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, [page, perPage]);

  const handleChangePage = (newPage: number) => {
    setPage(newPage);
  };

  const handleChangePerPage = (newPerPage: number) => {
    setPerPage(newPerPage);
  };

  return (
    <div className="App">
      <h1>Tableau de données</h1>
      <button onClick={() => handleChangePage(page - 1)}>Précédent</button>
      <button onClick={() => handleChangePage(page + 1)}>Suivant</button>
      <select onChange={(e) => handleChangePerPage(parseInt(e.target.value, 10))}>
        <option value="5">5 par page</option>
        <option value="10">10 par page</option>
        <option value="20">20 par page</option>
      </select>
      {loading ? <p>Veuillez patienter...</p> : null}
      {error ? <pErreur d'application</p> : null}
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Titre</th>
            <th>Contenu</th>
            <th_Utilisateur ID</th>
          </tr>
        </thead>
        <tbody>
          {posts.map((post, index) => (
            <tr key={post.id}>
              <td>{post.id}</td>
              <td>{post.title}</td>
              <td>{post.body}</td>
              <td>{post.userId}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;
