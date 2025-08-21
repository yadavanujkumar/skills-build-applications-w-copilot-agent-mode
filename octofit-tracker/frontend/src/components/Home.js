import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  const isAuthenticated = localStorage.getItem('token');

  return (
    <div className="container">
      {/* Hero Section */}
      <div className="row align-items-center min-vh-100 py-5">
        <div className="col-lg-6">
          <h1 className="display-4 fw-bold text-primary mb-4">
            Welcome to OctoFit Tracker
          </h1>
          <p className="lead mb-4">
            Track your fitness journey, compete with friends, and achieve your health goals 
            with Mergington High School's premier fitness tracking app.
          </p>
          <div className="d-flex gap-3">
            {isAuthenticated ? (
              <Link to="/dashboard" className="btn btn-primary btn-lg">
                Go to Dashboard
              </Link>
            ) : (
              <>
                <Link to="/register" className="btn btn-primary btn-lg">
                  Get Started
                </Link>
                <Link to="/login" className="btn btn-outline-primary btn-lg">
                  Login
                </Link>
              </>
            )}
          </div>
        </div>
        <div className="col-lg-6">
          <div className="text-center">
            <div className="bg-light rounded-3 p-5">
              <h2 className="h1">🏃‍♂️</h2>
              <h3 className="text-muted">Start Your Fitness Journey</h3>
              <p className="text-muted">
                Join thousands of students tracking their activities and competing for fitness goals.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="row py-5">
        <div className="col-12">
          <h2 className="text-center mb-5">Why Choose OctoFit Tracker?</h2>
        </div>
        <div className="col-md-4 mb-4">
          <div className="card h-100 border-0 shadow-sm">
            <div className="card-body text-center">
              <div className="display-6 text-primary mb-3">📊</div>
              <h5 className="card-title">Track Activities</h5>
              <p className="card-text">
                Log your workouts, track progress, and earn points for every activity you complete.
              </p>
            </div>
          </div>
        </div>
        <div className="col-md-4 mb-4">
          <div className="card h-100 border-0 shadow-sm">
            <div className="card-body text-center">
              <div className="display-6 text-primary mb-3">👥</div>
              <h5 className="card-title">Join Teams</h5>
              <p className="card-text">
                Create or join teams with your friends and compete in group challenges and competitions.
              </p>
            </div>
          </div>
        </div>
        <div className="col-md-4 mb-4">
          <div className="card h-100 border-0 shadow-sm">
            <div className="card-body text-center">
              <div className="display-6 text-primary mb-3">🏆</div>
              <h5 className="card-title">Compete & Win</h5>
              <p className="card-text">
                Climb the leaderboards, earn achievements, and stay motivated with friendly competition.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Statistics Section */}
      <div className="row py-5 bg-light rounded-3">
        <div className="col-12">
          <h2 className="text-center mb-5">Join the Movement</h2>
        </div>
        <div className="col-md-3 text-center mb-4">
          <h3 className="display-5 text-primary fw-bold">500+</h3>
          <p className="text-muted">Active Students</p>
        </div>
        <div className="col-md-3 text-center mb-4">
          <h3 className="display-5 text-primary fw-bold">50+</h3>
          <p className="text-muted">Teams</p>
        </div>
        <div className="col-md-3 text-center mb-4">
          <h3 className="display-5 text-primary fw-bold">10K+</h3>
          <p className="text-muted">Activities Logged</p>
        </div>
        <div className="col-md-3 text-center mb-4">
          <h3 className="display-5 text-primary fw-bold">1M+</h3>
          <p className="text-muted">Points Earned</p>
        </div>
      </div>

      {/* Call to Action */}
      {!isAuthenticated && (
        <div className="row py-5">
          <div className="col-12 text-center">
            <h2 className="mb-4">Ready to Start Your Fitness Journey?</h2>
            <p className="lead mb-4">
              Join OctoFit Tracker today and start competing with your classmates!
            </p>
            <Link to="/register" className="btn btn-primary btn-lg me-3">
              Sign Up Now
            </Link>
            <Link to="/login" className="btn btn-outline-primary btn-lg">
              Already have an account?
            </Link>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;