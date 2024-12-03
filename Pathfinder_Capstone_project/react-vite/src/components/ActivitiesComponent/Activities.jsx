import React, { useEffect, useState } from 'react';

const ActivitiesPage = () => {
  const [activities, setActivities] = useState([]);

  useEffect(() => {
    fetch('/api/activities')
      .then((response) => response.json())
      .then((data) => setActivities(data));
  }, []);

  return (
    <div>
      <h2>Activities</h2>
      {activities.length > 0 ? (
        activities.map((activity, idx) => (
          <div key={idx}>{activity.name}</div>
        ))
      ) : (
        <p>No activities available</p>
      )}
    </div>
  );
};

export default ActivitiesPage;