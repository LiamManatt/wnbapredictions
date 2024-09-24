import React, { useState } from "react";
import "./App.css";
import predictionsData from "./data/predictions.json"; // Import JSON file

const criteria = {
  'Pts+Rebs+Asts': 2.0,
  'Points': 1.5,
  'FG Attempted': 1.5,
  'Rebounds': 0.65,
  'Assists': 0.5,
  'Defensive Rebounds': 0.5,
  'Offensive Rebounds': 0.35,
};

function App() {
  const [predictions, setPredictions] = useState(predictionsData);
  const [flippedCards, setFlippedCards] = useState({}); // Track which cards are flipped

  const predictionsByStat = predictions.reduce((acc, prediction) => {
    const { stat } = prediction;
    if (!acc[stat]) {
      acc[stat] = [];
    }
    acc[stat].push(prediction);
    return acc;
  }, {});

  const statTypes = Object.keys(predictionsByStat);
  const maxPredictions = Math.max(...statTypes.map(stat => predictionsByStat[stat].length));

  const sortPredictions = () => {
    const sorted = [...predictions].sort((a, b) => {
      const diffA = Math.abs((a.prediction - a.line) / a.line);
      const diffB = Math.abs((b.prediction - b.line) / b.line);
      return diffB - diffA;
    });
    setPredictions(sorted);
  };

  const isCriteriaMet = (prediction) => {
    const { stat, prediction: pred, line } = prediction;
    if (criteria[stat]) {
      const absoluteDifference = Math.abs(pred - line);
      return absoluteDifference >= criteria[stat];
    }
    return false;
  };

  const getGradientBackground = (ou) => {
    if (ou === "over") {
      return `linear-gradient(to bottom, green, white)`;
    } else if (ou === "under") {
      return `linear-gradient(to bottom, red, white)`;
    }
    return "transparent";
  };

  const handleCardClick = (index) => {
    setFlippedCards((prevFlipped) => ({
      ...prevFlipped,
      [index]: !prevFlipped[index], // Toggle the flipped state
    }));
  };

  return (
    <div className="App">
      <h1>WNBA Predictions</h1>
      <button onClick={sortPredictions}>Sort Predictions</button>
      <table>
        <thead>
          <tr>
            {statTypes.map(stat => (
              <th key={stat}>{stat}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {Array.from({ length: maxPredictions }).map((_, rowIndex) => (
            <tr key={rowIndex}>
              {statTypes.map(stat => {
                const prediction = predictionsByStat[stat][rowIndex];
                const cardIndex = `${stat}-${rowIndex}`; // Unique index for each card

                return (
                  <td
                    key={stat}
                    onClick={() => handleCardClick(cardIndex)}
                    className={`card ${flippedCards[cardIndex] ? "flipped" : ""}`} // Add flipped class based on state
                    style={{
                      background: prediction
                        ? getGradientBackground(prediction.OU)
                        : "transparent",
                    }}
                  >
                    {prediction ? (
                      <div className="card-inner">
                        {/* Front of the card */}
                        <div className="card-front">
                          <div className="star">
                            {isCriteriaMet(prediction) && <span>&#9733;</span>}
                          </div>
                          <div>
                            <strong>{prediction.name} ({prediction.team})</strong>
                          </div>
                          <div>
                            <strong>Line:</strong> {prediction.line}
                          </div>
                          <div>
                            <strong>Prediction:</strong> {prediction.prediction}
                          </div>
                        </div>
                        {/* Back of the card */}
                        <div className="card-back">
                          <div>
                            <strong>More Stats:</strong>
                            <ul>
                              {/* <li>FG%: {prediction.fg_percentage}</li>
                              <li>Rebounds: {prediction.rebounds}</li>
                              <li>Assists: {prediction.assists}</li> */}
                            </ul>
                          </div>
                        </div>
                      </div>
                    ) : (
                      <div>—</div>
                    )}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
