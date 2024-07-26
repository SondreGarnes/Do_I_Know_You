import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [first_name, setFirstName] = useState('');
    const [last_name, setLastName] = useState('');

    const login = (first_name, last_name) => {
        setIsLoggedIn(true);
        setFirstName(first_name);
        setLastName(last_name);
    };

    const logout = () => {
        setIsLoggedIn(false);
    };

    return (
        <AuthContext.Provider value={{ isLoggedIn, first_name, last_name, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);