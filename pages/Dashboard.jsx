import { useEffect, useState } from "react";
import API from "../api/axios";
import VaultCard from "../components/VaultCard";

function Dashboard() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    API.get("/vault/items")
      .then((res) => setItems(res.data))
      .catch(() => alert("Failed to fetch vault items"));
  }, []);

  return (
    <div>
      <h2 className="text-2xl mb-6">Your Timeless Vault</h2>

      <div className="grid md:grid-cols-3 gap-6">
        {items.map((item) => (
          <VaultCard key={item.id} item={item} />
        ))}
      </div>
    </div>
  );
}

export default Dashboard;