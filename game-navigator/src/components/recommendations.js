import React, { useEffect, useState } from 'react';

function Recommendations() {
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    fetch('recommendations/')
      .then(response => response.json())
      .then(data => setRecommendations(data.recommended_games));
  }, []);

  return (
    <div>
      <h2>Recommended Games</h2>
      <ul>
        {recommendations.map(game => (
          <li key={game.id}>{game.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default Recommendations;
