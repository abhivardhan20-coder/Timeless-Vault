import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import API from "../api/axios";

function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      await API.post("/register", { email, password });
      alert("Registered successfully!");
      navigate("/");
    } catch {
      alert("Registration failed");
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
      alert("Google sign-up failed");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 bg-gray-900 p-8 rounded-xl">
      <h2 className="text-2xl font-bold mb-6 text-center">
        Create Timeless Vault Account
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
        onClick={handleRegister}
        className="w-full bg-purple-600 p-2 rounded hover:bg-purple-700 transition"
      >
        Register
      </button>

      <div className="my-6 flex items-center gap-3">
        <div className="flex-1 h-px bg-gray-700"></div>
        <span className="text-gray-400 text-sm">or</span>
        <div className="flex-1 h-px bg-gray-700"></div>
      </div>

      <div className="flex justify-center">
        <GoogleLogin
          onSuccess={handleGoogleSuccess}
          onError={() => alert("Google sign-up failed")}
          theme="filled_black"
          size="large"
          width="100%"
          text="signup_with"
        />
      </div>

      <p className="mt-4 text-center">
        Already have an account?{" "}
        <Link to="/" className="text-purple-400">
          Login
        </Link>
      </p>
    </div>
  );
}

export default Register;