import React, { useState, useEffect } from "react";
import Destination from "./Destination";

const ItineraryManager = () => {
  const [itineraries, setItineraries] = useState([]);
  const [selectedItineraryId, setSelectedItineraryId] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchItineraries = async () => {
      try {
        const response = await fetch("/api/itineraries", { credentials: "include" });
        if (!response.ok) {
          throw new Error("Failed to fetch itineraries");
        }
        const data = await response.json();
        setItineraries(data);
        if (data.length > 0) {
          setSelectedItineraryId(data[0].id);
        }
      } catch (error) {
        console.error("Error fetching itineraries:", error);
        setError(error.message);
      }
    };

    fetchItineraries();
  }, []);

  const handleSelectionChange = (event) => {
    setSelectedItineraryId(Number(event.target.value));
  };

  return (
    <div>
      <h1>Destinations</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      
      <div>
        <label htmlFor="itinerary-select">Select an Itinerary:</label>
        <select
          id="itinerary-select"
          value={selectedItineraryId || ""}
          onChange={handleSelectionChange}
        >
          <option value="" disabled>
            -- Select an Itinerary --
          </option>
          {itineraries.map((itinerary) => (
            <option key={itinerary.id} value={itinerary.id}>
              {itinerary.name}
            </option>
          ))}
        </select>
      </div>

      {selectedItineraryId ? (
        <Destination itineraryId={selectedItineraryId} />
      ) : (
        <p>Please select an itinerary to view destinations.</p>
      )}
    </div>
  );
};

export default ItineraryManager;