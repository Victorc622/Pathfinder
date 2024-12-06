import React, { useState, useEffect } from "react";
import AddDestinationForm from "./AddDestinationForm";
import "./Destination.css";

const Destination = ({ itineraryId }) => {
  const [showForm, setShowForm] = useState(false);
  const [destinations, setDestinations] = useState([]);
  const [itineraries, setItineraries] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDestinations = async () => {
      if (!itineraryId) {
        setError("No itinerary selected");
        return;
      }

      try {
        const response = await fetch(`/api/destinations/itinerary/${itineraryId}`, {
          credentials: "include",
        });
        if (response.status === 404) {
          setError("Itinerary not found or unauthorized");
          return;
        }
        if (!response.ok) {
          throw new Error("Failed to fetch destinations");
        }
        const data = await response.json();
        setDestinations(data);
      } catch (error) {
        console.error("Error fetching destinations:", error);
        setError(error.message);
      }
    };

    fetchDestinations();
  }, [itineraryId]);

  useEffect(() => {
    const fetchItineraries = async () => {
      try {
        const response = await fetch("/api/itineraries", {
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Failed to fetch itineraries");
        }
        const data = await response.json();
        setItineraries(data);
      } catch (error) {
        console.error("Error fetching itineraries:", error);
        setError(error.message);
      }
    };

    fetchItineraries();
  }, []);

  const addDestination = async (destination) => {
    if (!itineraryId) {
      setError("No itinerary selected");
      return;
    }

    const payload = { ...destination, itinerary_id: itineraryId };

    try {
      console.log("Adding destination:", payload);
      const response = await fetch("/api/destinations", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Failed to add destination");
      }

      const newDestination = await response.json();
      setDestinations((prev) => [...prev, newDestination]);
      setShowForm(false);
    } catch (error) {
      console.error("Error adding destination:", error);
      setError(error.message);
    }
  };

  return (
    <div className="destination-container">
      <h2>Destinations</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button onClick={() => setShowForm(true)} className="create-button">
        Add Destination
      </button>
      {showForm && (
        <AddDestinationForm
          itineraries={itineraries}
          onSubmit={(data) => addDestination(data)}
          onCancel={() => setShowForm(false)}
        />
      )}
      <div className="destination-list">
        {destinations.length > 0 ? (
          destinations.map((item) => (
            <div key={item.id} className="destination-card">
              <h3>{item?.name || "Unnamed Destination"}</h3>
              <p>{item?.description || "No description available."}</p>
            </div>
          ))
        ) : (
          <p>No destinations available.</p>
        )}
      </div>
    </div>
  );
};

Destination.defaultProps = {
  itineraryId: null,
};

export default Destination;
