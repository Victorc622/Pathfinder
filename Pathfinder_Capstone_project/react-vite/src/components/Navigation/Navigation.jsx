import React, { useState, useEffect, useRef } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { thunkLogout } from "../../redux/session";
import styles from "./Navigation.module.css";

const Navigation = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const user = useSelector((store) => store.session.user);
  const [showMenu, setShowMenu] = useState(false);
  const menuRef = useRef();

  const toggleMenu = (e) => {
    e.stopPropagation();
    setShowMenu(!showMenu);
  };

  const logout = async (e) => {
    e.preventDefault();
    try {
      await dispatch(thunkLogout());
      navigate("/login");
    } catch (error) {
      console.error("Logout failed:", error);
    }
    setShowMenu(false);
  };

  useEffect(() => {
    const closeMenu = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setShowMenu(false);
      }
    };

    if (showMenu) {
      document.addEventListener("click", closeMenu);
    }

    return () => {
      document.removeEventListener("click", closeMenu);
    };
  }, [showMenu]);

  return (
    <header className={styles.navigation}>
      <div className={styles.logo}>
        <Link to="/">Pathfinder</Link>
      </div>
      <nav className={styles.nav}>
        <ul>
          <li>
            <Link to="/itinerary">Itinerary</Link>
          </li>
          <li>
            <Link to="/destinations">Destination</Link>
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
        {user ? (
          <div className={styles.profileMenu} ref={menuRef}>
            <button onClick={toggleMenu} className={styles.profileButton}>
              {user.username}
            </button>
            {showMenu && (
              <ul className={styles.profileDropdown}>
                <li>
                  <span>{user.email}</span>
                </li>
                <li>
                  <button onClick={logout} className={styles.logoutButton}>
                    Log Out
                  </button>
                </li>
              </ul>
            )}
          </div>
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
