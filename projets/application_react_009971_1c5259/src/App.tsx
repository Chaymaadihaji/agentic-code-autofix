typescript
import React, { useState, useEffect } from 'react';
import { Provider } from 'react-redux';
import store from './store';
import AppRouter from './AppRouter';
import { Container } from '@chakra-ui/react';

function App() {
  return (
    <Provider store={store}>
      <Container maxW="100%" p={4}>
        <AppRouter />
      </Container>
    </Provider>
  );
}

export default App;
