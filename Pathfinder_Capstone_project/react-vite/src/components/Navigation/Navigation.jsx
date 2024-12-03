import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import styles from "./Navigation.module.css";

const Navigation = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const response = await fetch('/api/auth/check-login-status', { credentials: 'include' });
        if (response.ok) {
          setIsLoggedIn(true);
        } else {
          setIsLoggedIn(false);
        }
      } catch (error) {
        console.error('Error checking login status:', error);
      }
    };

    checkLoginStatus();
  }, []);

  const handleSignOut = async () => {
    try {
      const response = await fetch('/api/auth/logout', {
        method: 'POST',
        credentials: 'include',
      });

      if (response.ok) {
        setIsLoggedIn(false);
        navigate('/login');
      } else {
        console.error('Error logging out');
      }
    } catch (error) {
      console.error('Error during sign-out:', error);
    }
  };

  return (
    <header className={styles.navigation}>
      <div className={styles.logo}>
        <Link to="/">Pathfinder</Link>
      </div>
      <nav className={styles.nav}>
        <ul>
          <li>
            <Link to="/trips">My Trips</Link>
          </li>
          <li>
            <Link to="/itinerary">Itinerary</Link>
          </li>
          <li>
            <Link to="/destinations">Destinations</Link>
          </li>
          <li>
            <Link to="/collaboration">Collaboration</Link>
          </li>
          <li>
            <Link to="/activities">Activities</Link>
          </li>
        </ul>
      </nav>
      <div className={styles.actions}>
        {isLoggedIn ? (
          <button onClick={handleSignOut} className={styles.login}>
            Log Out
          </button>
        ) : (
          <>
            <Link to="/login" className={styles.login}>
              Log In
            </Link>
            <Link to="/signup" className={styles.signup}>
              Sign Up
            </Link>
          </>
        )}
      </div>
    </header>
  );
};

export default Navigation;