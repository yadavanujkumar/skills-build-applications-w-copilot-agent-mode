# OctoFit Tracker Frontend

This is the React frontend for the OctoFit Tracker fitness app.

## Features

- **User Authentication**: Login and registration with demo mode
- **Dashboard**: Overview of user activity, points, and progress
- **Activity Logging**: Log workouts with different types, durations, and intensities
- **Team Management**: Create, join, and manage fitness teams
- **Leaderboards**: Individual and team rankings with achievements
- **Profile Management**: User profile with fitness goals and statistics

## Demo Credentials

For demonstration purposes, you can login with:
- Username: `demo`
- Password: `demo`

Or create a new account which will work in demo mode.

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

## Technology Stack

- **React** 18+ with Create React App
- **React Router DOM** for navigation
- **Bootstrap 5** for styling
- **Responsive Design** for mobile compatibility

## Components

### Main Components
- `App.js` - Main application with routing
- `Navbar.js` - Navigation bar with authentication state
- `Home.js` - Landing page with app features
- `Dashboard.js` - User dashboard with stats and recent activities
- `Activities.js` - Activity logging and history
- `Teams.js` - Team creation and management
- `Leaderboard.js` - Rankings, challenges, and achievements
- `Profile.js` - User profile management
- `Login.js` - Login form with demo mode
- `Register.js` - Registration form

## File Structure

```
src/
├── components/
│   ├── Activities.js
│   ├── Dashboard.js
│   ├── Home.js
│   ├── Leaderboard.js
│   ├── Login.js
│   ├── Navbar.js
│   ├── Profile.js
│   ├── Register.js
│   └── Teams.js
├── App.js
├── App.css
├── index.js
└── index.css
```

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
