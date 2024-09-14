import React, { useState } from "react";
import "./App.css";
import pp from "./icons/prizepicks.png";  // PrizePicks icon
import betr from "./icons/betr.png";      // Betr icon
import predictionsData from "./data/predictions.json"; // Import JSON file

function App() {
  const [predictions, setPredictions] = useState(predictionsData);
  const [selectedSportsbooks, setSelectedSportsbooks] = useState([]);

  const sortPredictions = () => {
    const sorted = [...predictions].sort((a, b) => {
      const diffA = Math.abs((a.prediction - a.line) / a.line);
      const diffB = Math.abs((b.prediction - b.line) / b.line);
      return diffB - diffA; // Sorting in descending order
    });
    setPredictions(sorted);
  };

  const toggleSportsbook = (sportsbook) => {
    setSelectedSportsbooks((prevSelected) =>
      prevSelected.includes(sportsbook)
        ? prevSelected.filter((s) => s !== sportsbook)
        : [...prevSelected, sportsbook]
    );
  };

  // Function to get the icon based on the book
  const getBookIcon = (book) => {
    switch (book) {
      case "betr":
        return betr;
      case "pp":
        return pp;
      default:
        return null; // or a default icon
    }
  };

  // Function to determine the background color based on OU
  const getBackgroundColor = (ou) => {
    return ou === "under" ? "red" : ou === "over" ? "green" : "transparent";
  };

  return (
    <div className="App">
      <h1>WNBA Predictions</h1>
      <div className="sportsbook-icons">
        <img
          src={pp}
          alt="PrizePicks"
          className={`sportsbook-icon ${
            selectedSportsbooks.includes("PrizePicks") ? "selected" : ""
          }`}
          onClick={() => toggleSportsbook("PrizePicks")}
        />
        <img
          src={betr}
          alt="Betr"
          className={`sportsbook-icon ${
            selectedSportsbooks.includes("Betr") ? "selected" : ""
          }`}
          onClick={() => toggleSportsbook("Betr")}
        />
      </div>
      <button onClick={sortPredictions}>Sort Predictions</button>
      <ul>
        {predictions.map((prediction, index) => (
          <li
            key={index}
            style={{ backgroundColor: getBackgroundColor(prediction.OU) }}
            className="prediction-item"
          >
            {prediction.name} ({prediction.team}): {prediction.prediction}{" "}
            {prediction.stat}
            <br />
            {getBookIcon(prediction.book) && (
              <img
                src={getBookIcon(prediction.book)}
                alt={prediction.book}
                className="sportsbook-icon"
              />
            )}
            <br />
            Line: {prediction.line} | Odds: {prediction.odds}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
