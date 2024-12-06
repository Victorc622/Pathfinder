import React, { useState, useEffect } from "react";
import "./AddDestinationForm.css";

const AddDestinationForm = ({ itineraries, onSubmit, onCancel, initialData }) => {
  const [name, setName] = useState(initialData?.name || "");
  const [description, setDescription] = useState(initialData?.description || "");
  const [image, setImage] = useState(initialData?.image || "");
  const [itineraryId, setItineraryId] = useState(initialData?.itinerary_id || "");
  const [error, setError] = useState(null);

  useEffect(() => {
    if (itineraries.length > 0 && !initialData) {
      setItineraryId(itineraries[0].id);
    }
  }, [itineraries, initialData]);

  const validateForm = () => {
    if (!name.trim()) return "Name is required.";
    if (name.length > 50) return "Name cannot exceed 50 characters.";
    if (description.length > 100) return "Description cannot exceed 100 characters.";
    if (!itineraryId) return "An itinerary must be selected.";
    return null;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    onSubmit({
      name: name.trim(),
      description: description.trim(),
      image: image.trim(),
      itinerary_id: itineraryId,
    });
  };

  return (
    <div className="add-destination-form">
      <h2>{initialData ? "Edit Destination" : "Add Destination"}</h2>
      {error && <div className="errorMessage">{error}</div>}
      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            maxLength={50}
            placeholder="Enter destination name (max 50 characters)"
            required
          />
        </label>
        <label>
          Description:
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            maxLength={100}
            placeholder="Enter destination description (max 100 characters)"
          />
        </label>
        <label>
          Image URL:
          <input
            type="text"
            value={image}
            onChange={(e) => setImage(e.target.value)}
            placeholder="Enter image URL"
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
          <button type="submit">{initialData ? "Update" : "Add"}</button>
          <button type="button" onClick={onCancel}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddDestinationForm;