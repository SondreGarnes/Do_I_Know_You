import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import Login from './Login';
import Home from './Home';
import Register from './Register';
import FriendGraph from './FriendGraph';

const App = () => {
    return (
        <AuthProvider>
            <Router>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/friend_graph" element={<FriendGraph />} />
                </Routes>
            </Router>
        </AuthProvider>
    );
};

export default App;