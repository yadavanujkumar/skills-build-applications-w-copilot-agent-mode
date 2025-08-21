# OctoFit Tracker Backend

This is the Django REST API backend for the OctoFit Tracker fitness app.

## Features

- User authentication and profiles
- Activity logging and tracking
- Team creation and management
- Competitive leaderboard
- Personalized workout suggestions

## API Endpoints

### Users
- `GET /api/users/` - List users
- `POST /api/users/` - Create user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `GET /api/users/{id}/profile/` - Get user profile

### Activities
- `GET /api/activities/` - List activities
- `POST /api/activities/` - Log new activity
- `GET /api/activities/{id}/` - Get activity details
- `PUT /api/activities/{id}/` - Update activity
- `DELETE /api/activities/{id}/` - Delete activity

### Teams
- `GET /api/teams/` - List teams
- `POST /api/teams/` - Create team
- `GET /api/teams/{id}/` - Get team details
- `POST /api/teams/{id}/join/` - Join team
- `POST /api/teams/{id}/leave/` - Leave team

### Leaderboard
- `GET /api/leaderboard/` - Get overall leaderboard
- `GET /api/leaderboard/teams/` - Get team leaderboard
- `GET /api/leaderboard/users/` - Get user leaderboard

## Setup

1. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run development server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

The API will be available at `http://localhost:8000/api/`