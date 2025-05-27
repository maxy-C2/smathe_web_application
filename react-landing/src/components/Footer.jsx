import React from "react";
import "./styles/Footer.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
    faYoutube,
    faGithub,
    faFacebook,
    faLinkedin
} from "@fortawesome/free-brands-svg-icons";
import { faCopyright } from "@fortawesome/free-solid-svg-icons";

function Footer(){
    return (
        <footer className="footer">
        <div className="copyright-infor">
            <span style={{ paddingRight: 5 }}>Copyright </span>
            © {" "}
            <span style={{ paddingLeft: 5 }}>
                {new Date().getFullYear()} BlitzAgroTech. All Rights
                Reserved.
            </span>
        </div>
        {/* <a
            href=""
            target="_blank"
            className="item3"
        >
            <FontAwesomeIcon icon={faLinkedin} />
        </a> */}
        
        </footer>
    )
}

export default Footer;
