import { useState } from "react";
import { useDispatch } from "react-redux";
import { thunkLogin } from "../../redux/session";
import { useModal } from "../../context/Modal";
import "./LoginForm.css";

function LoginFormModal() {
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const { closeModal } = useModal();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await dispatch(
      thunkLogin({
        email,
        password,
      })
    );

    if (response) {
      setErrors(response);
    } else {
      closeModal();
    }
  };

  return (
    <div className="login-modal">
      <h1 className="login-title">Log In</h1>
      <form className="login-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className={`form-input ${errors.email ? "input-error" : ""}`}
          />
          {errors.email && <span className="error-text">{errors.email}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className={`form-input ${errors.password ? "input-error" : ""}`}
          />
          {errors.password && (
            <span className="error-text">{errors.password}</span>
          )}
        </div>

        <button type="submit" className="login-button">
          Log In
        </button>
      </form>
    </div>
  );
}

export default LoginFormModal;