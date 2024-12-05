import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./CreateItinerary.module.css";

const CreateItinerary = () => {
  const [title, setTitle] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [activities, setActivities] = useState([]);
  const navigate = useNavigate();

  const addActivity = () => {
    setActivities([...activities, { name: "", time: "" }]);
  };

  const formatToMMDDYYYY = (date) => {
    const [year, month, day] = date.split("-");
    return `${month}-${day}-${year}`;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formattedStartDate = formatToMMDDYYYY(startDate);
    const formattedEndDate = formatToMMDDYYYY(endDate);

    try {
      const response = await fetch("/api/itineraries/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title,
          start_date: formattedStartDate,
          end_date: formattedEndDate,
          activities,
        }),
      });

      if (response.ok) {
        navigate("/");
      } else {
        console.error("Error creating itinerary");
      }
    } catch (error) {
      console.error("Error creating itinerary", error);
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
      <form className={styles.form} onSubmit={handleSubmit}>
        <div className={styles.inputGroup}>
          <label htmlFor="title" className={styles.label}>
            Itinerary Title:
          </label>
          <input
            type="text"
            id="title"
            className={styles.input}
            value={title}
            onChange={(e) => setTitle(e.target.value)}
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