import React, { useState, useEffect } from 'react';
import './css/GameList.css';
import placeholder from './components/placeholder.jpg';

const GameList = () => {
  const [games, setGames] = useState([]);
  const [addedGames, setAddedGames] = useState([]);
  const [recommendations, setRecommendations] = useState([]);

  const getCsrfToken = () => {
    const csrfToken = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken'))
      ?.split('=')[1];
    return csrfToken;
  };

  useEffect(() => {
    const fetchGames = async () => {
      try {
        const response = await fetch('/api/games/');
        const data = await response.json();
        setGames(data);
      } catch (error) {
        console.error('Error fetching games:', error);
      }
    };

    const fetchRecommendations = async () => {
      try {
        const response = await fetch('/api/recommend/');
        const data = await response.json();
        setRecommendations(data);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      }
    };

    fetchGames();
    fetchRecommendations();
  }, []);

  const handleAddToPlayed = async (gameId) => {
    try {
      const response = await fetch(`/api/add_game/${gameId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        credentials: 'include',
        body: JSON.stringify({ game_id: gameId })
      });
      if (response.ok) {
        console.log(`Game with ID ${gameId} added to played list.`);
        setAddedGames(current => [...current, gameId]);
      } else {
        console.error('Failed to add game to played games:', response.statusText);
      }
    } catch (error) {
      console.error('Error adding game to played games:', error);
    }
  };

  return (
    <div>
      <h2>Game List</h2>
      <div className="game-list-container">
        <ul className="game-list">
          {games.map((game) => (
            <li key={game.id} className="game-item">
              <img
                src={game.preview_image || placeholder}
                alt={game.title}
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = placeholder;
                }}
                style={{ width: '266px', height: '400px', objectFit: 'cover' }}
              />
              <div className="game-details">
                <span className="game-title">{game.title}</span>
                {!addedGames.includes(game.id) && (
                  <button onClick={() => handleAddToPlayed(game.id)} className="add-to-played-btn">+</button>
                )}
              </div>
            </li>
          ))}
        </ul>
      </div>

      <h2>Recommended for You</h2>
      <div className="game-list-container">
        <ul className="game-list">
          {recommendations.map((game) => (
            <li key={game.id} className="game-item">
              <img
                src={game.preview_image || placeholder}
                alt={game.title}
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = placeholder;
                }}
                style={{ width: '266px', height: '400px', objectFit: 'cover' }}
              />
              <div className="game-details">
                <span className="game-title">{game.title}</span>
                {!addedGames.includes(game.id) && (
                  <button onClick={() => handleAddToPlayed(game.id)} className="add-to-played-btn">+</button>
                )}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default GameList;
