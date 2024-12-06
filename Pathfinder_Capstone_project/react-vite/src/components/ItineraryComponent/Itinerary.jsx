import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Itinerary = () => {
  const [itineraries, setItineraries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchItineraries = async () => {
      setLoading(true);
      try {
        const response = await fetch("/api/itineraries", { credentials: "include" });
        if (!response.ok) {
          throw new Error("Failed to fetch itineraries");
        }
        const data = await response.json();
        setItineraries(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchItineraries();
  }, []);

  const handleRedirect = () => {
    navigate("/create-itinerary");
  };

  const handleEditRedirect = (id) => {
    navigate(`/edit-itinerary/${id}`);
  };

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`/api/itineraries/${id}`, {
        method: "DELETE",
        credentials: "include",
      });

      if (response.ok) {

        setItineraries(itineraries.filter((itinerary) => itinerary.id !== id));
      } else {
        const errorData = await response.json();
        alert(`Failed to delete itinerary: ${errorData.error || "Unknown error"}`);
      }
    } catch (err) {
      alert(`Error deleting itinerary: ${err.message}`);
    }
  };

  if (loading) {
    return <p>Loading itineraries...</p>;
  }

  return (
    <div>
      <h2>My Itineraries</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      {itineraries.length === 0 ? (
        <p>No itineraries found. Create your first itinerary below!</p>
      ) : (
        <ul>
          {itineraries.map((itinerary) => (
            <li key={itinerary.id}>
              <h3>{itinerary.name}</h3>
              <p>{`Start: ${itinerary.start_date}`}</p>
              <p>{`End: ${itinerary.end_date}`}</p>
              <button
                onClick={() => handleEditRedirect(itinerary.id)}
                style={{ margin: "5px", backgroundColor: "blue", color: "white" }}
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(itinerary.id)}
                style={{ margin: "5px", backgroundColor: "red", color: "white" }}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}

      <button onClick={handleRedirect}>Create New Itinerary</button>
    </div>
  );
};

export default Itinerary;