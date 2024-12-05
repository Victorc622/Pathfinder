import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Navigate, useNavigate } from "react-router-dom";
import { thunkLogin } from "../../redux/session";
import './LoginForm.css';

function LoginFormPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const sessionUser = useSelector((state) => state.session.user);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (sessionUser) {
      navigate("/");
    }
  }, [sessionUser, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = { email, password };
    const response = await dispatch(thunkLogin(data));

    if (response.errors) {
      setErrors(response.errors);
    } else {
      navigate("/");
    }
  };

  const handleDemoLogin = async () => {
    const demoCredentials = { email: "demo@aa.io", password: "password" };
    const response = await dispatch(thunkLogin(demoCredentials));

    if (response.errors) {
      setErrors(response.errors);
    } else {
      navigate("/");
    }
  };

  return (
    <div className="login-form-container">
      <h2>Login to Pathfinder</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          {errors.email && <p className="error">{errors.email}</p>}
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {errors.password && <p className="error">{errors.password}</p>}
        </div>
        <button type="submit" className="form-button">
          Log In
        </button>
        <button type="button" onClick={handleDemoLogin} className="form-button demo-button">
          Log in as Demo User
        </button>
        <button type="button" onClick={() => navigate("/signup")} className="form-button">
          Sign Up
        </button>
      </form>
    </div>
  );
}

export default LoginFormPage;