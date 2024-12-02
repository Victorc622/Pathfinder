import { useState } from "react";
import { thunkLogin } from "../../redux/session";
import { useDispatch, useSelector } from "react-redux";
import { Navigate, useNavigate } from "react-router-dom";
import "./LoginForm.css";

function LoginFormPage() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const sessionUser = useSelector((state) => state.session.user);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState([]);

  if (sessionUser) return <Navigate to="/" replace={true} />;

  const handleSubmit = async (e) => {
    e.preventDefault();

    const serverResponse = await dispatch(
      thunkLogin({
        email,
        password,
      })
    );

    if (serverResponse) {
      setErrors(Object.values(serverResponse));
    } else {
      navigate("/");
    }
  };

  const handleDemoLogin = async () => {
    const serverResponse = await dispatch(
      thunkLogin({
        email: "demo@aa.io",
        password: "password",
      })
    );

    if (serverResponse) {
      setErrors(Object.values(serverResponse));
    } else {
      navigate("/");
    }
  };

  return (
    <div className="form-container">
      <h1 className="form-title">Log In</h1>
      {errors.length > 0 && (
        <div className="error-messages">
          {errors.map((message, index) => (
            <p key={index} className="error-text">
              {message}
            </p>
          ))}
        </div>
      )}
      <form onSubmit={handleSubmit} className="form">
        <label className="form-label">
          Email
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="form-input"
          />
        </label>
        <label className="form-label">
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="form-input"
          />
        </label>
        <button type="submit" className="form-button">
          Log In
        </button>
        <button type="button" onClick={handleDemoLogin} className="form-button demo-button">
          Log in as Demo User
        </button>
      </form>
    </div>
  );
}

export default LoginFormPage;