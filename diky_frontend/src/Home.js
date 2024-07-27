import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { getUsers, addFriend } from './apiService';

const Home = () => {
    const { isLoggedIn, logout, first_name, last_name, userId } = useAuth();
    const [users, setUsers] = useState([]);

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await getUsers();
                setUsers(response.data);
            } catch (error) {
                console.error("Error fetching users:", error);
            }
        };

        
        fetchUsers();
       
    }, []);

    const handleAddFriend = async (friendId) => {
        try {
            const response = await addFriend({ user1_id: userId, user2_id: friendId });
            console.log("Friend added:", response.data);
        } catch (error) {
            console.error("Error adding friend:", error);
        }
    };

    return (
        <div>
            <h1>Welcome to the Home Page</h1>
            <p>This is the home page of the application.</p>
            <nav>
                {isLoggedIn ? (
                    <div>
                        <p>Welcome, {first_name + " " + last_name}!</p>
                        <button onClick={logout}>Logout</button>
                        <h2>Other Users</h2>
                        <ul>
                            {users.filter(user => user.id !== userId).map(user => (
                                <li key={user.id}>
                                    {user.first_name} {user.last_name}
                                    <button onClick={() => handleAddFriend(user.id)}>Add Friend</button>
                                </li>
                            ))}
                        </ul>
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