import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import "./Activities.css";

const ActivitiesPage = () => {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [searchParams] = useSearchParams();
  const itineraryId = searchParams.get("itinerary_id");
  const destinationId = searchParams.get("destination_id");

  const fetchActivities = async () => {
    try {
      setLoading(true);
      setError(null);

      const params = new URLSearchParams();
      if (itineraryId) params.append("itinerary_id", itineraryId);
      if (destinationId) params.append("destination_id", destinationId);

      const response = await fetch(`/api/activities?${params.toString()}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch activities: ${response.status}`);
      }
      const data = await response.json();
      setActivities(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchActivities();
  }, [itineraryId, destinationId]);

  if (loading) {
    return <p>Loading activities...</p>;
  }

  if (error) {
    return (
      <div style={{ color: "red" }}>
        <p>Error: {error}</p>
        <button onClick={fetchActivities}>Retry</button>
      </div>
    );
  }

  return (
    <div className="activities-container">
      <h2>Activities</h2>
      {activities.length > 0 ? (
        <ul className="activities-list">
          {activities.map((activity) => (
            <li key={activity.id} className="activity-item">
              <h3>{activity.name}</h3>
              <p>{activity.description}</p>
              <p>
                <strong>Time:</strong> {activity.time}
              </p>
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