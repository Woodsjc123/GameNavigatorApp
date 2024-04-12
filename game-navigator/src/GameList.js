import React, { useState, useEffect } from 'react';

function GameList() {
  const [games, setGames] = useState([]);

  useEffect(() => {
    fetch('/api/games/')
      .then((response) => response.json())
      .then((data) => setGames(data))
      .catch((error) => console.error('Error fetching game data:', error));
  }, []);

  return (
    <div>
      <h2>Game List</h2>
      <ul>
        {games.map((game) => (
          <li key={game.id}>
            <h3>{game.title}</h3>
            <p>Release Date: {game.release_date}</p>
            <p>Rating: {game.rating}</p>
            <p>Platforms: {game.platforms.map(platform => platform.name).join(', ')}</p>
            <p>Genres: {game.genres.map(genre => genre.name).join(', ')}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default GameList;
