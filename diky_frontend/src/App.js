// src/App.js
import React from 'react';
import Login from './Login';
import Register from './Register';

const App = () => {
    return (
        <div>
            <h1>My App</h1>
            <Register />
            <Login />
        </div>
    );
};

export default App;