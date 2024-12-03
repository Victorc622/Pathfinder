import React from 'react';
import './Collaboration.css';

const Collaboration = ({ collaborationData }) => {
  if (!collaborationData) {
    return <p>Loading collaborations...</p>;
  }

  if (collaborationData.length === 0) {
    return <p>No collaborations available.</p>;
  }

  return (
    <div className="collaboration-container">
      <h2>Collaborations</h2>
      <div className="collaboration-list">
        {collaborationData.map((item, index) => (
          <div key={index} className="collaboration-card">
            <h3>{item.name}</h3>
            <p>Itinerary: {item.itineraryName}</p>
            <p>Collaborator: {item.collaboratorName}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

Collaboration.defaultProps = {
  collaborationData: [],
};

export default Collaboration;