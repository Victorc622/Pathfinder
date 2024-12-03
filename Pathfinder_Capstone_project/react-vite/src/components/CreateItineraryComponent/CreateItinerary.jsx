import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./CreateItinerary.module.css";

const CreateItinerary = () => {
  const [title, setTitle] = useState("");
  const [date, setDate] = useState("");
  const [activities, setActivities] = useState([]);
  const navigate = useNavigate();

  const addActivity = () => {
    setActivities([...activities, { name: "", time: "" }]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("/create-itinerary", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, date, activities }),
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
          <label htmlFor="title" className={styles.label}>Itinerary Title:</label>
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
          <label htmlFor="date" className={styles.label}>Date:</label>
          <input
            type="date"
            id="date"
            className={styles.input}
            value={date}
            onChange={(e) => setDate(e.target.value)}
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
              onChange={(e) => handleActivityChange(index, "name", e.target.value)}
              required
            />
            <input
              type="time"
              className={styles.activityInput}
              value={activity.time}
              onChange={(e) => handleActivityChange(index, "time", e.target.value)}
              required
            />
          </div>
        ))}
        <button type="button" className={styles.addButton} onClick={addActivity}>Add Activity</button>
        <div>
          <button type="submit" className={styles.submitButton}>Create Itinerary</button>
        </div>
      </form>
    </div>
  );
};

export default CreateItinerary;