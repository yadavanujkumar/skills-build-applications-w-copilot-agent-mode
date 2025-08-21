import React, { useState } from 'react';

const Activities = () => {
  const [activities, setActivities] = useState([
    {
      id: 1,
      name: "Morning Run",
      type: "Running",
      duration: 30,
      intensity: "Moderate",
      points: 75,
      date: "2024-08-21",
      distance: 5.2
    },
    {
      id: 2,
      name: "Weight Training",
      type: "Strength",
      duration: 45,
      intensity: "Vigorous", 
      points: 90,
      date: "2024-08-20"
    },
    {
      id: 3,
      name: "Basketball Practice",
      type: "Sports",
      duration: 60,
      intensity: "Vigorous",
      points: 120,
      date: "2024-08-19"
    }
  ]);

  const [showModal, setShowModal] = useState(false);
  const [newActivity, setNewActivity] = useState({
    name: '',
    type: 'Running',
    duration: '',
    intensity: 'Moderate',
    distance: '',
    date: new Date().toISOString().split('T')[0]
  });

  const activityTypes = [
    'Running', 'Walking', 'Cycling', 'Swimming', 'Strength', 'Sports', 
    'Yoga', 'Dance', 'Hiking', 'Other'
  ];

  const intensityLevels = ['Light', 'Moderate', 'Vigorous', 'Very Vigorous'];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewActivity(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const calculatePoints = (duration, intensity, type) => {
    let basePoints = parseInt(duration) || 0;
    const multipliers = {
      'Light': 1,
      'Moderate': 1.5,
      'Vigorous': 2,
      'Very Vigorous': 2.5
    };
    return Math.round(basePoints * (multipliers[intensity] || 1));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const points = calculatePoints(newActivity.duration, newActivity.intensity, newActivity.type);
    
    const activity = {
      id: activities.length + 1,
      ...newActivity,
      duration: parseInt(newActivity.duration),
      distance: newActivity.distance ? parseFloat(newActivity.distance) : null,
      points
    };

    setActivities([activity, ...activities]);
    setNewActivity({
      name: '',
      type: 'Running',
      duration: '',
      intensity: 'Moderate',
      distance: '',
      date: new Date().toISOString().split('T')[0]
    });
    setShowModal(false);
  };

  return (
    <div className="container">
      <div className="row">
        <div className="col-12">
          <div className="d-flex justify-content-between align-items-center mb-4">
            <h1>My Activities</h1>
            <button 
              className="btn btn-primary"
              onClick={() => setShowModal(true)}
            >
              📝 Log New Activity
            </button>
          </div>
        </div>
      </div>

      {/* Activity Summary */}
      <div className="row mb-4">
        <div className="col-md-3">
          <div className="card text-center">
            <div className="card-body">
              <h3 className="text-primary">{activities.length}</h3>
              <p className="text-muted mb-0">Total Activities</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-center">
            <div className="card-body">
              <h3 className="text-success">
                {activities.reduce((sum, activity) => sum + activity.duration, 0)}
              </h3>
              <p className="text-muted mb-0">Total Minutes</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-center">
            <div className="card-body">
              <h3 className="text-info">
                {activities.reduce((sum, activity) => sum + activity.points, 0)}
              </h3>
              <p className="text-muted mb-0">Total Points</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-center">
            <div className="card-body">
              <h3 className="text-warning">
                {activities.filter(a => a.distance).reduce((sum, activity) => sum + (activity.distance || 0), 0).toFixed(1)}
              </h3>
              <p className="text-muted mb-0">Total km</p>
            </div>
          </div>
        </div>
      </div>

      {/* Activities List */}
      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Recent Activities</h5>
            </div>
            <div className="card-body">
              {activities.length === 0 ? (
                <div className="text-center py-4">
                  <p className="text-muted">No activities logged yet. Start by adding your first workout!</p>
                  <button 
                    className="btn btn-primary"
                    onClick={() => setShowModal(true)}
                  >
                    Log Your First Activity
                  </button>
                </div>
              ) : (
                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead>
                      <tr>
                        <th>Activity</th>
                        <th>Type</th>
                        <th>Duration</th>
                        <th>Intensity</th>
                        <th>Distance</th>
                        <th>Points</th>
                        <th>Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      {activities.map(activity => (
                        <tr key={activity.id}>
                          <td>
                            <strong>{activity.name}</strong>
                          </td>
                          <td>
                            <span className="badge bg-secondary">{activity.type}</span>
                          </td>
                          <td>{activity.duration} min</td>
                          <td>
                            <span className={`badge ${
                              activity.intensity === 'Light' ? 'bg-success' :
                              activity.intensity === 'Moderate' ? 'bg-warning' :
                              activity.intensity === 'Vigorous' ? 'bg-danger' :
                              'bg-dark'
                            }`}>
                              {activity.intensity}
                            </span>
                          </td>
                          <td>{activity.distance ? `${activity.distance} km` : '-'}</td>
                          <td>
                            <span className="badge bg-primary">{activity.points} pts</span>
                          </td>
                          <td>{activity.date}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Log Activity Modal */}
      {showModal && (
        <div className="modal d-block" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Log New Activity</h5>
                <button 
                  type="button" 
                  className="btn-close"
                  onClick={() => setShowModal(false)}
                ></button>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label">Activity Name</label>
                    <input
                      type="text"
                      className="form-control"
                      name="name"
                      value={newActivity.name}
                      onChange={handleInputChange}
                      placeholder="e.g., Morning Run, Basketball Practice"
                      required
                    />
                  </div>

                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label className="form-label">Type</label>
                      <select
                        className="form-select"
                        name="type"
                        value={newActivity.type}
                        onChange={handleInputChange}
                        required
                      >
                        {activityTypes.map(type => (
                          <option key={type} value={type}>{type}</option>
                        ))}
                      </select>
                    </div>
                    <div className="col-md-6 mb-3">
                      <label className="form-label">Duration (minutes)</label>
                      <input
                        type="number"
                        className="form-control"
                        name="duration"
                        value={newActivity.duration}
                        onChange={handleInputChange}
                        min="1"
                        required
                      />
                    </div>
                  </div>

                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label className="form-label">Intensity</label>
                      <select
                        className="form-select"
                        name="intensity"
                        value={newActivity.intensity}
                        onChange={handleInputChange}
                        required
                      >
                        {intensityLevels.map(level => (
                          <option key={level} value={level}>{level}</option>
                        ))}
                      </select>
                    </div>
                    <div className="col-md-6 mb-3">
                      <label className="form-label">Distance (km, optional)</label>
                      <input
                        type="number"
                        className="form-control"
                        name="distance"
                        value={newActivity.distance}
                        onChange={handleInputChange}
                        step="0.1"
                        min="0"
                      />
                    </div>
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Date</label>
                    <input
                      type="date"
                      className="form-control"
                      name="date"
                      value={newActivity.date}
                      onChange={handleInputChange}
                      max={new Date().toISOString().split('T')[0]}
                      required
                    />
                  </div>

                  <div className="alert alert-info">
                    <small>
                      Estimated points: <strong>{calculatePoints(newActivity.duration, newActivity.intensity, newActivity.type)}</strong> 
                      {newActivity.duration && (
                        <span className="text-muted"> (based on {newActivity.duration} min at {newActivity.intensity} intensity)</span>
                      )}
                    </small>
                  </div>
                </div>
                <div className="modal-footer">
                  <button 
                    type="button" 
                    className="btn btn-secondary"
                    onClick={() => setShowModal(false)}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    Log Activity
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Activities;