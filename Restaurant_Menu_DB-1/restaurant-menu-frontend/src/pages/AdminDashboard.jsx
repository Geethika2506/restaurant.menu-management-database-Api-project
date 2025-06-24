import { useState } from "react";

const AdminDashboard = () => {
  const [logs, setLogs] = useState([
    { id: 1, filename: "menu1.pdf", status: "Completed" },
    { id: 2, filename: "menu2.pdf", status: "Pending" },
  ]);
  const [file, setFile] = useState(null);

  const handleFileUpload = () => {
    if (file) {
      const newLog = {
        id: logs.length + 1,
        filename: file.name,
        status: "Pending",
      };
      setLogs([...logs, newLog]);
      setFile(null);
    }
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold text-blue-600">Admin Dashboard</h1>
      
      {/* File Upload */}
      <form
        className="mt-6"
        onSubmit={(e) => {
          e.preventDefault();
          handleFileUpload();
        }}
      >
        <label className="block mb-2 font-medium">Upload Menu PDF:</label>
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="border rounded p-2 w-full"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded mt-4"
        >
          Upload
        </button>
      </form>

      {/* Processing Logs */}
      <div className="mt-8">
        <h2 className="text-2xl font-semibold">Processing Logs</h2>
        <ul className="mt-2 space-y-2">
          {logs.map((log) => (
            <li key={log.id} className="bg-white shadow rounded p-4">
              {log.filename}: <span className="font-bold">{log.status}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default AdminDashboard;
