import React, { useState } from 'react';
import { loginUser } from './apiService';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const { login } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await loginUser({ email, password });
            console.log(response.data);
            login(response.data.first_name, response.data.last_name);
            navigate('/');
        }
        catch (error) {
            console.log(error);
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;