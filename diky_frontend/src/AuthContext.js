import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userId, setUserId] = useState(null);
    const [first_name, setFirstName] = useState('');
    const [last_name, setLastName] = useState('');

    const login = (id, first_name, last_name) => {
        setIsLoggedIn(true);
        setUserId(id);
        setFirstName(first_name);
        setLastName(last_name);
    };

    const logout = () => {
        setIsLoggedIn(false);
        setUserId(null);
    };

    return (
        <AuthContext.Provider value={{ isLoggedIn, userId, first_name, last_name, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);