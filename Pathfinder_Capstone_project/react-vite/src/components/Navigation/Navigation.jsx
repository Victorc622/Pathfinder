import React from "react";
import { Link } from "react-router-dom";
import styles from "./Navigation.module.css";

const Navigation = () => {
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
            <Link to="/about">About</Link>
          </li>
          <li>
            <Link to="/contact">Contact</Link>
          </li>
        </ul>
      </nav>
      <div className={styles.actions}>
        <Link to="/login" className={styles.login}>
          Log In
        </Link>
        <Link to="/signup" className={styles.signup}>
          Sign Up
        </Link>
      </div>
    </header>
  );
};

export default Navigation;