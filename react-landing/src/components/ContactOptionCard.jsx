import React from "react";
import "./styles/ContactUs.css";

const ContactOptionCard = ({ option, onClick }) => {
  return (
    <div className="contact-option-card" onClick={onClick}>
      <img src={option.image} alt={option.name} className="contact-image" />
      <h3>{option.name}</h3>
      <p>{option.role}</p>
      <p>{option.contact}</p>
    </div>
  );
};

export default ContactOptionCard;
