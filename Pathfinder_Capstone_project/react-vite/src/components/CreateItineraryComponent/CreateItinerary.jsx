import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./CreateItinerary.module.css";

const CreateItinerary = () => {
  const [name, setName] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [activities, setActivities] = useState([]);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const addActivity = () => {
    setActivities([...activities, { name: "", time: "" }]);
  };

  const formatToMMDDYYYY = (date) => {
    const [year, month, day] = date.split("-");
    return `${month}-${day}-${year}`;
  };

  const validateForm = () => {
    if (!name.trim()) return "Itinerary name is required.";
    if (name.length > 50) return "Itinerary name cannot exceed 50 characters.";
    if (!startDate) return "Start date is required.";
    if (!endDate) return "End date is required.";
    if (new Date(startDate) > new Date(endDate))
      return "Start date cannot be after the end date.";
    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    const formattedStartDate = formatToMMDDYYYY(startDate);
    const formattedEndDate = formatToMMDDYYYY(endDate);

    try {
      const response = await fetch("/api/itineraries/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name,
          start_date: formattedStartDate,
          end_date: formattedEndDate,
          activities,
        }),
      });

      if (response.ok) {
        navigate("/");
      } else {
        setError("Error creating itinerary.");
      }
    } catch (error) {
      setError("Error creating itinerary. Please try again.");
    }
  };

  const handleActivityChange = (index, field, value) => {
    const updatedActivities = [...activities];
    updatedActivities[index][field] = value;
    setActivities(updatedActivities);
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Create an Itinerary</h2>
      {error && <div className={styles.errorMessage}>{error}</div>}
      <form className={styles.form} onSubmit={handleSubmit}>
        <div className={styles.inputGroup}>
          <label htmlFor="name" className={styles.label}>
            Itinerary Name:
          </label>
          <input
            type="text"
            id="name"
            className={styles.input}
            value={name}
            onChange={(e) => setName(e.target.value)}
            maxLength={50}
            placeholder="Enter itinerary name (max 50 characters)"
            required
          />
        </div>
        <div className={styles.inputGroup}>
          <label htmlFor="start_date" className={styles.label}>
            Start Date:
          </label>
          <input
            type="date"
            id="start_date"
            className={styles.input}
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            required
          />
        </div>
        <div className={styles.inputGroup}>
          <label htmlFor="end_date" className={styles.label}>
            End Date:
          </label>
          <input
            type="date"
            id="end_date"
            className={styles.input}
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            required
          />
        </div>
        <h3 className={styles.activityTitle}>Activities</h3>
        {activities.map((activity, index) => (
          <div key={index} className={styles.activity}>
            <input
              type="text"
              className={styles.activityInput}
              placeholder="Activity Name"
              value={activity.name}
              onChange={(e) =>
                handleActivityChange(index, "name", e.target.value)
              }
              required
            />
            <input
              type="time"
              className={styles.activityInput}
              value={activity.time}
              onChange={(e) =>
                handleActivityChange(index, "time", e.target.value)
              }
              required
            />
          </div>
        ))}
        <button
          type="button"
          className={styles.addButton}
          onClick={addActivity}
        >
          Add Activity
        </button>
        <div>
          <button type="submit" className={styles.submitButton}>
            Create Itinerary
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateItinerary;