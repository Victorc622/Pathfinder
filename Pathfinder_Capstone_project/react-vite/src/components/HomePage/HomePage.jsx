import { Link } from "react-router-dom";
import styles from "./HomePage.module.css";

const HomePage = () => {
  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.title}>Welcome to Pathfinder</h1>
        <p className={styles.subtitle}>
          Your ultimate tool for seamless trip planning.
        </p>
      </header>
      <div className={styles.features}>
        <div className={styles.featureCard}>
          <h2>Plan Your Itinerary</h2>
          <p>
            Create personalized travel schedules and manage activities
            effortlessly.
          </p>
        </div>
        <div className={styles.featureCard}>
          <h2>Explore Destinations</h2>
          <p>
            Discover top attractions and activities tailored to your interests.
          </p>
        </div>
        <div className={styles.featureCard}>
          <h2>Collaborate with Friends</h2>
          <p>Share and plan trips with family and friends in real-time.</p>
        </div>
      </div>

      {/* Updated Get Started button to navigate to /create-itinerary */}
      <Link to="/create-itinerary">
        <button className={styles.ctaButton}>
          Get Started
        </button>
      </Link>
    </div>
  );
};

export default HomePage;