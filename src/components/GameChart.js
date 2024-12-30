import React, { useEffect, useRef } from 'react';

const GameChart = ({ games, dates, line, stat }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    
    // Set canvas size
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    
    // Scale canvas
    ctx.scale(dpr, dpr);

    const width = rect.width;
    const height = rect.height;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // Set background
    ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
    ctx.fillRect(0, 0, width, height);

    // Calculate chart area
    const chartMargin = { top: 10, right: 10, bottom: 20, left: 40 };
    const chartWidth = width - chartMargin.left - chartMargin.right;
    const chartHeight = height - chartMargin.top - chartMargin.bottom;

    // Calculate y-axis scale
    const maxValue = Math.max(...games, line);
    const yScale = chartHeight / maxValue;

    // Draw y-axis
    ctx.strokeStyle = '#666';
    ctx.beginPath();
    ctx.moveTo(chartMargin.left, chartMargin.top);
    ctx.lineTo(chartMargin.left, height - chartMargin.bottom);
    ctx.stroke();

    // Draw y-axis labels
    ctx.fillStyle = '#a0a0a0';
    ctx.font = '12px Arial';
    ctx.textAlign = 'right';
    ctx.textBaseline = 'middle';
    for (let i = 0; i <= maxValue; i += Math.ceil(maxValue / 5)) {
      const y = height - chartMargin.bottom - i * yScale;
      ctx.fillText(i.toString(), chartMargin.left - 5, y);
      
      // Draw horizontal grid lines
      ctx.strokeStyle = 'rgba(102, 102, 102, 0.3)';
      ctx.beginPath();
      ctx.moveTo(chartMargin.left, y);
      ctx.lineTo(width - chartMargin.right, y);
      ctx.stroke();
    }

    // Draw line (now thicker and in blue)
    ctx.strokeStyle = '#0000ff';
    ctx.lineWidth = 3; // Increased line width
    ctx.setLineDash([5, 5]);
    const lineY = height - chartMargin.bottom - line * yScale;
    ctx.beginPath();
    ctx.moveTo(chartMargin.left, lineY);
    ctx.lineTo(width - chartMargin.right, lineY);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.lineWidth = 1; // Reset line width for other elements

    // Draw bars
    const barWidth = (chartWidth - (games.length + 1) * 10) / games.length;
    const bars = games.map((game, i) => {
      const x = chartMargin.left + 10 + i * (barWidth + 10);
      const barHeight = game * yScale;
      const y = height - chartMargin.bottom - barHeight;

      // Set color based on line and position
      if (game === line) {
        ctx.fillStyle = '#808080'; // Gray for last game if it matches the line
      } else {
        ctx.fillStyle = game > line ? '#00ff00' : '#ff0000';
      }
      ctx.fillRect(x, y, barWidth, barHeight);

      // Draw date
      ctx.fillStyle = '#a0a0a0';
      ctx.font = '10px Arial';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'top';
      const date = new Date(dates[i]).toLocaleDateString('en-US', { month: 'numeric', day: 'numeric' });
      ctx.fillText(date, x + barWidth / 2, height - chartMargin.bottom + 5);

      return { x, y, width: barWidth, height: barHeight, value: game, date: dates[i] };
    });

    const redrawChart = () => {
      // Redraw background
      ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
      ctx.fillRect(0, 0, width, height);

      // Redraw y-axis and labels
      ctx.strokeStyle = '#666';
      ctx.beginPath();
      ctx.moveTo(chartMargin.left, chartMargin.top);
      ctx.lineTo(chartMargin.left, height - chartMargin.bottom);
      ctx.stroke();
      ctx.fillStyle = '#a0a0a0';
      ctx.font = '12px Arial';
      ctx.textAlign = 'right';
      ctx.textBaseline = 'middle';
      for (let i = 0; i <= maxValue; i += Math.ceil(maxValue / 5)) {
        const y = height - chartMargin.bottom - i * yScale;
        ctx.fillText(i.toString(), chartMargin.left - 5, y);
        ctx.strokeStyle = 'rgba(102, 102, 102, 0.3)';
        ctx.beginPath();
        ctx.moveTo(chartMargin.left, y);
        ctx.lineTo(width - chartMargin.right, y);
        ctx.stroke();
      }

      // Redraw line
      ctx.strokeStyle = '#0000ff';
      ctx.lineWidth = 3; 
      ctx.setLineDash([5, 5]);
      const lineY = height - chartMargin.bottom - line * yScale;
      ctx.beginPath();
      ctx.moveTo(chartMargin.left, lineY);
      ctx.lineTo(width - chartMargin.right, lineY);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.lineWidth = 1; 

      // Redraw bars
      const barWidth = (chartWidth - (games.length + 1) * 10) / games.length;
      bars.forEach((bar) => {
        const x = bar.x;
        const barHeight = bar.height;
        const y = bar.y;
        if (bar.value === line) {
          ctx.fillStyle = '#808080'; 
        } else {
          ctx.fillStyle = bar.value > line ? '#00ff00' : '#ff0000';
        }
        ctx.fillRect(x, y, barWidth, barHeight);
        ctx.fillStyle = '#a0a0a0';
        ctx.font = '10px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        ctx.fillText(bar.date, x + barWidth / 2, height - chartMargin.bottom + 5);
      });
    };


    canvas.addEventListener('mousemove', (event) => {
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      let tooltipShown = false;

      for (const bar of bars) {
        if (x >= bar.x && x <= bar.x + bar.width && y >= bar.y && y <= bar.y + bar.height) {
          // Clear previous tooltip
          ctx.clearRect(0, 0, width, height);
          redrawChart(); // Redraw the entire chart

          // Draw new tooltip
          const tooltipWidth = 120;
          const tooltipHeight = 50;
          const tooltipX = Math.min(Math.max(x - tooltipWidth / 2, 0), width - tooltipWidth);
          const tooltipY = Math.max(bar.y - tooltipHeight - 10, 10);

          // Draw tooltip background
          ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
          ctx.beginPath();
          ctx.moveTo(tooltipX + 5, tooltipY);
          ctx.lineTo(tooltipX + tooltipWidth - 5, tooltipY);
          ctx.quadraticCurveTo(tooltipX + tooltipWidth, tooltipY, tooltipX + tooltipWidth, tooltipY + 5);
          ctx.lineTo(tooltipX + tooltipWidth, tooltipY + tooltipHeight - 5);
          ctx.quadraticCurveTo(tooltipX + tooltipWidth, tooltipY + tooltipHeight, tooltipX + tooltipWidth - 5, tooltipY + tooltipHeight);
          ctx.lineTo(tooltipX + 5, tooltipY + tooltipHeight);
          ctx.quadraticCurveTo(tooltipX, tooltipY + tooltipHeight, tooltipX, tooltipY + tooltipHeight - 5);
          ctx.lineTo(tooltipX, tooltipY + 5);
          ctx.quadraticCurveTo(tooltipX, tooltipY, tooltipX + 5, tooltipY);
          ctx.closePath();
          ctx.fill();

          // Draw tooltip content
          ctx.fillStyle = '#ffffff';
          ctx.font = 'bold 14px Arial';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(bar.value.toFixed(2), tooltipX + tooltipWidth / 2, tooltipY + 15);
          
          ctx.font = '12px Arial';
          ctx.fillText(bar.date, tooltipX + tooltipWidth / 2, tooltipY + 35);

          tooltipShown = true;
          break;
        }
      }

      if (!tooltipShown) {
        ctx.clearRect(0, 0, width, height);
        redrawChart(); // Redraw the entire chart if no tooltip is shown
      }
    });

    // Clear tooltip when mouse leaves canvas
    canvas.addEventListener('mouseleave', () => {
      ctx.clearRect(0, 0, width, height);
      redrawChart();
    });

  }, [games, dates, line, stat]);

  return (
    <canvas
      ref={canvasRef}
      style={{ width: '100%', height: '250px', display: 'block' }}
    />
  );
};

export default GameChart;

