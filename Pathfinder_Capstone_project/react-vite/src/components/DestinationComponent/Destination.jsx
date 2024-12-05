import React, { useState, useEffect } from "react";

const Destination = () => {
  const [destinations, setDestinations] = useState([]);
  const [selectedDestination, setSelectedDestination] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDestinations = async () => {
      try {
        const response = await fetch("/api/destinations", {
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Failed to fetch destinations");
        }
        const data = await response.json();
        setDestinations(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDestinations();
  }, []);

  const handleSelectDestination = (destination) => {
    setSelectedDestination(destination);
  };

  if (loading) {
    return <p>Loading destinations...</p>;
  }

  if (error) {
    return <p style={{ color: "red" }}>{error}</p>;
  }

  return (
    <div>
      <h2>Destinations</h2>
      {destinations.length === 0 ? (
        <p>No destinations available. Add a new destination to your itinerary!</p>
      ) : (
        <ul>
          {destinations.map((destination) => (
            <li key={destination.id} onClick={() => handleSelectDestination(destination)}>
              <h3>{destination.name}</h3>
              <p>{destination.description}</p>
            </li>
          ))}
        </ul>
      )}

      {selectedDestination && (
        <div>
          <h3>Selected Destination</h3>
          <p><strong>Name:</strong> {selectedDestination.name}</p>
          <p><strong>Description:</strong> {selectedDestination.description}</p>
        </div>
      )}
    </div>
  );
};

export default Destination;