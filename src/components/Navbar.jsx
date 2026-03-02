import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="flex justify-between items-center p-4 bg-gray-900 shadow">
      <h1 className="text-xl font-bold text-purple-400">
        Timeless Vault
      </h1>

      {token && (
        <div className="space-x-4">
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/upload">Upload</Link>
          <Link to="/nominees">Nominees</Link>
          <Link to="/requests">Requests</Link>
          <button
            onClick={logout}
            className="bg-red-500 px-3 py-1 rounded"
          >
            Logout
          </button>
        </div>
      )}
    </div>
  );
}

export default Navbar;