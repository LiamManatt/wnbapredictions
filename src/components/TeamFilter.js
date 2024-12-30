import React from 'react';

const TeamFilter = ({ teams, selectedTeams, onSelectTeams }) => {
  const handleTeamClick = (team) => {
    if (team === 'All') {
      onSelectTeams(selectedTeams.length === teams.length - 1 ? [] : teams.slice(1));
    } else {
      onSelectTeams(
        selectedTeams.includes(team)
          ? selectedTeams.filter(t => t !== team)
          : [...selectedTeams, team]
      );
    }
  };

  return (
    <div className="filter team-filter">
      <h3>Filter by Team:</h3>
      <div className="filter-options">
        {teams.map(team => (
          <div
            key={team}
            className={`filter-option ${selectedTeams.includes(team) || (team === 'All' && selectedTeams.length === teams.length - 1) ? 'selected' : ''}`}
            onClick={() => handleTeamClick(team)}
          >
            {team}
          </div>
        ))}
      </div>
    </div>
  );
};

export default TeamFilter;

