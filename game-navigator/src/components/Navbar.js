import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import { FaUserCircle } from 'react-icons/fa';
import '../css/Navbar.css';

const Navbar = () => {
  const { isAuthenticated } = useAuth();
  const { setIsAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await fetch('/api/logout/', {
        method: 'POST',
        credentials: 'include', 
    });
    setIsAuthenticated(false);
    navigate('/login');
};

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          Game Navigator
        </Link>
        
        <ul className="nav-menu">
          {isAuthenticated ? (
            <>
              <li className="nav-item">
                <Link to="/profile" className="nav-links"><FaUserCircle className="nav-links" /></Link>
              </li>
              <li className="nav-item">
                <button onClick={handleLogout} className="nav-links btn-logout">Logout</button>
              </li>
            </>
          ) : (
            <>
              <li className="nav-item">
                <Link to="/login" className="nav-links">
                  Login
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/signup" className="nav-links">
                  Sign Up
                </Link>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
