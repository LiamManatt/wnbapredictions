import React from 'react';
import GameChart from './GameChart';

const PickDetails = ({ pick, onClose }) => {
  const getColor = (value, threshold, inverse = false) => {
    if (inverse) {
      return value < threshold ? 'var(--accent-green)' : 'var(--accent-red)';
    }
    return value < threshold ? 'var(--accent-red)' : 'var(--accent-green)';
  };

  return (
    <>
      <div className="backdrop" onClick={onClose} />
      <div className="pick-details">
        <button className="close-button" onClick={onClose}>×</button>
        
        <div className="stats-section">
          <h2>{pick.name}</h2>
          <div className="stat-row">
            <span className="stat-label">Team:</span>
            <span className="stat-value">{pick.team}</span>
          </div>
          <div className="stat-row">
            <span className="stat-label">Opponent:</span>
            <span className="stat-value">{pick.opp}</span>
          </div>
          <div className="stat-row">
            <span className="stat-label">Stat:</span>
            <span className="stat-value">{pick.stat}</span>
          </div>
        </div>

        <div className="stats-chart">
          <h3>{pick.name}'s {pick.stat}:</h3>
          <GameChart 
            games={pick.last_games} 
            dates={pick.last_games_date}
            line={pick.line}
            stat={pick.stat}
          />
        </div>

        <div className="stats-section">
          <div className="stat-row">
            <span className="stat-label">Line:</span>
            <span className="stat-value">{pick.line}</span>
          </div>
          <div className="stat-row">
            <span className="stat-label">Prediction:</span>
            <span className="stat-value" style={{ color: getColor(pick.prediction, pick.line) }}>
              {pick.prediction?.toFixed(2)}
            </span>
          </div>
          <div className="stat-row">
            <span className="stat-label">Season Average:</span>
            <span className="stat-value" style={{ color: getColor(pick.stat_avg, pick.line) }}>
              {pick.stat_avg?.toFixed(2)}
            </span>
          </div>
          <div className="stat-row">
            <span className="stat-label">Last Game vs Opponent:</span>
            <span className="stat-value" style={{ color: getColor(pick.last_game_opp, pick.line) }}>
              {pick.last_game_opp}
            </span>
          </div>
        </div>

        <div className="stats-section">
          <h3>Opponent Stats</h3>
          <div className="stat-row">
            <span className="stat-label">{pick.stat} Allowed:</span>
            <span className="stat-value">{pick.stat_allowed?.toFixed(2)}</span>
          </div>
          <div className="stat-row">
            <span className="stat-label">{pick.stat} Allowed Rank:</span>
            <span className="stat-value" style={{ color: getColor(pick.stat_allowed_rank, 16, false) }}>
              {pick.stat_allowed_rank}
            </span>
          </div>
          <div className="stat-row">
            <span className="stat-label">Positional {pick.stat} Allowed:</span>
            <span className="stat-value">{pick.pos_allowed?.toFixed(2)}</span>
          </div>
          <div className="stat-row">
            <span className="stat-label">Positional {pick.stat} Allowed Rank:</span>
            <span className="stat-value" style={{ color: getColor(pick.pos_allowed_rank, 16, false) }}>
              {pick.pos_allowed_rank}
            </span>
          </div>
        </div>
      </div>
    </>
  );
};

export default PickDetails;

