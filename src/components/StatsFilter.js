import React from 'react';

const StatsFilter = ({ stats, selectedStats, onSelectStats }) => {
  const handleStatClick = (stat) => {
    if (stat === 'All') {
      onSelectStats(selectedStats.length === stats.length - 1 ? [] : stats.slice(1));
    } else {
      onSelectStats(
        selectedStats.includes(stat)
          ? selectedStats.filter(s => s !== stat)
          : [...selectedStats, stat]
      );
    }
  };

  return (
    <div className="filter stats-filter">
      <h3>Filter by Stat:</h3>
      <div className="filter-options">
        {stats.map(stat => (
          <div
            key={stat}
            className={`filter-option ${selectedStats.includes(stat) || (stat === 'All' && selectedStats.length === stats.length - 1) ? 'selected' : ''}`}
            onClick={() => handleStatClick(stat)}
          >
            {stat}
          </div>
        ))}
      </div>
    </div>
  );
};

export default StatsFilter;

