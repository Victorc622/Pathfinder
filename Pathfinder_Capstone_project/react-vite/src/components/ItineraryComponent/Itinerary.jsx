import React from 'react';
import './Itinerary.css';

const Itinerary = ({ itineraryData }) => {
  if (!itineraryData || itineraryData.length === 0) {
    return (
      <div className="itinerary-container">
        <h2>My Itinerary</h2>
        <p>No itineraries available.</p>
      </div>
    );
  }

  return (
    <div className="itinerary-container">
      <h2>My Itinerary</h2>
      <div className="itinerary-list">
        {itineraryData.map((item, index) => (
          <div key={index} className="itinerary-card">
            <div className="itinerary-header">
              <h3>{item.title || 'Untitled Itinerary'}</h3>
              <p className="itinerary-date">{item.date || 'No Date Available'}</p>
            </div>
            <ul className="activities-list">
              {item.activities && item.activities.length > 0 ? (
                item.activities.map((activity, idx) => (
                  <li key={idx} className="activity-item">
                    <p>{activity.name || 'Unnamed Activity'}</p>
                    <p className="activity-time">{activity.time || 'No Time Specified'}</p>
                  </li>
                ))
              ) : (
                <li className="activity-item">
                  <p>No activities listed for this itinerary.</p>
                </li>
              )}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Itinerary;