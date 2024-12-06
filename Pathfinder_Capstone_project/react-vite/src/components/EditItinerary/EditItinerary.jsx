import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import styles from "./EditItinerary.css";

const EditItinerary = () => {
  const { id } = useParams();
  const [itinerary, setItinerary] = useState(null);
  const [name, setName] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const formatDate = (date) => {
    const d = new Date(date);
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    const year = d.getFullYear();
    return `${month}-${day}-${year}`;
  };

  useEffect(() => {
    const fetchItinerary = async () => {
      try {
        const response = await fetch(`/api/itineraries/${id}`, {
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch itinerary: ${response.status}`);
        }

        const data = await response.json();
        setItinerary(data);
        setName(data.name);
        setStartDate(data.start_date);
        setEndDate(data.end_date);
      } catch (err) {
        setError(err.message || "Something went wrong while fetching itinerary");
      } finally {
        setLoading(false);
      }
    };

    fetchItinerary();
  }, [id]);

  // Form Validation
  const validateForm = () => {
    if (!name.trim()) return "Name is required";
    if (name.length > 50) return "Name cannot exceed 50 characters";
    if (!startDate || !endDate) return "Start and End dates are required";
    if (new Date(startDate) > new Date(endDate)) return "Start date cannot be after the End date";
    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    try {
      const formattedStartDate = formatDate(startDate);
      const formattedEndDate = formatDate(endDate);

      const response = await fetch(`/api/itineraries/${id}`, {
        method: "PUT",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name,
          start_date: formattedStartDate,
          end_date: formattedEndDate,
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to update itinerary: ${response.status}`);
      }

      setSuccess(true);
      setTimeout(() => navigate("/itinerary"), 1500);
    } catch (err) {
      setError(err.message || "Failed to save changes");
    }
  };

  if (loading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  return (
    <div className={styles.editItinerary}>
      <h1>Edit Itinerary</h1>
      {error && <div className={styles.error}>{error}</div>}
      {success && <div className={styles.success}>Itinerary updated successfully!</div>}
      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter itinerary name (max 50 characters)"
            maxLength={50}
          />
        </label>
        <label>
          Start Date:
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </label>
        <label>
          End Date:
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </label>
        <button type="submit">Save Changes</button>
      </form>
    </div>
  );
};

export default EditItinerary;