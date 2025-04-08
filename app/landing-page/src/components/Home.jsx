import React from "react";
import Navigation from "./Navigation";
import "./styles/Home.css"

function Home(){
    return (
        <div className="home-container" id="home">
        <div className="home-container-content">
        <Navigation/>
        <div className="heading-text">
            <h1>Transform Your Farming with Real-Time Weather Data</h1>
            <h2>Accurate, Portable, and Easy-to-use Weather Stations for Modern Agriculture</h2>
        </div>
        <button className="btn">SIGN UP</button>
        </div>
        </div>

    )

}


export default Home;