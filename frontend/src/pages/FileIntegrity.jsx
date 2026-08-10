import { useState } from "react";
import api from "../utils/api";

function FileIntegrity() {
  const [folder, setFolder] = useState("monitored_files");
  const [hashFile, setHashFile] = useState("hashes.json");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleCheck = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const response = await api.post("/integrity/check", null, {
        params: { folder_to_monitor: folder, hash_file: hashFile },
      });

      setResult(response.data);
    } catch (err) {
      setError("Could not check file integrity. Check the folder path and try again.");
    } finally {
      setLoading(false);
    }
  };

  const renderFileList = (title, files) => (
    <div>
      <h4>{title}</h4>
      {files.length > 0 ? (
        <ul>
          {files.map((file, index) => (
            <li key={index}>{file}</li>
          ))}
        </ul>
      ) : (
        <p>None</p>
      )}
    </div>
  );

  return (
    <div>
      <div className="page-header">
        <h2>File Integrity Monitor</h2>
      </div>
      <form onSubmit={handleCheck}>
        <div>
          <label>Folder to Monitor</label>
          <input value={folder} onChange={(e) => setFolder(e.target.value)} required />
        </div>
        <div>
          <label>Hash File</label>
          <input value={hashFile} onChange={(e) => setHashFile(e.target.value)} required />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Checking..." : "Check Integrity"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div>
          {renderFileList("New Files", result.new_files)}
          {renderFileList("Changed Files", result.changed_files)}
          {renderFileList("Deleted Files", result.deleted_files)}
        </div>
      )}
    </div>
  );
}

export default FileIntegrity;