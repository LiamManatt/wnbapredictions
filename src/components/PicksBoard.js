import React from 'react';

const PicksBoard = ({ picks, onPickSelect }) => {
  const calculatePercentageDifference = (prediction, line) => {
    return ((prediction - line) / line * 100).toFixed(2);
  };

  return (
    <div className="picks-board">
      {picks.map((pick, index) => {
        const percentageDiff = calculatePercentageDifference(pick.prediction, pick.line);
        const isOver = pick.prediction > pick.line;

        return (
          <div
            key={index}
            className={`pick-card ${pick.taken === 1 ? 'taken' : ''}`}
            onClick={() => onPickSelect(pick)}
          >
            <h3>{pick.name}</h3>
            <div className="stat-row">
              <span className="stat-label">Team:</span>
              <span className="stat-value">{pick.team}</span>
            </div>
            <div className="stat-row">
              <span className="stat-label">Stat:</span>
              <span className="stat-value">{pick.stat}</span>
            </div>
            <div className="stat-row">
              <span className="stat-label">Prediction:</span>
              <span className={`stat-value ${isOver ? 'over' : 'under'}`}>
                {pick.prediction?.toFixed(2)}
              </span>
            </div>
            <div className="stat-row">
              <span className="stat-label">Line:</span>
              <span className="stat-value">{pick.line}</span>
            </div>
            <div className="stat-row percentage-diff">
              <span className="stat-label">Difference:</span>
              <span className={`stat-value ${isOver ? 'over' : 'under'}`}>
                {isOver ? '+' : ''}{percentageDiff}%
              </span>
            </div>
            {pick.taken === 1 && <span className="taken-marker">✓ SUGGESTED</span>}
          </div>
        );
      })}
    </div>
  );
};

export default PicksBoard;

