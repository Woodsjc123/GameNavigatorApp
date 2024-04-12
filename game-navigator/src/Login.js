import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

import './css/Login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const { setIsAuthenticated } = useAuth();

  const handleSubmit = async (event) => {
    event.preventDefault();

    const getCsrfToken = () => {
      const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1];
      return csrfToken;
    };

    try {
      const response = await fetch('/api/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        credentials: 'include', 
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        console.log('Login successful');
        setIsAuthenticated(true);
        navigate('/games');
      } else {
        console.error('Login failed: Invalid username or password');
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <div className="form-container">
      <h1>Log in</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Login</button>
        <button type="button" onClick={() => {/* handle forgot password logic */}}>Forgot Password?</button>
      </form>
    </div>
  );
}

export default Login;
