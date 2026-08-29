import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Header from "../Header/Header";
import "./Login.css";

const Login = () => {
  const navigate = useNavigate();
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const login = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch("/djangoapp/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userName, password }),
      });
      const json = await res.json();
      if (!res.ok || json.status !== "Authenticated") throw new Error("The user could not be authenticated.");
      sessionStorage.setItem("username", json.userName);
      sessionStorage.setItem("firstname", json.firstName || "");
      sessionStorage.setItem("lastname", json.lastName || "");
      navigate("/");
    } catch (err) { setError(err.message); }
  };

  return <div><Header /><main className="login_panel"><form onSubmit={login}>
    <h2>Login</h2>
    {error && <p className="auth-error">{error}</p>}
    <label>Username <input type="text" value={userName} onChange={(e) => setUserName(e.target.value)} required /></label>
    <label>Password <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required /></label>
    <button className="action_button" type="submit">Login</button>
    <p><Link to="/register">Register Now</Link></p>
  </form></main></div>;
};

export default Login;
