import React from 'react';
import { Link as ScrollLink } from 'react-scroll';
import logo from '../assets/logo.png';
import './styles/Navigation.css';
import useNavigationLinks from './useNavigationLinks';

function Navigation() {
  const { isOpen, toggleMenu, links } = useNavigationLinks();

  return (
    <header className="header glass">
      <img src={logo} alt="Logo" className="logo" />
      <nav className={`navbar teachers-navigation-font ${isOpen ? 'open' : ''}`}>
        {links.map((link) => (
          <ScrollLink
            key={link.name}
            to={link.href.substring(1)} // Remove the '#' from href
            smooth={true}
            duration={500}
            className="nav-link"
            activeClass="active"
            spy={true}
          >
            {link.name}
          </ScrollLink>
        ))}
      </nav>
      <div className="menu-icon" onClick={toggleMenu}>
        ☰
      </div>
    </header>
  );
}

export default Navigation;
