import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';

// Set map container dimensions
const containerStyle = {
  width: '100%',
  height: '400px'
};

// Set initial center coordinates
const center = {
  lat: 37.7749, // Example: San Francisco latitude
  lng: -122.4194 // Example: San Francisco longitude
};

function MapComponent() {
  return (
    <LoadScript googleMapsApiKey={process.env.REACT_APP_GOOGLE_MAPS_API_KEY}>
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={10}
      >
        {/* Example marker */}
        <Marker position={center} />
      </GoogleMap>
    </LoadScript>
  );
}

export default MapComponent;
