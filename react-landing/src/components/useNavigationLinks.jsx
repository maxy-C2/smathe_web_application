import { useState } from 'react';
import AboutUs from './AboutUs';
import Home from './Home';

const useNavigationLinks = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const links = [
    { name: 'Home', href: '#home' },
    { name: 'About Us', href: '#about-us' },
    { name: 'Services', href: '#services' },
    { name: 'Contact Us', href: '#contact-us' },
    { name: 'Sign Up', onClick: () => window.location.href ='/userLogs/signup/' },
    { name: 'Sign in', onClick: () => window.location.href= '/userLogs/signin/' },
  ];

  return {
    isOpen,
    toggleMenu,
    links,
  };
};

export default useNavigationLinks;
