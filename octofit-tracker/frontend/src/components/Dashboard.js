import React, { useState, useEffect } from 'react';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [stats, setStats] = useState({
    totalPoints: 1250,
    weeklyPoints: 320,
    totalActivities: 45,
    weeklyActivities: 8,
    currentRank: 15,
    teamRank: 3
  });
  const [recentActivities, setRecentActivities] = useState([
    {
      id: 1,
      name: "Morning Run",
      type: "Running",
      duration: 30,
      points: 75,
      date: "2024-08-21"
    },
    {
      id: 2,
      name: "Weight Training",
      type: "Strength",
      duration: 45,
      points: 90,
      date: "2024-08-20"
    },
    {
      id: 3,
      name: "Basketball Practice",
      type: "Sports",
      duration: 60,
      points: 120,
      date: "2024-08-19"
    }
  ]);

  useEffect(() => {
    // Get user info from localStorage
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

  if (!user) {
    return (
      <div className="container">
        <div className="text-center">
          <h2>Please log in to access your dashboard</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="row">
        <div className="col-12">
          <h1 className="mb-4">Welcome back, {user.first_name}! 👋</h1>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="row mb-4">
        <div className="col-md-3 mb-3">
          <div className="card bg-primary text-white">
            <div className="card-body">
              <div className="d-flex justify-content-between">
                <div>
                  <h6 className="card-title">Total Points</h6>
                  <h2 className="mb-0">{stats.totalPoints}</h2>
                </div>
                <div className="align-self-center">
                  <span className="display-6">🏆</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="col-md-3 mb-3">
          <div className="card bg-success text-white">
            <div className="card-body">
              <div className="d-flex justify-content-between">
                <div>
                  <h6 className="card-title">Weekly Points</h6>
                  <h2 className="mb-0">{stats.weeklyPoints}</h2>
                </div>
                <div className="align-self-center">
                  <span className="display-6">📈</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="col-md-3 mb-3">
          <div className="card bg-info text-white">
            <div className="card-body">
              <div className="d-flex justify-content-between">
                <div>
                  <h6 className="card-title">Activities</h6>
                  <h2 className="mb-0">{stats.totalActivities}</h2>
                </div>
                <div className="align-self-center">
                  <span className="display-6">🏃‍♂️</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="col-md-3 mb-3">
          <div className="card bg-warning text-white">
            <div className="card-body">
              <div className="d-flex justify-content-between">
                <div>
                  <h6 className="card-title">Current Rank</h6>
                  <h2 className="mb-0">#{stats.currentRank}</h2>
                </div>
                <div className="align-self-center">
                  <span className="display-6">🎯</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="row">
        {/* Recent Activities */}
        <div className="col-lg-8 mb-4">
          <div className="card">
            <div className="card-header d-flex justify-content-between align-items-center">
              <h5 className="mb-0">Recent Activities</h5>
              <a href="/activities" className="btn btn-sm btn-primary">View All</a>
            </div>
            <div className="card-body">
              {recentActivities.length === 0 ? (
                <p className="text-muted text-center">No activities logged yet. Start by adding your first workout!</p>
              ) : (
                <div className="list-group list-group-flush">
                  {recentActivities.map(activity => (
                    <div key={activity.id} className="list-group-item d-flex justify-content-between align-items-center">
                      <div>
                        <h6 className="mb-1">{activity.name}</h6>
                        <small className="text-muted">
                          {activity.type} • {activity.duration} minutes • {activity.date}
                        </small>
                      </div>
                      <span className="badge bg-primary rounded-pill">
                        {activity.points} pts
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Quick Actions & Progress */}
        <div className="col-lg-4">
          {/* Quick Actions */}
          <div className="card mb-4">
            <div className="card-header">
              <h5 className="mb-0">Quick Actions</h5>
            </div>
            <div className="card-body">
              <div className="d-grid gap-2">
                <a href="/activities" className="btn btn-primary">
                  📝 Log Activity
                </a>
                <a href="/teams" className="btn btn-outline-primary">
                  👥 View Teams
                </a>
                <a href="/leaderboard" className="btn btn-outline-primary">
                  🏆 Leaderboard
                </a>
              </div>
            </div>
          </div>

          {/* Weekly Progress */}
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">This Week's Progress</h5>
            </div>
            <div className="card-body">
              <div className="mb-3">
                <div className="d-flex justify-content-between">
                  <small>Activities</small>
                  <small>{stats.weeklyActivities}/10 goal</small>
                </div>
                <div className="progress">
                  <div 
                    className="progress-bar" 
                    style={{width: `${(stats.weeklyActivities / 10) * 100}%`}}
                  ></div>
                </div>
              </div>
              
              <div className="mb-3">
                <div className="d-flex justify-content-between">
                  <small>Points</small>
                  <small>{stats.weeklyPoints}/500 goal</small>
                </div>
                <div className="progress">
                  <div 
                    className="progress-bar bg-success" 
                    style={{width: `${(stats.weeklyPoints / 500) * 100}%`}}
                  ></div>
                </div>
              </div>

              <div className="text-center">
                <p className="text-muted mb-1">Keep going! You're doing great! 💪</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;