import React, { useState } from 'react';

const Leaderboard = () => {
  const [activeTab, setActiveTab] = useState('individual');

  const individualLeaderboard = [
    { rank: 1, username: "FitnessAlex", name: "Alex Johnson", points: 2450, weeklyPoints: 420, change: "+2" },
    { rank: 2, username: "RunnerSarah", name: "Sarah Davis", points: 2380, weeklyPoints: 380, change: "-1" },
    { rank: 3, username: "MikeChen", name: "Mike Chen", points: 2350, weeklyPoints: 450, change: "+1" },
    { rank: 4, username: "EmilyR", name: "Emily Rodriguez", points: 2280, weeklyPoints: 320, change: "0" },
    { rank: 5, username: "TomWilson", name: "Tom Wilson", points: 2150, weeklyPoints: 290, change: "-2" },
    { rank: 6, username: "JessicaLee", name: "Jessica Lee", points: 2080, weeklyPoints: 340, change: "+3" },
    { rank: 7, username: "DavidBrown", name: "David Brown", points: 1950, weeklyPoints: 280, change: "-1" },
    { rank: 8, username: "LisaGreen", name: "Lisa Green", points: 1890, weeklyPoints: 310, change: "+1" },
    { rank: 9, username: "JamesMiller", name: "James Miller", points: 1820, weeklyPoints: 260, change: "0" },
    { rank: 10, username: "AmyTaylor", name: "Amy Taylor", points: 1750, weeklyPoints: 275, change: "+2" },
    { rank: 11, username: "demo", name: "Demo Student", points: 1250, weeklyPoints: 320, change: "+5" },
  ];

  const teamLeaderboard = [
    { rank: 1, teamName: "Sports All-Stars", members: 30, totalPoints: 18750, avgPoints: 625, captain: "Mike Chen" },
    { rank: 2, teamName: "Mergington Runners", members: 25, totalPoints: 15420, avgPoints: 617, captain: "Alex Johnson" },
    { rank: 3, teamName: "Strength Squad", members: 18, totalPoints: 12850, avgPoints: 714, captain: "Sarah Davis" },
    { rank: 4, teamName: "Yoga & Wellness", members: 15, totalPoints: 8920, avgPoints: 595, captain: "Emily Rodriguez" },
    { rank: 5, teamName: "Basketball Stars", members: 20, totalPoints: 8450, avgPoints: 423, captain: "Tom Wilson" },
  ];

  const weeklyChallenge = {
    name: "Step Up Challenge",
    description: "Complete 10 different types of activities this week",
    target: 10,
    participants: 156,
    completions: 23,
    userProgress: 7,
    daysLeft: 3
  };

  const achievements = [
    { name: "First Steps", description: "Log your first activity", icon: "🏃‍♂️", earned: true },
    { name: "Consistency King", description: "Log activities 7 days in a row", icon: "👑", earned: true },
    { name: "Point Master", description: "Earn 1000 total points", icon: "🏆", earned: true },
    { name: "Team Player", description: "Join a team", icon: "👥", earned: true },
    { name: "Distance Demon", description: "Run 100km total", icon: "🏃‍♂️", earned: false },
    { name: "Strength Superstar", description: "Complete 50 strength activities", icon: "💪", earned: false },
  ];

  const getRankBadge = (rank) => {
    if (rank === 1) return "🥇";
    if (rank === 2) return "🥈";
    if (rank === 3) return "🥉";
    return `#${rank}`;
  };

  const getChangeIcon = (change) => {
    if (change.startsWith('+')) return "📈";
    if (change.startsWith('-')) return "📉";
    return "➖";
  };

  const getChangeColor = (change) => {
    if (change.startsWith('+')) return "text-success";
    if (change.startsWith('-')) return "text-danger";
    return "text-muted";
  };

  return (
    <div className="container">
      <div className="row">
        <div className="col-12">
          <h1 className="mb-4">Leaderboard 🏆</h1>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="row mb-4">
        <div className="col-12">
          <ul className="nav nav-pills">
            <li className="nav-item">
              <button 
                className={`nav-link ${activeTab === 'individual' ? 'active' : ''}`}
                onClick={() => setActiveTab('individual')}
              >
                👤 Individual
              </button>
            </li>
            <li className="nav-item">
              <button 
                className={`nav-link ${activeTab === 'teams' ? 'active' : ''}`}
                onClick={() => setActiveTab('teams')}
              >
                👥 Teams
              </button>
            </li>
            <li className="nav-item">
              <button 
                className={`nav-link ${activeTab === 'challenges' ? 'active' : ''}`}
                onClick={() => setActiveTab('challenges')}
              >
                🎯 Challenges
              </button>
            </li>
            <li className="nav-item">
              <button 
                className={`nav-link ${activeTab === 'achievements' ? 'active' : ''}`}
                onClick={() => setActiveTab('achievements')}
              >
                🏅 Achievements
              </button>
            </li>
          </ul>
        </div>
      </div>

      {/* Individual Leaderboard */}
      {activeTab === 'individual' && (
        <div className="row">
          <div className="col-12">
            <div className="card">
              <div className="card-header">
                <h5 className="mb-0">Individual Rankings</h5>
                <small className="text-muted">Based on total points earned</small>
              </div>
              <div className="card-body p-0">
                <div className="table-responsive">
                  <table className="table table-hover mb-0">
                    <thead className="table-light">
                      <tr>
                        <th>Rank</th>
                        <th>Student</th>
                        <th>Total Points</th>
                        <th>Weekly Points</th>
                        <th>Change</th>
                      </tr>
                    </thead>
                    <tbody>
                      {individualLeaderboard.map((user, index) => (
                        <tr key={user.username} className={user.username === 'demo' ? 'table-warning' : ''}>
                          <td>
                            <span className="fs-5">{getRankBadge(user.rank)}</span>
                          </td>
                          <td>
                            <div>
                              <strong>{user.name}</strong>
                              <br />
                              <small className="text-muted">@{user.username}</small>
                            </div>
                          </td>
                          <td>
                            <span className="badge bg-primary fs-6">
                              {user.points.toLocaleString()} pts
                            </span>
                          </td>
                          <td>
                            <span className="badge bg-success">
                              {user.weeklyPoints} pts
                            </span>
                          </td>
                          <td>
                            <span className={getChangeColor(user.change)}>
                              {getChangeIcon(user.change)} {user.change}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Team Leaderboard */}
      {activeTab === 'teams' && (
        <div className="row">
          <div className="col-12">
            <div className="card">
              <div className="card-header">
                <h5 className="mb-0">Team Rankings</h5>
                <small className="text-muted">Based on total team points</small>
              </div>
              <div className="card-body p-0">
                <div className="table-responsive">
                  <table className="table table-hover mb-0">
                    <thead className="table-light">
                      <tr>
                        <th>Rank</th>
                        <th>Team</th>
                        <th>Members</th>
                        <th>Total Points</th>
                        <th>Avg per Member</th>
                        <th>Captain</th>
                      </tr>
                    </thead>
                    <tbody>
                      {teamLeaderboard.map((team) => (
                        <tr key={team.teamName}>
                          <td>
                            <span className="fs-5">{getRankBadge(team.rank)}</span>
                          </td>
                          <td>
                            <strong>{team.teamName}</strong>
                          </td>
                          <td>
                            <span className="badge bg-info">{team.members}</span>
                          </td>
                          <td>
                            <span className="badge bg-primary fs-6">
                              {team.totalPoints.toLocaleString()} pts
                            </span>
                          </td>
                          <td>
                            <span className="badge bg-success">
                              {team.avgPoints} pts
                            </span>
                          </td>
                          <td>
                            <small>{team.captain}</small>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Weekly Challenges */}
      {activeTab === 'challenges' && (
        <div className="row">
          <div className="col-lg-8">
            <div className="card mb-4">
              <div className="card-header">
                <h5 className="mb-0">Current Weekly Challenge</h5>
              </div>
              <div className="card-body">
                <h6 className="text-primary">{weeklyChallenge.name}</h6>
                <p className="text-muted">{weeklyChallenge.description}</p>
                
                <div className="row mb-3">
                  <div className="col-md-6">
                    <small className="text-muted">Your Progress</small>
                    <div className="progress mb-2">
                      <div 
                        className="progress-bar bg-primary" 
                        style={{width: `${(weeklyChallenge.userProgress / weeklyChallenge.target) * 100}%`}}
                      ></div>
                    </div>
                    <small>{weeklyChallenge.userProgress}/{weeklyChallenge.target} activities</small>
                  </div>
                  <div className="col-md-6">
                    <div className="text-center">
                      <h3 className="text-warning">{weeklyChallenge.daysLeft}</h3>
                      <small className="text-muted">Days Left</small>
                    </div>
                  </div>
                </div>

                <div className="row text-center">
                  <div className="col-4">
                    <h4 className="text-primary">{weeklyChallenge.participants}</h4>
                    <small className="text-muted">Participants</small>
                  </div>
                  <div className="col-4">
                    <h4 className="text-success">{weeklyChallenge.completions}</h4>
                    <small className="text-muted">Completed</small>
                  </div>
                  <div className="col-4">
                    <h4 className="text-info">
                      {Math.round((weeklyChallenge.completions / weeklyChallenge.participants) * 100)}%
                    </h4>
                    <small className="text-muted">Success Rate</small>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="col-lg-4">
            <div className="card">
              <div className="card-header">
                <h6 className="mb-0">Challenge Tips</h6>
              </div>
              <div className="card-body">
                <ul className="list-unstyled">
                  <li className="mb-2">🏃‍♂️ Try running or walking</li>
                  <li className="mb-2">💪 Add some strength training</li>
                  <li className="mb-2">🏀 Play team sports</li>
                  <li className="mb-2">🧘‍♀️ Don't forget yoga/stretching</li>
                  <li className="mb-2">🚴‍♂️ Go for a bike ride</li>
                </ul>
                <button className="btn btn-success btn-sm w-100">
                  Join Challenge
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Achievements */}
      {activeTab === 'achievements' && (
        <div className="row">
          <div className="col-12">
            <div className="card">
              <div className="card-header">
                <h5 className="mb-0">Achievements Gallery</h5>
                <small className="text-muted">Earn badges by completing fitness milestones</small>
              </div>
              <div className="card-body">
                <div className="row">
                  {achievements.map((achievement, index) => (
                    <div key={index} className="col-md-6 col-lg-4 mb-3">
                      <div className={`card h-100 ${achievement.earned ? 'border-success' : 'border-light'}`}>
                        <div className="card-body text-center">
                          <div 
                            className="fs-1 mb-3"
                            style={{filter: achievement.earned ? 'none' : 'grayscale(100%)'}}
                          >
                            {achievement.icon}
                          </div>
                          <h6 className="card-title">{achievement.name}</h6>
                          <p className="card-text text-muted small">{achievement.description}</p>
                          {achievement.earned ? (
                            <span className="badge bg-success">✓ Earned</span>
                          ) : (
                            <span className="badge bg-secondary">🔒 Locked</span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Leaderboard;