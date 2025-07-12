# Skill Swap Platform - Frontend

A modern React frontend for the Skill Swap Platform, built with React 18, React Router, and Axios for API communication.

## Features

- **Authentication System**: Login/Register with JWT token management
- **Dashboard**: Overview of user statistics and available skills
- **Skill Marketplace**: Browse and filter skills by category and difficulty
- **Profile Management**: Update personal information and manage skills
- **Responsive Design**: Mobile-friendly interface with modern UI
- **Real-time Updates**: Dynamic data fetching and state management

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Login.js
│   │   ├── Register.js
│   │   ├── Dashboard.js
│   │   ├── Profile.js
│   │   ├── SkillSwap.js
│   │   └── Navbar.js
│   ├── contexts/
│   │   └── AuthContext.js
│   ├── services/
│   │   └── api.js
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   ├── index.css
│   └── reportWebVitals.js
├── package.json
└── README.md
```

## Installation

1. **Install Node.js** (if not already installed):
   - Download from [nodejs.org](https://nodejs.org/)
   - Or use a package manager like Chocolatey: `choco install nodejs`

2. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

The app will open at `http://localhost:3000`

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm eject` - Ejects from Create React App (not recommended)

## Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

### Backend Connection

The frontend is configured to connect to the Django backend at `http://localhost:8000`. Make sure the backend is running before starting the frontend.

## Key Components

### Authentication
- **Login**: Email/password authentication with error handling
- **Register**: User registration with form validation
- **AuthContext**: Global state management for user authentication

### Dashboard
- **Statistics Cards**: Display user activity metrics
- **Skill Grid**: Show available skills with filtering
- **Quick Actions**: Direct links to main features

### Skill Marketplace
- **Search & Filter**: Find skills by category, difficulty, and keywords
- **Skill Details**: Comprehensive view of individual skills
- **Swap Requests**: Initiate skill swap requests

### Profile Management
- **Personal Info**: Update user profile details
- **Skill Management**: View and manage user's skills
- **Form Validation**: Client-side validation with error handling

## API Integration

The frontend communicates with the Django backend through RESTful APIs:

- **Authentication**: `/api/auth/`
- **Skills**: `/api/skills/`
- **Profiles**: `/api/auth/profile/`
- **Swap Requests**: `/api/swap-requests/`
- **Dashboard**: `/api/dashboard/stats/`

## Styling

The app uses custom CSS with:
- **Modern Design**: Clean, professional interface
- **Responsive Layout**: Works on all device sizes
- **Consistent Theming**: Purple gradient color scheme
- **Interactive Elements**: Hover effects and transitions

## Development

### Adding New Components

1. Create a new component in `src/components/`
2. Import and add to `App.js` routing
3. Add corresponding styles to `App.css`

### API Integration

1. Add new API calls to `src/services/api.js`
2. Create corresponding components
3. Handle loading states and error messages

### State Management

- Use React hooks for local state
- Use AuthContext for global authentication state
- Consider adding Redux for complex state management

## Deployment

### Build for Production

```bash
npm run build
```

### Deploy Options

- **Netlify**: Drag and drop the `build` folder
- **Vercel**: Connect GitHub repository
- **AWS S3**: Upload build files to S3 bucket
- **Heroku**: Use the buildpack for React apps

## Troubleshooting

### Common Issues

1. **Node.js not found**: Install Node.js from the official website
2. **Port conflicts**: Change the port in package.json or use `PORT=3001 npm start`
3. **API connection errors**: Ensure the Django backend is running on port 8000
4. **CORS issues**: Configure CORS settings in the Django backend

### Development Tips

- Use React Developer Tools for debugging
- Check the browser console for API errors
- Use the Network tab to monitor API calls
- Test on different screen sizes for responsiveness

## Contributing

1. Follow the existing code structure
2. Add proper error handling
3. Include loading states for async operations
4. Test on multiple browsers
5. Ensure mobile responsiveness

## License

This project is part of the Skill Swap Platform and follows the same license as the main project. 