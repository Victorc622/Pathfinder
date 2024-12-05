import React, { useState, useEffect } from "react";
import "./Collaboration.css";

const Collaboration = () => {
  const [collaborations, setCollaborations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch collaborations on component mount
  useEffect(() => {
    const fetchCollaborations = async () => {
      try {
        const response = await fetch("/api/collaborations", {
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Failed to fetch collaborations");
        }
        const data = await response.json();
        setCollaborations(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCollaborations();
  }, []);

  const handleRemoveCollaboration = async (id) => {
    try {
      const response = await fetch(`/api/collaborations/${id}`, {
        method: "DELETE",
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error("Failed to remove collaboration");
      }
      setCollaborations(collaborations.filter((item) => item.id !== id));
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) {
    return <p>Loading collaborations...</p>;
  }

  if (error) {
    return <p style={{ color: "red" }}>{error}</p>;
  }

  if (collaborations.length === 0) {
    return <p>No collaborations available.</p>;
  }

  return (
    <div className="collaboration-container">
      <h2>Collaborations</h2>
      <ul className="collaboration-list">
        {collaborations.map((item) => (
          <li key={item.id} className="collaboration-item">
            <div className="collaboration-details">
              <p><strong>Name:</strong> {item.name}</p>
              <p><strong>Description:</strong> {item.description}</p>
            </div>
            <button
              className="remove-button"
              onClick={() => handleRemoveCollaboration(item.id)}
            >
              Remove
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Collaboration;