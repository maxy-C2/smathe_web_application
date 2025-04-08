import React from "react";
import "./styles/AboutUs.css";
import onions from "../assets/onions.jpg";

function AboutUs() {
  return (
    <div className="about-us-container">
      <section id="about-us" className="about-us">
        <div className="about-us-content">
          <div className="about-us-text">
            <div className="h1-text">
              <div>Smart weather</div>
              <div>stations using AI,</div>
              <div>ML, IoT, and cloud</div>
              <div>for accurate real-time</div>
              <div>forecasts.</div>
            </div>
            <p className="p-text">
              We are BlitzAgroTech, a technological startup implementing a smart weather station
              through machine learning algorithms, artificial intelligence, cloud servers and IoT
              sensors to provide real-time, accurate weather information beforehand.
            </p>
          </div>
          <div className="about-us-image">
            <img src={onions} alt="Cultivating Through Innovation" />
          </div>
        </div>
      </section>
    </div>
  );
}

export default AboutUs;
