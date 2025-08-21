import React, { useState } from 'react';

const Teams = () => {
  const [teams, setTeams] = useState([
    {
      id: 1,
      name: "Mergington Runners",
      description: "For students who love running and cardio activities",
      members: 25,
      maxMembers: 30,
      totalPoints: 15420,
      captain: "Alex Johnson",
      color: "#007bff",
      isMember: true
    },
    {
      id: 2,
      name: "Strength Squad",
      description: "Weight training and strength building enthusiasts",
      members: 18,
      maxMembers: 25,
      totalPoints: 12850,
      captain: "Sarah Davis",
      color: "#dc3545",
      isMember: false
    },
    {
      id: 3,
      name: "Sports All-Stars",
      description: "Multi-sport athletes competing in various activities",
      members: 30,
      maxMembers: 35,
      totalPoints: 18750,
      captain: "Mike Chen",
      color: "#28a745",
      isMember: false
    },
    {
      id: 4,
      name: "Yoga & Wellness",
      description: "Focus on flexibility, mindfulness, and overall wellness",
      members: 15,
      maxMembers: 20,
      totalPoints: 8920,
      captain: "Emily Rodriguez",
      color: "#6f42c1",
      isMember: false
    }
  ]);

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newTeam, setNewTeam] = useState({
    name: '',
    description: '',
    maxMembers: 25,
    color: '#007bff'
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewTeam(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCreateTeam = (e) => {
    e.preventDefault();
    const team = {
      id: teams.length + 1,
      ...newTeam,
      members: 1, // Creator is first member
      totalPoints: 0,
      captain: "You", // Current user
      isMember: true
    };

    setTeams([team, ...teams]);
    setNewTeam({
      name: '',
      description: '',
      maxMembers: 25,
      color: '#007bff'
    });
    setShowCreateModal(false);
  };

  const handleJoinTeam = (teamId) => {
    setTeams(teams.map(team => 
      team.id === teamId 
        ? { ...team, members: team.members + 1, isMember: true }
        : team
    ));
  };

  const handleLeaveTeam = (teamId) => {
    setTeams(teams.map(team => 
      team.id === teamId 
        ? { ...team, members: team.members - 1, isMember: false }
        : team
    ));
  };

  const myTeams = teams.filter(team => team.isMember);
  const availableTeams = teams.filter(team => !team.isMember);

  return (
    <div className="container">
      <div className="row">
        <div className="col-12">
          <div className="d-flex justify-content-between align-items-center mb-4">
            <h1>Teams</h1>
            <button 
              className="btn btn-primary"
              onClick={() => setShowCreateModal(true)}
            >
              👥 Create Team
            </button>
          </div>
        </div>
      </div>

      {/* My Teams */}
      {myTeams.length > 0 && (
        <div className="row mb-5">
          <div className="col-12">
            <h3 className="mb-3">My Teams</h3>
            <div className="row">
              {myTeams.map(team => (
                <div key={team.id} className="col-md-6 col-lg-4 mb-3">
                  <div className="card border-2" style={{borderColor: team.color}}>
                    <div className="card-header d-flex justify-content-between align-items-center" 
                         style={{backgroundColor: team.color, color: 'white'}}>
                      <h6 className="mb-0">{team.name}</h6>
                      <span className="badge bg-light text-dark">Member</span>
                    </div>
                    <div className="card-body">
                      <p className="card-text text-muted">{team.description}</p>
                      <div className="mb-3">
                        <div className="d-flex justify-content-between text-sm">
                          <span>Members</span>
                          <span>{team.members}/{team.maxMembers}</span>
                        </div>
                        <div className="progress" style={{height: '6px'}}>
                          <div 
                            className="progress-bar" 
                            style={{
                              width: `${(team.members / team.maxMembers) * 100}%`,
                              backgroundColor: team.color
                            }}
                          ></div>
                        </div>
                      </div>
                      <div className="row text-center">
                        <div className="col-6">
                          <small className="text-muted">Total Points</small>
                          <div className="fw-bold">{team.totalPoints.toLocaleString()}</div>
                        </div>
                        <div className="col-6">
                          <small className="text-muted">Captain</small>
                          <div className="fw-bold">{team.captain}</div>
                        </div>
                      </div>
                    </div>
                    <div className="card-footer">
                      <button 
                        className="btn btn-outline-danger btn-sm"
                        onClick={() => handleLeaveTeam(team.id)}
                      >
                        Leave Team
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Available Teams */}
      <div className="row">
        <div className="col-12">
          <h3 className="mb-3">
            {myTeams.length > 0 ? 'Other Teams' : 'Available Teams'}
          </h3>
          {availableTeams.length === 0 ? (
            <div className="text-center py-5">
              <h5 className="text-muted">No other teams available</h5>
              <p className="text-muted">Create your own team to get started!</p>
              <button 
                className="btn btn-primary"
                onClick={() => setShowCreateModal(true)}
              >
                Create First Team
              </button>
            </div>
          ) : (
            <div className="row">
              {availableTeams.map(team => (
                <div key={team.id} className="col-md-6 col-lg-4 mb-3">
                  <div className="card h-100">
                    <div className="card-header d-flex justify-content-between align-items-center"
                         style={{backgroundColor: `${team.color}20`, borderColor: team.color}}>
                      <h6 className="mb-0" style={{color: team.color}}>{team.name}</h6>
                      {team.members >= team.maxMembers && (
                        <span className="badge bg-warning">Full</span>
                      )}
                    </div>
                    <div className="card-body">
                      <p className="card-text text-muted">{team.description}</p>
                      <div className="mb-3">
                        <div className="d-flex justify-content-between text-sm">
                          <span>Members</span>
                          <span>{team.members}/{team.maxMembers}</span>
                        </div>
                        <div className="progress" style={{height: '6px'}}>
                          <div 
                            className="progress-bar" 
                            style={{
                              width: `${(team.members / team.maxMembers) * 100}%`,
                              backgroundColor: team.color
                            }}
                          ></div>
                        </div>
                      </div>
                      <div className="row text-center">
                        <div className="col-6">
                          <small className="text-muted">Total Points</small>
                          <div className="fw-bold">{team.totalPoints.toLocaleString()}</div>
                        </div>
                        <div className="col-6">
                          <small className="text-muted">Captain</small>
                          <div className="fw-bold">{team.captain}</div>
                        </div>
                      </div>
                    </div>
                    <div className="card-footer">
                      <button 
                        className="btn btn-primary btn-sm w-100"
                        onClick={() => handleJoinTeam(team.id)}
                        disabled={team.members >= team.maxMembers}
                      >
                        {team.members >= team.maxMembers ? 'Team Full' : 'Join Team'}
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Create Team Modal */}
      {showCreateModal && (
        <div className="modal d-block" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Create New Team</h5>
                <button 
                  type="button" 
                  className="btn-close"
                  onClick={() => setShowCreateModal(false)}
                ></button>
              </div>
              <form onSubmit={handleCreateTeam}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label">Team Name</label>
                    <input
                      type="text"
                      className="form-control"
                      name="name"
                      value={newTeam.name}
                      onChange={handleInputChange}
                      placeholder="Enter team name"
                      required
                    />
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Description</label>
                    <textarea
                      className="form-control"
                      name="description"
                      value={newTeam.description}
                      onChange={handleInputChange}
                      rows="3"
                      placeholder="Describe your team's focus and goals"
                      required
                    ></textarea>
                  </div>

                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label className="form-label">Max Members</label>
                      <input
                        type="number"
                        className="form-control"
                        name="maxMembers"
                        value={newTeam.maxMembers}
                        onChange={handleInputChange}
                        min="5"
                        max="100"
                        required
                      />
                    </div>
                    <div className="col-md-6 mb-3">
                      <label className="form-label">Team Color</label>
                      <input
                        type="color"
                        className="form-control form-control-color"
                        name="color"
                        value={newTeam.color}
                        onChange={handleInputChange}
                        title="Choose team color"
                      />
                    </div>
                  </div>

                  <div className="alert alert-info">
                    <small>
                      <strong>Note:</strong> As the team creator, you will automatically become the team captain.
                    </small>
                  </div>
                </div>
                <div className="modal-footer">
                  <button 
                    type="button" 
                    className="btn btn-secondary"
                    onClick={() => setShowCreateModal(false)}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    Create Team
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

export default Teams;