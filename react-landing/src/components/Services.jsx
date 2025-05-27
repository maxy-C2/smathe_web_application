import React from 'react';
import ServiceCard from './ServiceCard';
import './styles/Services.css';
import { FaCloudSun, FaLeaf, FaBell, FaUmbrella, FaChartLine } from 'react-icons/fa'; 

const services = [
  {
    icon: <FaLeaf />,
    title: 'Soil Composition Analysis',
    description: 'Analyzing soil composition to help optimize crop yield and quality.',
  },
  {
    icon: <FaCloudSun />,
    title: 'Daily Weather Reports',
    description: 'Providing daily weather updates to help you plan your agricultural activities.',
  },
  {
    icon: <FaBell />,
    title: 'Severe Weather Alerts',
    description: 'Get alerts about severe weather conditions to protect your crops and assets.',
  },
  {
    icon: <FaUmbrella />,
    title: 'Weather Forecasts',
    description: 'Accurate weather forecasts to plan your farming activities more effectively.',
  },
  {
    icon: <FaChartLine />,
    title: 'Weather-based Insurance Products',
    description: 'Insurance products tailored to weather risks, helping you secure your investments.',
  },
];

const Services = () => {
  return (
    <div id='services' className="service-list">
      <h2>Our Services</h2>
      <div className="service-cards-container">
        {services.map((service, index) => (
          <ServiceCard
            key={index}
            icon={service.icon}
            title={service.title}
            description={service.description}
          />
        ))}
      </div>
    </div>
  );
};

export default Services;
