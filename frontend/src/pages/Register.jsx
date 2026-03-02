import { useState } from "react";
import { useNavigate } from "react-router-dom";
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
        className="w-full bg-purple-600 p-2 rounded"
      >
        Register
      </button>
    </div>
  );
}

export default Register;