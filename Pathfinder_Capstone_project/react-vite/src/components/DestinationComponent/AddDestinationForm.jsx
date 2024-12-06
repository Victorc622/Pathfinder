import React, { useState, useEffect } from "react";
import "./AddDestinationForm.css";

const AddDestinationForm = ({ itineraries, onSubmit, onCancel }) => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [itineraryId, setItineraryId] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (itineraries.length > 0) {
      setItineraryId(itineraries[0].id);
    }
  }, [itineraries]);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!name.trim()) {
      setError("Destination name is required.");
      return;
    }
    if (!itineraryId) {
      setError("Please select an itinerary.");
      return;
    }

    const newDestination = {
      name: name.trim(),
      description: description.trim(),
      itinerary_id: itineraryId,
    };

    onSubmit(newDestination);

    setName("");
    setDescription("");
    setItineraryId(itineraries.length > 0 ? itineraries[0].id : "");
    setError("");
  };

  return (
    <div className="add-destination-form">
      <h2>Add Destination</h2>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Destination Name:
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            placeholder="Enter destination name"
          />
        </label>
        <label>
          Description:
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Enter destination description (optional)"
          />
        </label>
        <label>
          Select Itinerary:
          <select
            value={itineraryId}
            onChange={(e) => setItineraryId(e.target.value)}
            required
          >
            {itineraries.length > 0 ? (
              itineraries.map((itinerary) => (
                <option key={itinerary.id} value={itinerary.id}>
                  {itinerary.name}
                </option>
              ))
            ) : (
              <option value="">No itineraries available</option>
            )}
          </select>
        </label>
        <div className="form-actions">
          <button type="submit" className="submit-button">
            Add Destination
          </button>
          <button type="button" onClick={onCancel} className="cancel-button">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddDestinationForm;