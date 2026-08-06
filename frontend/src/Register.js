import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "./api";
import "./index.css";

function Register() {

  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: ""
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {

    e.preventDefault();

    try {

      await api.post("/register", {
        ...form,
        
      });

      alert("Registration Successful");

      navigate("/");

    }
    catch (err) {

      console.log(err);
      console.log(err.response);

      alert(err.response?.data?.detail || "Registration Failed");

    }

  };

  return (

    <div className="app-bg">

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "100vh"
        }}
      >

        <div className="card auth-card">

          <div className="auth-title">

            <div className="auth-icon">
              👤
            </div>

            <h1>Create Account</h1>

            <p className="muted">
              Register to manage your products
            </p>

          </div>

          <form onSubmit={handleSubmit}>

            <br /><br />

            <input
              className="auth-input"
              type="email"
              name="email"
              placeholder="Email Address"
              value={form.email}
              onChange={handleChange}
            />

            <br /><br />

            <input
              className="auth-input"
              type="password"
              name="password"
              placeholder="Password"
              value={form.password}
              onChange={handleChange}
            />

            <br /><br />

            <button
              className="btn"
              style={{
                width: "100%",
                padding: "14px",
                fontSize: "16px"
              }}
            >
              Register
            </button>

          </form>

          <div className="auth-footer">

            <span className="muted">
              Already have an account?
            </span>

            <br />

            <Link
              className="auth-link"
              to="/"
            >
              Login Here
            </Link>

          </div>

        </div>

      </div>

    </div>

  );

}

export default Register;