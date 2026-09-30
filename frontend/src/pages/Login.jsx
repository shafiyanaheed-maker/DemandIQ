import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    if (username === "business1") {
      navigate("/business");
    } else if (username === "investor1") {
      navigate("/investor");
    } else if (username === "admin") {
      navigate("/admin");
    } else {
      alert("Invalid username");
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <h1>DemandIQ</h1>
        <p>Sign in to continue</p>

        <form onSubmit={handleLogin}>
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter username"
            required
          />

          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter password"
            required
          />

          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
}

export default Login;