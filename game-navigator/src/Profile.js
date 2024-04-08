import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './css/Profile.css';

const Profile = () => {
  const [userData, setUserData] = useState({
    profilePic: '',
    favoriteGenres: [],
    preferredPlatforms: [],
    playedGames: [],
  });

  const [gameHours, setGameHours] = useState({});
  
  const [selectedFile, setSelectedFile] = useState(null);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const { data } = await axios.get('/api/profile/');
      setUserData({
        profilePic: data.profile_pic,
        favoriteGenres: data.favorite_genres || [],
        preferredPlatforms: data.preferred_platforms || [],
        playedGames: data.played_games || [],
      });

      const initialGameHours = data.played_games.reduce((acc, game) => ({
        ...acc,
        [game.id]: game.hoursPlayed || 0,
      }), {});
      setGameHours(initialGameHours);
    } 
    catch (error) {
      console.error("Error fetching user data:", error);
    }
  };

  const handleProfilePicSubmit = async (event) => { // Not working atm, need to finish
    event.preventDefault();
    if (!selectedFile) {
      alert("Please select an image.");
      return;
    }

    const formData = new FormData();
    formData.append('profile_pic', selectedFile);

    try {
      const response = await axios.post('/api/profilepic/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      if (response.status === 200) {
        alert("Profile picture updated.");
        fetchUserData();
      }
    } 
    catch (error) {
      alert("An error occurred.");
      console.error(error);
    }
  };

  const handleHoursChange = (gameId, hours) => {
    setGameHours((prevHours) => ({
      ...prevHours,
      [gameId]: hours,
    }));
  };

  const handleSubmitHours = async () => {
    try {
      await axios.post('/api/updatehours/', { hours: gameHours }, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      alert("Hours updated.");
      fetchUserData();
    } 
    catch (error) {
      alert("An error occurred.");
      console.error(error);
    }
  };

  return (
    <div className="profile">
      <div className="profile-pic-div">
        <img src={userData.profilePic || 'defaultProfilePicURL'} alt="Profile" />
        <form onSubmit={handleProfilePicSubmit}>
          <input type="file" onChange={(e) => setSelectedFile(e.target.files[0])} />
          <button type="submit">Upload New Picture</button>
        </form>
      </div>
      <div className="stats">
        <h2>User Statistics</h2>
        <p>Favorite Genre: {userData.favoriteGenres.join(', ')}</p>
        <div>
          <h3>Played Games</h3>
          <ul>
            {userData.playedGames.map((game) => (
              <li key={game.id}>
                {game.title}
                <input
                  type="number"
                  value={gameHours[game.id] || 0}
                  onChange={(e) => handleHoursChange(game.id, e.target.value)}
                  min="0"
                  style={{ marginLeft: '10px' }}
                />
              </li>
            ))}
          </ul>
          <button onClick={handleSubmitHours}>Save Hours</button>
        </div>
      </div>
    </div>
  );
};

export default Profile;
