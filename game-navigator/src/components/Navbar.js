import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import { FaUserCircle } from 'react-icons/fa';
import '../css/Navbar.css';

function Navbar() {
  const { isAuthenticated } = useAuth();
  const { setIsAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {

    const getCsrfToken = () => {
      const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1];
      return csrfToken;
    };
  
    await fetch('/api/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        credentials: 'include', 
    }).then(response => {
      if (response.ok) {
        setIsAuthenticated(false);
        navigate('/login');
      } else {
        console.error('Failed to log out.');
      }
    }).catch(error => console.error('Error:', error));
  };

  return (
    <nav className="navbar">
      <div className="navbar-div">
        <Link to="/" className="nav-logo">
          Game Navigator
        </Link>
        
        <ul className="nav-menu">
          {isAuthenticated ? (
            <>
              <li className="nav-item">
                <Link to="/games" className="nav-links">Games</Link>
              </li>
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
