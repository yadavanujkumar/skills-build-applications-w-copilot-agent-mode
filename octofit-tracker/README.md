# OctoFit Tracker 🏃‍♂️

A comprehensive fitness tracking application built for Mergington High School students to log activities, compete in teams, and achieve fitness goals.

![OctoFit Tracker](https://img.shields.io/badge/OctoFit-Tracker-blue?style=for-the-badge&logo=github)
![Django](https://img.shields.io/badge/Django-4.1.7-green?style=flat&logo=django)
![React](https://img.shields.io/badge/React-18+-blue?style=flat&logo=react)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=flat&logo=bootstrap)

## 🎯 Project Overview

OctoFit Tracker is a full-stack web application designed to motivate high school students to stay active through gamification, team competition, and social features. Built using modern web technologies with GitHub Copilot agent mode assistance.

### 🌟 Key Features

- **User Authentication & Profiles**: Secure registration and login with personalized fitness profiles
- **Activity Logging**: Track workouts with 10+ activity types and intensity levels
- **Points System**: Gamified experience with points calculation based on duration and intensity
- **Team Management**: Create and join teams for group challenges and competitions
- **Leaderboards**: Individual and team rankings with real-time updates
- **Achievement System**: Earn badges for fitness milestones and consistency
- **Weekly Challenges**: Participate in school-wide fitness challenges
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## 🏗️ Architecture

### Backend (Django REST Framework)
```
octofit-tracker/backend/
├── octofit_tracker/
│   ├── apps/
│   │   ├── users/          # User authentication & profiles
│   │   ├── activities/     # Activity logging & tracking
│   │   ├── teams/          # Team management & competitions
│   │   └── leaderboard/    # Rankings & achievements
│   ├── settings.py         # Django configuration
│   └── urls.py            # API routing
├── requirements.txt        # Python dependencies
└── manage.py              # Django management script
```

### Frontend (React + Bootstrap)
```
octofit-tracker/frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.js    # User dashboard with stats
│   │   ├── Activities.js   # Activity logging interface
│   │   ├── Teams.js        # Team management
│   │   ├── Leaderboard.js  # Rankings & achievements
│   │   ├── Profile.js      # User profile management
│   │   └── ...            # Auth & navigation components
│   ├── App.js             # Main application with routing
│   └── index.js           # Application entry point
└── package.json           # Node.js dependencies
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+ & npm
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yadavanujkumar/skills-build-applications-w-copilot-agent-mode.git
   cd skills-build-applications-w-copilot-agent-mode/octofit-tracker
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8000
   ```

3. **Frontend Setup** (in a new terminal)
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/

### Demo Access
- **Username**: `demo`
- **Password**: `demo`

## 📱 Application Screenshots

### Home Page
Beautiful landing page with app features and call-to-action buttons.

### Dashboard
Personal dashboard showing user stats, recent activities, and quick actions.

### Activity Logging
Intuitive interface for logging workouts with real-time points calculation.

### Team Management
Create and join teams with visual progress indicators and member management.

### Leaderboards
Multi-tab interface showing individual rankings, team competitions, and achievements.

## 🔧 Technology Stack

### Backend
- **Django 4.1.7** - Web framework
- **Django REST Framework** - API development
- **SQLite** - Database (MongoDB-ready)
- **Python 3.8+** - Programming language

### Frontend
- **React 18+** - JavaScript library
- **React Router DOM** - Client-side routing
- **Bootstrap 5** - CSS framework
- **JavaScript ES6+** - Programming language

### Development Tools
- **GitHub Codespaces** - Cloud development environment
- **GitHub Copilot** - AI-powered code assistance
- **npm** - Package manager
- **Git** - Version control

## 🏫 Educational Use Case

Designed specifically for **Mergington High School**, OctoFit Tracker addresses the challenge of keeping students physically active outside of required PE classes. The application:

- **Motivates** students through gamification and friendly competition
- **Tracks** progress with detailed analytics and reporting
- **Connects** students through team-based challenges
- **Rewards** consistency and achievement with a comprehensive badge system
- **Engages** the school community in fitness initiatives

## 🎮 Gamification Features

### Points System
- Activities earn points based on duration and intensity
- Different multipliers for activity types and difficulty levels
- Weekly and total point tracking

### Achievement Badges
- "First Steps" - Log your first activity
- "Consistency King" - 7 days in a row
- "Point Master" - Earn 1000+ total points
- "Team Player" - Join a team
- "Distance Demon" - Run 100km total
- "Strength Superstar" - 50 strength activities

### Team Competitions
- Create custom teams with unique colors and descriptions
- Team rankings based on combined member points
- Team challenges and competitions
- Captain and moderator roles

## 📊 API Endpoints

### Users
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User authentication
- `GET /api/users/me/` - Current user profile
- `PUT /api/users/me/` - Update user profile

### Activities
- `GET /api/activities/` - List activities
- `POST /api/activities/` - Log new activity
- `GET /api/activities/summary/` - User activity statistics
- `GET /api/activities/types/` - Available activity types

### Teams
- `GET /api/teams/` - List public teams
- `POST /api/teams/` - Create new team
- `POST /api/teams/{id}/join/` - Join a team
- `GET /api/teams/my_teams/` - User's teams

### Leaderboard
- `GET /api/leaderboard/overall/` - Overall rankings
- `GET /api/leaderboard/weekly/` - Weekly rankings
- `GET /api/leaderboard/achievements/` - Available achievements

## 🔮 Future Enhancements

- **Mobile App** - Native iOS and Android applications
- **Fitness Tracker Integration** - Connect with Fitbit, Apple Health, Google Fit
- **Social Features** - Activity feeds and social sharing
- **Advanced Analytics** - Detailed progress reports and insights
- **Coach Dashboard** - Teacher tools for monitoring student progress
- **Real-time Notifications** - Push notifications for challenges and achievements

## 🤝 Contributing

This project was built as part of the GitHub Skills exercise for learning GitHub Copilot agent mode. Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **GitHub Copilot** - AI-powered development assistance
- **Mergington High School** - Educational context and requirements
- **Django & React Communities** - Excellent documentation and resources
- **Bootstrap Team** - Beautiful and responsive UI components

---

**Built with ❤️ using GitHub Copilot Agent Mode**

*OctoFit Tracker - Empowering students to achieve their fitness goals through technology and community.*