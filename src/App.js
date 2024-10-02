import React, { useState, useEffect } from "react";
import { Bar } from 'react-chartjs-2'; // Import the Bar chart from react-chartjs-2
import "./App.css";
import predictionsData from "./data/predictions.json"; // Import JSON file

// Register the chart components
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import annotationPlugin from 'chartjs-plugin-annotation';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, annotationPlugin);


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
  const [predictions, setPredictions] = useState([]);
  const [flippedCards, setFlippedCards] = useState({});
  const [userChoices, setUserChoices] = useState({});
  const [selectedCards, setSelectedCards] = useState([]);
  const [selectedCard, setSelectedCard] = useState(null);

  useEffect(() => {
    const sortedPredictions = [...predictionsData].sort((a, b) => {
      const diffA = Math.abs((a.prediction - a.line) / a.line);
      const diffB = Math.abs((b.prediction - b.line) / b.line);
      return diffB - diffA;
    });
    setPredictions(sortedPredictions);
  }, []);

  const isCriteriaMet = (prediction) => {
    const { stat, prediction: pred, line } = prediction;
    if (criteria[stat]) {
      const absoluteDifference = Math.abs(pred - line);
      return absoluteDifference >= criteria[stat];
    }
    return false;
  };

  const handleCardClick = (index) => {
    setFlippedCards((prevFlipped) => ({
      ...prevFlipped,
      [index]: !prevFlipped[index],
    }));
    setSelectedCard(predictions[index]);
  };

  const getGradientBackground = (index) => {
    const userChoice = userChoices[index];
    if (userChoice === "over") {
      return `linear-gradient(to bottom, green, white)`;
    } else if (userChoice === "under") {
      return `linear-gradient(to bottom, red, white)`;
    }
    return "transparent";
  };

  const handleOverUnderClick = (index, option) => {
    setUserChoices((prevChoices) => ({
      ...prevChoices,
      [index]: option,
    }));

    setSelectedCards((prevSelected) => {
      const alreadySelected = prevSelected.find((card) => card.index === index);
      if (!alreadySelected) {
        return [...prevSelected, { ...predictions[index], index, ou: option }];
      }
      return prevSelected;
    });
  };

  const handleRemoveCard = (index) => {
    setSelectedCards((prevSelected) =>
      prevSelected.filter((card) => card.index !== index)
    );

    setUserChoices((prevChoices) => {
      const updatedChoices = { ...prevChoices };
      delete updatedChoices[index];
      return updatedChoices;
    });
  };

  // Bar chart data generation based on selectedCard.last_games
  const chartData = selectedCard ? {
    labels: selectedCard.last_games.map((_, index) => `Game ${index + 1}`),
    datasets: [{
      label: `${selectedCard.name}'s ${selectedCard.stat} in Last Games`,
      data: selectedCard.last_games, 
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1,
    }]
  } : null;

  return (
    <div className="App">
      <div className="header">
        <p className="logo">WNBA WIZARD</p>
      </div>
      <div className="base">
        <div className="section-container">
          <div className="section">
            <h2 className="section-title">Statistics</h2>
          </div>
          <div className="section">
            <h2 className="section-title">Model Predictions</h2>
          </div>
          <div className="section">
            <h2 className="section-title">Your Picks</h2>
          </div>
        </div>

        <div className="flex-container">
          <div className="left-container">
            {selectedCard ? (
              <div className="card-details">
                <p className="leftplayer-name"><strong>Player:</strong> {selectedCard.name}</p>
                <p className="leftteam-name"><strong>Team:</strong> {selectedCard.team}</p>
                <p className="leftstat"><strong>Stat:</strong> {selectedCard.stat}</p>

                {/* Render the bar chart if last_games data is available */}
                {selectedCard.last_games && (
  <div className="chart-container">
    <Bar
      data={{
        labels: selectedCard.last_games.map((_, index) => `Game ${index + 1}`).reverse(), // Reverse the x-axis labels
        datasets: [{
          label: `${selectedCard.name}'s ${selectedCard.stat} in Last 5 Games`,
          data: selectedCard.last_games.slice().reverse(), // Reverse the order of data
          backgroundColor: selectedCard.last_games.map((gameStat) =>
            gameStat > selectedCard.line
              ? 'rgba(0, 255, 0, 0.6)' // Green if greater
              : gameStat < selectedCard.line
              ? 'rgba(255, 0, 0, 0.6)' // Red if less
              : 'rgba(128, 128, 128, 0.6)' // Grey if equal
          ).reverse(), // Reverse the background color array
          borderColor: selectedCard.last_games.map((gameStat) =>
            gameStat > selectedCard.line
              ? 'rgba(0, 128, 0, 1)' // Darker green for border
              : gameStat < selectedCard.line
              ? 'rgba(128, 0, 0, 1)' // Darker red for border
              : 'rgba(128, 128, 128, 1)' // Darker grey for border
          ).reverse(), // Reverse the border color array
          borderWidth: 1,
        }],
      }}
      options={{
        scales: {
          x: {
            reverse: false, // Reverse the X-axis order
            ticks: {
              color: 'white', // Change X-axis label color to blue
              font: {
                size: 20, // Change X-axis label font size
              },
            },
          },
          y: {
            beginAtZero: true,
            ticks: {
              color: 'green', // Change Y-axis label color to green
              font: {
                size: 16, // Change Y-axis label font size
              },
            },
          },
        },
        plugins: {
          legend: {
            labels: {
              color: 'white', // Change legend label color to purple
              font: {
                size: 20, // Change legend font size
              },
            },
          },
          tooltip: {
            titleColor: 'yellow', // Change the color of the tooltip title
            titleFont: {
              size: 16, // Change tooltip title font size
            },
            bodyColor: 'orange',  // Change the color of the tooltip body
            bodyFont: {
              size: 14, // Change tooltip body font size
            },
          },
          annotation: {
            annotations: {
              line1: {
                type: 'line',
                yMin: selectedCard.line,
                yMax: selectedCard.line,
                borderColor: 'rgba(0, 0, 255, 0.7)', // Line color (e.g., blue)
                borderWidth: 2,
                borderDash: [5, 5], // Dotted line
                label: {
                  enabled: true,
                  content: `Line: ${selectedCard.line}`,
                  position: 'end',
                  backgroundColor: 'rgba(0, 0, 0, 0.7)',
                  color: 'white', // Label text color
                  font: {
                    size: 12, // Change the font size for the line label
                  },
                  padding: 6,
                },
              },
            },
          },
        },
      }}
    />
  </div>
)}
<p className="leftplayer-line" style={{ fontSize: '25px', fontWeight: 'bold' }}>
  <strong>Line:   </strong>{selectedCard.line}
</p>

<p className="leftplayer-prediction" style={{ fontSize: '25px', fontWeight: 'bold' }}>
  <strong>Prediction:   </strong> 
  <span style={{ color: selectedCard.prediction < selectedCard.line ? 'red' : 'green' }}>
    {selectedCard.prediction}
  </span>
</p>

<p className="leftplayer-prediction" style={{ fontSize: '25px', fontWeight: 'bold' }}>
  <strong>Season Average:   </strong> 
  <span style={{ color: selectedCard.stat_avg < selectedCard.line ? 'red' : 'green' }}>
    {selectedCard.stat_avg}
  </span>
</p>

<p className="leftplayer-line" style={{ fontSize: '25px', fontWeight: 'bold' }}>
  <strong>Opponent {selectedCard.stat} Allowed:   </strong> {selectedCard.stat_allowed}
</p>

<p className="leftplayer-prediction" style={{ fontSize: '25px', fontWeight: 'bold' }}>
  <strong>Opponent {selectedCard.stat} Allowed Rank:   </strong> 
  <span style={{ color: selectedCard.stat_allowed_rank < 7 ? 'red' : 'green' }}>
    {selectedCard.stat_allowed_rank}
  </span>
</p>

<p className="leftplayer-line" style={{ fontSize: '25px', fontWeight: 'bold' }}>
  <strong>Positional {selectedCard.stat} Allowed:   </strong> {selectedCard.pos_allowed}
</p>

<p className="leftplayer-prediction" style={{ fontSize: '25px', fontWeight: 'bold' }}>
  <strong>Positional {selectedCard.stat} Allowed Rank:   </strong> 
  <span style={{ color: selectedCard.pos_allowed_rank < 7 ? 'red' : 'green' }}>
    {selectedCard.pos_allowed_rank}
  </span>
</p>


              </div>
            ) : (
              <p>No card selected.</p>
            )}
          </div>

          <div className="sortable-container">
            {predictions.map((prediction, index) => {
              if (selectedCards.some((card) => card.index === index)) {
                return null;
              }

              const { stat, prediction: pred, line } = prediction;
              const isFlipped = flippedCards[index];
              const background = getGradientBackground(index);

              return (
                <div
                  key={index}
                  className={`item ${isCriteriaMet(prediction) ? 'criteria-met' : ''}`}
                  onClick={() => handleCardClick(index)}
                  style={{ background }}
                >
                  <div className="player-info">
                    <span style={{ fontSize: '25px' }}>{prediction.name} </span>
                    <span style={{ fontSize: '14px', color: 'gray' }}>({prediction.team})</span>
                    <p className="stat-text">{stat}</p>
                    <p className="prediction-text">{pred} | {line}</p>
                  </div>
                  <div className="over-under-container">
                    <div
                      className={`over ${userChoices[index] === 'over' ? 'selected' : ''}`}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleOverUnderClick(index, 'over');
                      }}
                    >
                      Over
                    </div>
                    <div
                      className={`under ${userChoices[index] === 'under' ? 'selected' : ''}`}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleOverUnderClick(index, 'under');
                      }}
                    >
                      Under
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="right-container">
            {selectedCards.map((card) => (
              <div
                key={card.index}
                className={`item ${isCriteriaMet(card) ? 'criteria-met' : ''}`}
                style={{ background: getGradientBackground(card.index) }}
                onClick={() => handleCardClick(card.index)}
              >
                <div
                  className="player-info"
                  style={{ marginTop: '100px' }}
                >
                  <span style={{ fontSize: '25px' }}>{card.name} </span>
                  <span style={{ fontSize: '14px', color: 'gray' }}>({card.team})</span>
                  <p className="stat-text">{card.stat}</p>
                  <p className="prediction-text">{card.prediction} | {card.line}</p>
                  <p className="ou-text">{card.ou}</p>
                  <button className="remove-button" onClick={() => handleRemoveCard(card.index)}>
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
