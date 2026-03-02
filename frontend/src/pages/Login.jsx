import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../api/axios";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await API.post("/login", { email, password });
      localStorage.setItem("token", res.data.access_token);
      navigate("/dashboard");
    } catch {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 bg-gray-900 p-8 rounded-xl">
      <h2 className="text-2xl font-bold mb-6 text-center">
        Login to Timeless Vault
      </h2>

      <input
        type="email"
        placeholder="Email"
        className="w-full mb-4 p-2 bg-gray-800 rounded"
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        className="w-full mb-4 p-2 bg-gray-800 rounded"
        onChange={(e) => setPassword(e.target.value)}
      />

      <button
        onClick={handleLogin}
        className="w-full bg-purple-600 p-2 rounded"
      >
        Login
      </button>

      <p className="mt-4 text-center">
        No account?{" "}
        <Link to="/register" className="text-purple-400">
          Register
        </Link>
      </p>
    </div>
  );
}

export default Login;