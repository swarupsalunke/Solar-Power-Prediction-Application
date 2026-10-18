import "../App.css";
import logo from "../assets/logo.png";

function PageHeader() {
    return (
        <header className="topbar">
            <div className="brand-section">
                <img
                    src={logo}
                    alt="Embed Square Solutions logo"
                    className="company-logo"
                />

                <div className="brand-details">
                    <h2 className="company-name">Embed Square Solutions Pvt. Ltd.</h2>
                    <h1 className="assignment-name">Solar Power Prediction Application</h1>
                </div>
            </div>
        </header>
    );
}

export default PageHeader;