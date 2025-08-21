import React, { useState, useEffect } from 'react';

const Profile = () => {
  const [user, setUser] = useState(null);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    grade_level: '',
    height_cm: '',
    weight_kg: '',
    fitness_goals: '',
    preferred_activities: ''
  });

  useEffect(() => {
    // Get user info from localStorage
    const userData = localStorage.getItem('user');
    if (userData) {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);
      setFormData({
        first_name: parsedUser.first_name || '',
        last_name: parsedUser.last_name || '',
        email: parsedUser.email || '',
        grade_level: parsedUser.grade_level || '',
        height_cm: parsedUser.height_cm || '',
        weight_kg: parsedUser.weight_kg || '',
        fitness_goals: parsedUser.fitness_goals || '',
        preferred_activities: parsedUser.preferred_activities || 'Running, Basketball, Swimming'
      });
    }
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Update user data in localStorage (in real app, would send to API)
    const updatedUser = { ...user, ...formData };
    setUser(updatedUser);
    localStorage.setItem('user', JSON.stringify(updatedUser));
    setEditing(false);
  };

  const calculateBMI = () => {
    if (formData.height_cm && formData.weight_kg) {
      const heightM = formData.height_cm / 100;
      return (formData.weight_kg / (heightM * heightM)).toFixed(1);
    }
    return null;
  };

  const userStats = {
    totalPoints: 1250,
    totalActivities: 45,
    totalDistance: 156.7,
    avgWeeklyActivities: 8,
    joinDate: "2024-01-15",
    currentRank: 11,
    achievements: 4
  };

  if (!user) {
    return (
      <div className="container">
        <div className="text-center">
          <h2>Please log in to view your profile</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="row">
        <div className="col-12">
          <h1 className="mb-4">My Profile</h1>
        </div>
      </div>

      <div className="row">
        {/* Profile Information */}
        <div className="col-lg-8">
          <div className="card mb-4">
            <div className="card-header d-flex justify-content-between align-items-center">
              <h5 className="mb-0">Personal Information</h5>
              {!editing ? (
                <button 
                  className="btn btn-outline-primary btn-sm"
                  onClick={() => setEditing(true)}
                >
                  ✏️ Edit
                </button>
              ) : (
                <div>
                  <button 
                    className="btn btn-outline-secondary btn-sm me-2"
                    onClick={() => setEditing(false)}
                  >
                    Cancel
                  </button>
                  <button 
                    form="profile-form"
                    type="submit"
                    className="btn btn-primary btn-sm"
                  >
                    Save
                  </button>
                </div>
              )}
            </div>
            <div className="card-body">
              {!editing ? (
                <div className="row">
                  <div className="col-md-6">
                    <div className="mb-3">
                      <label className="form-label fw-bold">Full Name</label>
                      <p>{user.first_name} {user.last_name}</p>
                    </div>
                    <div className="mb-3">
                      <label className="form-label fw-bold">Username</label>
                      <p>@{user.username}</p>
                    </div>
                    <div className="mb-3">
                      <label className="form-label fw-bold">Email</label>
                      <p>{user.email}</p>
                    </div>
                    <div className="mb-3">
                      <label className="form-label fw-bold">Grade Level</label>
                      <p>{formData.grade_level ? `${formData.grade_level}th Grade` : 'Not specified'}</p>
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="mb-3">
                      <label className="form-label fw-bold">Height</label>
                      <p>{formData.height_cm ? `${formData.height_cm} cm` : 'Not specified'}</p>
                    </div>
                    <div className="mb-3">
                      <label className="form-label fw-bold">Weight</label>
                      <p>{formData.weight_kg ? `${formData.weight_kg} kg` : 'Not specified'}</p>
                    </div>
                    <div className="mb-3">
                      <label className="form-label fw-bold">BMI</label>
                      <p>{calculateBMI() || 'Not available'}</p>
                    </div>
                    <div className="mb-3">
                      <label className="form-label fw-bold">Preferred Activities</label>
                      <p>{formData.preferred_activities || 'Not specified'}</p>
                    </div>
                  </div>
                  <div className="col-12">
                    <div className="mb-3">
                      <label className="form-label fw-bold">Fitness Goals</label>
                      <p>{formData.fitness_goals || 'No goals set yet'}</p>
                    </div>
                  </div>
                </div>
              ) : (
                <form id="profile-form" onSubmit={handleSubmit}>
                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label className="form-label">First Name</label>
                      <input
                        type="text"
                        className="form-control"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleInputChange}
                        required
                      />
                    </div>
                    <div className="col-md-6 mb-3">
                      <label className="form-label">Last Name</label>
                      <input
                        type="text"
                        className="form-control"
                        name="last_name"
                        value={formData.last_name}
                        onChange={handleInputChange}
                        required
                      />
                    </div>
                  </div>

                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label className="form-label">Email</label>
                      <input
                        type="email"
                        className="form-control"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        required
                      />
                    </div>
                    <div className="col-md-6 mb-3">
                      <label className="form-label">Grade Level</label>
                      <select
                        className="form-select"
                        name="grade_level"
                        value={formData.grade_level}
                        onChange={handleInputChange}
                      >
                        <option value="">Select grade</option>
                        <option value="9">9th Grade</option>
                        <option value="10">10th Grade</option>
                        <option value="11">11th Grade</option>
                        <option value="12">12th Grade</option>
                      </select>
                    </div>
                  </div>

                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label className="form-label">Height (cm)</label>
                      <input
                        type="number"
                        className="form-control"
                        name="height_cm"
                        value={formData.height_cm}
                        onChange={handleInputChange}
                        min="100"
                        max="250"
                      />
                    </div>
                    <div className="col-md-6 mb-3">
                      <label className="form-label">Weight (kg)</label>
                      <input
                        type="number"
                        className="form-control"
                        name="weight_kg"
                        value={formData.weight_kg}
                        onChange={handleInputChange}
                        min="30"
                        max="200"
                      />
                    </div>
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Preferred Activities</label>
                    <input
                      type="text"
                      className="form-control"
                      name="preferred_activities"
                      value={formData.preferred_activities}
                      onChange={handleInputChange}
                      placeholder="e.g., Running, Basketball, Swimming"
                    />
                    <div className="form-text">Separate multiple activities with commas</div>
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Fitness Goals</label>
                    <textarea
                      className="form-control"
                      name="fitness_goals"
                      value={formData.fitness_goals}
                      onChange={handleInputChange}
                      rows="3"
                      placeholder="Describe your fitness goals and what you want to achieve"
                    ></textarea>
                  </div>

                  {calculateBMI() && (
                    <div className="alert alert-info">
                      <small>
                        <strong>Current BMI:</strong> {calculateBMI()}
                      </small>
                    </div>
                  )}
                </form>
              )}
            </div>
          </div>
        </div>

        {/* Statistics Sidebar */}
        <div className="col-lg-4">
          <div className="card mb-4">
            <div className="card-header">
              <h6 className="mb-0">Profile Statistics</h6>
            </div>
            <div className="card-body">
              <div className="row text-center">
                <div className="col-6 mb-3">
                  <h4 className="text-primary">{userStats.totalPoints}</h4>
                  <small className="text-muted">Total Points</small>
                </div>
                <div className="col-6 mb-3">
                  <h4 className="text-success">{userStats.totalActivities}</h4>
                  <small className="text-muted">Activities</small>
                </div>
                <div className="col-6 mb-3">
                  <h4 className="text-info">{userStats.totalDistance}</h4>
                  <small className="text-muted">Total km</small>
                </div>
                <div className="col-6 mb-3">
                  <h4 className="text-warning">#{userStats.currentRank}</h4>
                  <small className="text-muted">Current Rank</small>
                </div>
              </div>
              
              <hr />
              
              <div className="d-flex justify-content-between mb-2">
                <span>Member since:</span>
                <span>{new Date(userStats.joinDate).toLocaleDateString()}</span>
              </div>
              <div className="d-flex justify-content-between mb-2">
                <span>Achievements:</span>
                <span>{userStats.achievements} 🏅</span>
              </div>
              <div className="d-flex justify-content-between">
                <span>Weekly average:</span>
                <span>{userStats.avgWeeklyActivities} activities</span>
              </div>
            </div>
          </div>

          {/* Recent Achievements */}
          <div className="card">
            <div className="card-header">
              <h6 className="mb-0">Recent Achievements</h6>
            </div>
            <div className="card-body">
              <div className="list-group list-group-flush">
                <div className="list-group-item d-flex align-items-center px-0">
                  <span className="me-3">🏃‍♂️</span>
                  <div>
                    <h6 className="mb-1">First Steps</h6>
                    <small className="text-muted">Logged first activity</small>
                  </div>
                </div>
                <div className="list-group-item d-flex align-items-center px-0">
                  <span className="me-3">👑</span>
                  <div>
                    <h6 className="mb-1">Consistency King</h6>
                    <small className="text-muted">7 days in a row</small>
                  </div>
                </div>
                <div className="list-group-item d-flex align-items-center px-0">
                  <span className="me-3">🏆</span>
                  <div>
                    <h6 className="mb-1">Point Master</h6>
                    <small className="text-muted">Earned 1000 points</small>
                  </div>
                </div>
                <div className="list-group-item d-flex align-items-center px-0">
                  <span className="me-3">👥</span>
                  <div>
                    <h6 className="mb-1">Team Player</h6>
                    <small className="text-muted">Joined a team</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;