import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "./api";
import "./index.css";

function Login() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post("/login", form);

      localStorage.setItem("token", res.data.access_token);

      navigate("/dashboard");
    } catch (err) {
      alert("Invalid Credentials");
    }
  };

  return (
    <div className="app-bg">

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "100vh",
        }}
      >

        <div
          className="card"
          style={{
            width: "420px",
            padding: "35px",
          }}
        >

          <div style={{ textAlign: "center" }}>
            <div
              style={{
                fontSize: "55px",
                marginBottom: "10px",
              }}
            >
              🔐
            </div>

            <h1
              style={{
                marginBottom: "8px",
              }}
            >
              Welcome Back
            </h1>

            <p className="muted">
              Login to continue
            </p>
          </div>

          <form onSubmit={handleSubmit}>

            <input
              type="email"
              name="email"
              placeholder="Email Address"
              value={form.email}
              onChange={handleChange}
              style={{
                width: "100%",
                padding: "14px",
                marginTop: "20px",
                borderRadius: "10px",
                border: "1px solid #ddd",
                fontSize: "15px",
              }}
            />

            <br />
            <br />

            <input
              type="password"
              name="password"
              placeholder="Password"
              value={form.password}
              onChange={handleChange}
              style={{
                width: "100%",
                padding: "14px",
                borderRadius: "10px",
                border: "1px solid #ddd",
                fontSize: "15px",
              }}
            />

            <br />
            <br />

            <button
              className="btn"
              style={{
                width: "100%",
                padding: "14px",
                fontSize: "16px",
              }}
            >
              Login
            </button>

          </form>

          <div
            style={{
              marginTop: "25px",
              textAlign: "center",
            }}
          >
            <span className="muted">
              Don't have an account?
            </span>

            <br />

            <Link
              to="/register"
              style={{
                textDecoration: "none",
                color: "#7c3aed",
                fontWeight: "bold",
              }}
            >
              Create Account
            </Link>
          </div>

        </div>

      </div>

    </div>
  );
}

export default Login;