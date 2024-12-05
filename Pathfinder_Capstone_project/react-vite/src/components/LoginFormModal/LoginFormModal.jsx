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

    // Dispatch login action
    const response = await dispatch(
      thunkLogin({ email, password })
    );

    if (response?.errors) {
      setErrors(response.errors);
    } else {
      closeModal();
    }
  };

  return (
    <div className="login-modal">
      <h2>Log In</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          {errors.email && <p className="error-text">{errors.email}</p>}
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {errors.password && <p className="error-text">{errors.password}</p>}
        </div>
        <button type="submit" className="login-button">
          Log In
        </button>
      </form>
    </div>
  );
}

export default LoginFormModal;