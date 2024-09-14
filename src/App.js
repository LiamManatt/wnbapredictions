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
  const getBackgroundColor = (ou) => {
    return ou === "under" ? "red" : ou === "over" ? "green" : "transparent";
  };

  return (
    <div className="App">
      <h1>WNBA Predictions</h1>
      <button onClick={sortPredictions}>Sort Predictions</button>
      <table>
        <thead>
          <tr>
            <th>Prediction</th>
            {statTypes.map(stat => (
              <th key={stat}>{stat}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {Array.from({ length: maxPredictions }).map((_, rowIndex) => (
            <tr key={rowIndex}>
              <td>{rowIndex === 0 ? 'Prediction' : ''}</td>
              {statTypes.map(stat => {
                const prediction = predictionsByStat[stat][rowIndex];
                return (
                  <td
                    key={stat}
                    style={{ backgroundColor: prediction ? getBackgroundColor(prediction.OU) : 'transparent' }}
                  >
                    {prediction ? (
                      <>
                        <div>
                          <strong>Prediction:</strong> {prediction.prediction}
                        </div>
                        <div>
                          <strong>Line:</strong> {prediction.line}
                        </div>
                        <div>{prediction.name} ({prediction.team})</div>
                        <div>
                          {isCriteriaMet(prediction) && <span className="star">&#9733;</span>}
                        </div>
                      </>
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
