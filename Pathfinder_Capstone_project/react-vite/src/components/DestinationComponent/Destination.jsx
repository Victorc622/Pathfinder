import React, { useState, useEffect } from "react";
import AddDestinationForm from "./AddDestinationForm";

const Destination = ({ itineraryId }) => {
  const [destinations, setDestinations] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [currentDestination, setCurrentDestination] = useState(null); // For editing
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDestinations = async () => {
      try {
        const response = await fetch(`/api/destinations/itinerary/${itineraryId}`, {
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

    if (itineraryId) {
      fetchDestinations();
    }
  }, [itineraryId]);

  const deleteDestination = async (destinationId) => {
    if (!window.confirm("Are you sure you want to delete this destination?")) {
      return;
    }

    try {
      const response = await fetch(`/api/destinations/${destinationId}`, {
        method: "DELETE",
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Failed to delete destination");
      }

      setDestinations((prev) =>
        prev.filter((destination) => destination.id !== destinationId)
      );
    } catch (err) {
      console.error("Error deleting destination:", err);
      setError(err.message);
    }
  };

  const createDestination = async (newDestination) => {
    try {
      const response = await fetch(`/api/destinations`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newDestination),
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Failed to create destination");
      }

      const createdDestination = await response.json();
      setDestinations((prev) => [...prev, createdDestination]);
      setShowForm(false);
    } catch (err) {
      console.error("Error creating destination:", err);
      setError(err.message);
    }
  };

  const updateDestination = async (updatedDestination) => {
    try {
      const response = await fetch(`/api/destinations/${currentDestination.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedDestination),
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Failed to update destination");
      }

      const updatedData = await response.json();
      setDestinations((prev) =>
        prev.map((destination) =>
          destination.id === updatedData.id ? updatedData : destination
        )
      );

      setCurrentDestination(null);
      setShowForm(false);
    } catch (err) {
      console.error("Error updating destination:", err);
      setError(err.message);
    }
  };

  const handleEditClick = (destination) => {
    setCurrentDestination(destination);
    setShowForm(true);
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
      <button onClick={() => setShowForm(true)} className="create-button">
        Create Destination
      </button>
      {showForm && (
        <AddDestinationForm
          itineraries={[{ id: itineraryId, name: "Current Itinerary" }]} // Pass current itinerary
          onSubmit={
            currentDestination
              ? (data) => updateDestination({ ...data, itinerary_id: itineraryId })
              : (data) => createDestination({ ...data, itinerary_id: itineraryId })
          }
          onCancel={() => {
            setShowForm(false);
            setCurrentDestination(null);
          }}
          initialData={currentDestination} // Pass initial data for editing
        />
      )}
      {destinations.length === 0 ? (
        <p>No destinations available for this itinerary.</p>
      ) : (
        <ul>
          {destinations.map((destination) => (
            <li key={destination.id}>
              <h3>{destination.name}</h3>
              <p>{destination.description}</p>
              <button
                onClick={() => deleteDestination(destination.id)}
                className="delete-button"
              >
                Delete
              </button>
              <button
                onClick={() => handleEditClick(destination)}
                className="edit-button"
              >
                Edit
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Destination;