import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Register.css";

function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ userName: "", firstName: "", lastName: "", email: "", password: "" });
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const response = await fetch("/djangoapp/register", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(form),
      });
      const data = await response.json();
      if (!response.ok || data.status !== "Authenticated") throw new Error(data.message || "Registration failed.");
      sessionStorage.setItem("username", data.userName);
      sessionStorage.setItem("firstname", data.firstName || form.firstName);
      sessionStorage.setItem("lastname", data.lastName || form.lastName);
      navigate("/");
    } catch (err) { setError(err.message); }
  };

  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  return <div><main className="register-container"><h2>Sign-up</h2>{error && <p className="auth-error">{error}</p>}
    <form onSubmit={handleSubmit}>
      <input name="userName" type="text" placeholder="Username" value={form.userName} onChange={update} required />
      <input name="firstName" type="text" placeholder="First Name" value={form.firstName} onChange={update} required />
      <input name="lastName" type="text" placeholder="Last Name" value={form.lastName} onChange={update} required />
      <input name="email" type="email" placeholder="Email" value={form.email} onChange={update} required />
      <input name="password" type="password" placeholder="Password" value={form.password} onChange={update} minLength="8" required />
      <button type="submit">Register</button>
    </form><p><Link to="/login">Already registered? Login</Link></p>
  </main></div>;
}
export default Register;
