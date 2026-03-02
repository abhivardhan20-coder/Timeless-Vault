import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
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

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      const res = await API.post("/auth/google", {
        credential: credentialResponse.credential,
      });
      localStorage.setItem("token", res.data.access_token);
      navigate("/dashboard");
    } catch {
      alert("Google login failed");
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
        className="w-full bg-purple-600 p-2 rounded hover:bg-purple-700 transition"
      >
        Login
      </button>

      <div className="my-6 flex items-center gap-3">
        <div className="flex-1 h-px bg-gray-700"></div>
        <span className="text-gray-400 text-sm">or</span>
        <div className="flex-1 h-px bg-gray-700"></div>
      </div>

      <div className="flex justify-center">
        <GoogleLogin
          onSuccess={handleGoogleSuccess}
          onError={() => alert("Google login failed")}
          theme="filled_black"
          size="large"
          width="100%"
          text="signin_with"
        />
      </div>

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