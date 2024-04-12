import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './Login';
import Signup from './Signup';
import Profile from './Profile';
import GameList from './GameList';
import { AuthProvider } from './AuthContext';
import ProtectedRoute from './components/ProtectedRoute'
import ForgotPassword from './Forgotpassword';
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
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/games" element={<ProtectedRoute><GameList /></ProtectedRoute>} />
            <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
