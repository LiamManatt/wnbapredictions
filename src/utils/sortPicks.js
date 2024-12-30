export function sortPicksByPercentageDifference(picks) {
    return picks.sort((a, b) => {
      // Prioritize taken picks
      if (a.taken === 1 && b.taken !== 1) return -1;
      if (b.taken === 1 && a.taken !== 1) return 1;
  
      // If both are taken or both are not taken, sort by percentage difference
      const percentageDiffA = Math.abs((a.prediction - a.line) / a.line) * 100;
      const percentageDiffB = Math.abs((b.prediction - b.line) / b.line) * 100;
      return percentageDiffB - percentageDiffA;
    });
  }
  
  