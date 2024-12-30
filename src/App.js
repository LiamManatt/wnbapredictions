import React, { useState, useMemo } from 'react';
import PicksBoard from './components/PicksBoard';
import PickDetails from './components/PickDetails';
import TeamFilter from './components/TeamFilter';
import StatsFilter from './components/StatsFilter';
import picksData from './data/picks.json';
import './App.css';
import { sortPicksByPercentageDifference } from './utils/sortPicks';

const App = () => {
  const [selectedPick, setSelectedPick] = useState(null);
  const [selectedTeams, setSelectedTeams] = useState([]);
  const [selectedStats, setSelectedStats] = useState([]);

  const teams = useMemo(() => ['All', ...new Set(picksData.map(pick => pick.team))], []);
  const stats = useMemo(() => ['All', ...new Set(picksData.map(pick => pick.stat))], []);

  const filteredPicks = useMemo(() => {
    const filtered = picksData.filter(pick => {
      const teamMatch = selectedTeams.length === 0 || selectedTeams.includes(pick.team);
      const statMatch = selectedStats.length === 0 || selectedStats.includes(pick.stat);
      return teamMatch && statMatch;
    });
    return sortPicksByPercentageDifference(filtered);
  }, [selectedTeams, selectedStats]);

  return (
    <div className="app">
      <h1>AI Player Props</h1>
      <div className="filters">
        <TeamFilter teams={teams} selectedTeams={selectedTeams} onSelectTeams={setSelectedTeams} />
        <StatsFilter stats={stats} selectedStats={selectedStats} onSelectStats={setSelectedStats} />
      </div>
      <PicksBoard picks={filteredPicks} onPickSelect={setSelectedPick} />
      {selectedPick && (
        <PickDetails pick={selectedPick} onClose={() => setSelectedPick(null)} />
      )}
    </div>
  );
};

export default App;

