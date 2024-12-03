import { createBrowserRouter } from 'react-router-dom';
import LoginFormPage from '../components/LoginFormPage';
import SignupFormPage from '../components/SignupFormPage';
import Layout from './Layout';
import HomePage from '../components/HomePage/HomePage';
import Itinerary from '../components/ItineraryComponent/Itinerary';
import CreateItinerary from '../components/CreateItineraryComponent/CreateItinerary'; // Import the new component
import Destination from '../components/DestinationComponent/Destination';
import Collaboration from '../components/CollaborationComponent/Collaboration';
import Activities from '../components/ActivitiesComponent/Activities';

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
      {
        path: "login",
        element: <LoginFormPage />,
      },
      {
        path: "signup",
        element: <SignupFormPage />,
      },
      {
        path: "itinerary",
        element: <Itinerary />,
      },
      {
        path: "create-itinerary",
        element: <CreateItinerary />,
      },
      {
        path: "destinations",
        element: <Destination />,
      },
      {
        path: "collaboration",
        element: <Collaboration />,
      },
      {
        path: "activities",
        element: <Activities />,
      },
    ],
  },
]);