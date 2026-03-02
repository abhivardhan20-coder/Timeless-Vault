import { useState } from "react";
import API from "../api/axios";

function Upload() {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      await API.post("/vault/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("Uploaded successfully!");
    } catch {
      alert("Upload failed");
    }
  };

  return (
    <div className="max-w-lg mx-auto">
      <h2 className="text-2xl mb-6">
        Upload to Timeless Vault
      </h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4"
      />

      <button
        onClick={handleUpload}
        className="bg-purple-600 px-6 py-2 rounded"
      >
        Upload
      </button>
    </div>
  );
}

export default Upload;