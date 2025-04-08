// ContactUs.js
import React, { useState } from "react";
import ContactOptionCard from "./ContactOptionCard";
import { FaPhoneAlt, FaEnvelope, FaLinkedin } from "react-icons/fa";
import "./styles/ContactUs.css";
import clairePhoto from "../assets/claireProfile.jpeg";
import maxPhoto from "../assets/maxProfile.jpeg";
import einsteinPhoto from "../assets/eisteinProfile.jpeg";

const ContactUs = () => {
  const [selectedOption, setSelectedOption] = useState(null);

  const options = [
    {
      name: "Claire Makuyana",
      role: "Email Support",
      contact: "c.makuyana@blitzagrotech.com",
      whatsappLink: "https://wa.me/263774647520",
      image: clairePhoto,
      type: "email",
    },
    {
      name: "Einstein Makuyana",
      role: "Help Centre",
      contact: "e.makuyana@blitzagrotech.com",
      whatsappLink: "https://wa.me/263774613020",
      image: einsteinPhoto,
      type: "help",
    },
    {
      name: "Max Sibanda",
      role: "Chat Support",
      contact: "m.sibanda@blitzagrotech.com",
      whatsappLink: "https://wa.me/263738963521",
      image: maxPhoto,
      type: "chat",
    },
  ];

  return (
    <div className="contact-us">
      <div className="map-container">
        <iframe
          src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14795.547014317136!2d31.03450783855427!3d-17.825165498921117!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x1931a525a0f0cce3%3A0xb36225b875d02136!2sHarare%2C%20Zimbabwe!5e0!3m2!1sen!2sus!4v1616568446189!5m2!1sen!2sus"
          width="100%"
          height="400"
          style={{ border: 0 }}
          allowFullScreen=""
          loading="lazy"
          title="BlitzAgroTech Location"
        ></iframe>
      </div>
      <div className="contact-info">
        <div className="contact-info-item">
          <FaPhoneAlt size={20} />
          <span>+263 774 613 020</span>
        </div>
        <div className="contact-info-item">
          <FaEnvelope size={20} />
          <span>blitzagrotech@gmail.com</span>
        </div>
        <div className="contact-info-item">
          <FaLinkedin size={20} />
          <a href="https://www.linkedin.com/company/blitzagrotech" target="_blank" rel="noopener noreferrer">
            BlitzAgroTech LinkedIn
          </a>
        </div>
      </div>
      <div className="contact-options">
        {options.map((option, index) => (
          <ContactOptionCard
            key={index}
            option={option}
            onClick={() => window.open(option.whatsappLink, "_blank")}
          />
        ))}
      </div>
      
      <div className="contact-form">
        <h3>Contact Us via Email</h3>
        <form>
          <div>
            <label>Name</label>
            <input type="text" name="name" placeholder="Your Name" required />
          </div>
          <div>
            <label>Email</label>
            <input type="email" name="email" placeholder="Your Email" required />
          </div>
          <div>
            <label>Message</label>
            <textarea name="message" placeholder="Your Message" rows="5" required></textarea>
          </div>
          <button type="submit">Send Message</button>
        </form>
      </div>
    </div>
  );
};

export default ContactUs;
