import React, { useState } from 'react';

import './css/Login.css'

function SignUp({ setAuth }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch('/api/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password, email }),
      });
      if (response.ok) {
        console.log('Registration successful');
        setAuth(true);
      } else {
        const data = await response.json();
        console.error('Registration failed:', data.error);
      }
    } catch (error) {
      console.error('Registration error:', error);
    }
  };

  return (
    <div className="form-container">
      <h1>Sign Up</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          required
        />
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <input
          type="confirm-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Confirm Password"
          required
        />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default SignUp;
