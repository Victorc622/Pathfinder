import React, { useEffect, useState } from "react";
import "./Activities.css";

const ActivitiesPage = () => {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const response = await fetch("/api/activities");
        if (!response.ok) {
          throw new Error("Failed to fetch activities");
        }
        const data = await response.json();
        setActivities(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchActivities();
  }, []);

  if (loading) {
    return <p>Loading activities...</p>;
  }

  if (error) {
    return <p style={{ color: "red" }}>{error}</p>;
  }

  return (
    <div className="activities-container">
      <h2>Activities</h2>
      {activities.length > 0 ? (
        <ul className="activities-list">
          {activities.map((activity, idx) => (
            <li key={idx} className="activity-item">
              <h3>{activity.name}</h3>
              <p>{activity.description}</p>
              <p>Time: {activity.time}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No activities available.</p>
      )}
    </div>
  );
};

export default ActivitiesPage;