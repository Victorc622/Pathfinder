import { createBrowserRouter } from 'react-router-dom';
import LoginFormPage from '../components/LoginFormPage';
import SignupFormPage from '../components/SignupFormPage';
import Layout from './Layout';
import HomePage from '../components/HomePage/HomePage';
import Itinerary from '../components/ItineraryComponent/Itinerary';
import CreateItinerary from '../components/CreateItineraryComponent/CreateItinerary';
import Destination from '../components/DestinationComponent/Destination';
import Collaboration from '../components/CollaborationComponent/Collaboration';
import Activities from '../components/ActivitiesComponent/Activities';
import EditItinerary from '../components/EditItinerary/EditItinerary';
import ItineraryManager from '../components/DestinationComponent/ItineraryManager';

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
        path: "destinations",
        element: <ItineraryManager />,
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
        path: "/edit-itinerary/:id",
        element: <EditItinerary />,
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