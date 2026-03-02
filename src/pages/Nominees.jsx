import { useState } from "react";
import API from "../api/axios";

function Nominees() {
  const [email, setEmail] = useState("");

  const addNominee = async () => {
    try {
      await API.post("/nominee/add", {
        nominee_email: email,
      });
      alert("Nominee added!");
    } catch {
      alert("Failed to add nominee");
    }
  };

  return (
    <div className="max-w-md mx-auto">
      <h2 className="text-2xl mb-6">
        Add Nominee to Timeless Vault
      </h2>

      <input
        type="email"
        placeholder="Nominee Email"
        className="w-full mb-4 p-2 bg-gray-800 rounded"
        onChange={(e) => setEmail(e.target.value)}
      />

      <button
        onClick={addNominee}
        className="bg-purple-600 p-2 rounded w-full"
      >
        Add Nominee
      </button>
    </div>
  );
}

export default Nominees;