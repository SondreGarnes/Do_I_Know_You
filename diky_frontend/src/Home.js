
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from './AuthContext';
const Home = () => {
    const {isLoggedIn, logout, first_name, last_name} = useAuth();
    return (
        <div>
            <h1>Welcome to the Home Page</h1>
            <p>This is the home page of the application.</p>
            <nav>
                {isLoggedIn ? (
                    <div> 
                        <p>Welcome, {first_name + " " + last_name}!</p>
                        <button onClick={logout}>Logout</button>
                    </div>
                ) : (
                    <div>
                        <Link to="/login">Login</Link>
                        <Link to="/register">Register</Link>
                    </div>
                )}
            </nav>
        </div>
    );
};

export default Home;