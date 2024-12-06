import React, { useState, useEffect } from "react";
import "./AddDestinationForm.css";

const AddDestinationForm = ({ itineraries, onSubmit, onCancel }) => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [image, setImage] = useState("");
  const [itineraryId, setItineraryId] = useState("");

  useEffect(() => {
    if (itineraries.length > 0) {
      setItineraryId(itineraries[0].id); // Default to the first itinerary
    }
  }, [itineraries]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name || !itineraryId) {
      alert("Name and Itinerary are required.");
      return;
    }

    const newDestination = {
      name,
      description,
      image,
      itinerary_id: itineraryId,
    };

    onSubmit(newDestination);

    // Reset the form
    setName("");
    setDescription("");
    setImage("");
    setItineraryId(itineraries.length > 0 ? itineraries[0].id : "");
  };

  return (
    <div className="add-destination-form">
      <h2>Add Destination</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Destination Name:
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </label>
        <label>
          Description:
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </label>
        <label>
          Image URL:
          <input
            type="text"
            value={image}
            onChange={(e) => setImage(e.target.value)}
          />
        </label>
        <label>
          Select Itinerary:
          <select
            value={itineraryId}
            onChange={(e) => setItineraryId(e.target.value)}
            required
          >
            {itineraries.map((itinerary) => (
              <option key={itinerary.id} value={itinerary.id}>
                {itinerary.name}
              </option>
            ))}
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