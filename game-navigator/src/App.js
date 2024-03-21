import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/navbar';
import Login from './Login';
import Signup from './signup';
import GameList from './GameList';
import { AuthProvider } from './AuthContext';
import ProtectedRoute from './components/ProtectedRoute'
import './App.css';


function App() {

  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <div className="app-content">
          <Routes>
            <Route path="/login" element={<Login setAuth={<Login />} />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/games" element={<ProtectedRoute><GameList /></ProtectedRoute>} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
