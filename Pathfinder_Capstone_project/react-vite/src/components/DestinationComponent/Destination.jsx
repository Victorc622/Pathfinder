import './Destination.css';

const Destination = ({ destinationData }) => {
  if (!destinationData || destinationData.length === 0) {
    return <p>No destinations available.</p>;
  }

  return (
    <div className="destination-container">
      <h2>Destinations</h2>
      <div className="destination-list">
        {destinationData.map((item, index) => (
          <div key={index} className="destination-card">
            <img
              src={item?.image || '/default-image.jpg'}
              alt={item?.name || 'Destination'}
              className="destination-image"
            />
            <h3>{item?.name || 'Unnamed Destination'}</h3>
            <p>{item?.description || 'No description available.'}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

Destination.defaultProps = {
  destinationData: [],
};

export default Destination;