import { useEffect, useState } from "react";
import API from "../api/axios";

function AccessRequests() {
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    API.get("/access/requests")
      .then((res) => setRequests(res.data))
      .catch(() => alert("Failed to fetch requests"));
  }, []);

  const approve = async (id) => {
    try {
      await API.post("/access/approve", {
        request_id: id,
      });
      alert("Approved!");
    } catch {
      alert("Approval failed");
    }
  };

  return (
    <div>
      <h2 className="text-2xl mb-6">
        Timeless Vault Access Requests
      </h2>

      {requests.map((req) => (
        <div
          key={req.id}
          className="bg-gray-900 p-4 rounded mb-4"
        >
          <p>Vault Item ID: {req.vault_item_id}</p>
          <p>Status: {req.status}</p>

          <button
            onClick={() => approve(req.id)}
            className="bg-green-600 px-4 py-1 mt-2 rounded"
          >
            Approve
          </button>
        </div>
      ))}
    </div>
  );
}

export default AccessRequests;