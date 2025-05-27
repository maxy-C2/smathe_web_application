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
        {links.map((link, index) => (
          <div key={index} className="nav-item">
            {link.href ? (
              <ScrollLink
                to={link.href.substring(1)} // Remove the '#' for scroll target
                smooth={true}
                duration={500}
                className="nav-link"
                activeClass="active"
                spy={true}
                onClick={toggleMenu} // Close menu on click
              >
                {link.name}
              </ScrollLink>
            ) : link.onClick ? (
              <button
                onClick={() => {
                  toggleMenu();
                  link.onClick();
                }}
                className="nav-link nav-button"
              >
                {link.name}
              </button>
            ) : null}
          </div>
        ))}
      </nav>
      <div className="menu-icon" onClick={toggleMenu}>
        ☰
      </div>
    </header>
  );
}

export default Navigation;
