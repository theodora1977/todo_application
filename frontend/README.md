# Frontend Quick Start

## Overview
This is a modern, responsive Todo application frontend built with vanilla HTML, CSS, and JavaScript. It connects to your FastAPI backend and provides a beautiful user interface for managing tasks.

## Features
- **User Authentication**: Sign up and login with email/password
- **Task Management**: Create, read, update, and delete tasks
- **Task Filtering**: Filter tasks by status (All, Pending, Completed)
- **Task Tracking**: View task completion statistics
- **Responsive Design**: Works beautifully on desktop, tablet, and mobile devices
- **Modern UI**: Gradient backgrounds, smooth animations, and intuitive design

## Quick Start

### Option 1: Run Locally with Python
```bash
# Navigate to the frontend directory
cd frontend

# Start a simple Python HTTP server
python -m http.server 8080
```

Then open your browser to `http://localhost:8080`

### Option 2: Run with Node.js (if available)
```bash
# Install http-server globally
npm install -g http-server

# Navigate to frontend directory
cd frontend

# Start the server
http-server -p 8080
```

### Option 3: Open in Browser Directly
Simply open `index.html` in your browser (limited functionality without a local server for API calls).

## Configuration

### Update API URL
In `app.js`, find the API_BASE_URL variable and update it to match your backend server:

**Local Development:**
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

**Production (Render):**
```javascript
const API_BASE_URL = 'https://your-render-app.onrender.com';
```

## Backend Setup Requirements

Your FastAPI backend must have CORS (Cross-Origin Resource Sharing) enabled. Add this to your `app/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

# Add after app = FastAPI() line
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## API Endpoints Used

The frontend connects to these endpoints:

### Authentication
- `POST /users/` - User registration
- `POST /users/login` - User login (expects response with `access_token` and `user` object)

### Tasks
- `GET /tasks/` - Get all tasks
- `POST /tasks/` - Create a new task
- `PUT /tasks/{id}` - Update task (mark as completed)
- `DELETE /tasks/{id}` - Delete task

## Expected API Response Format

### User Login Response
```json
{
    "access_token": "your_jwt_token",
    "user": {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com"
    }
}
```

### Task Response
```json
{
    "id": 1,
    "title": "My Task",
    "description": "Task description",
    "owner_id": 1,
    "date": "2025-12-10",
    "time": "14:30",
    "completed": false
}
```

## File Structure
```
frontend/
├── index.html       # Main HTML structure
├── styles.css       # All styling (responsive, modern design)
├── app.js          # JavaScript logic and API integration
└── README.md       # This file
```

## Browser Compatibility
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### 401 Unauthorized
- Check that your API token is being sent correctly
- Verify the login endpoint returns a valid `access_token`
- Check token format in Authorization header

### CORS Errors
- Ensure CORS middleware is added to your FastAPI app
- Check that allowed origins include your frontend URL
- Verify API_BASE_URL in app.js is correct

### Tasks Not Loading
- Ensure you're logged in first
- Check that the `/tasks/` endpoint returns tasks array
- Open browser DevTools (F12) → Network tab to see API responses

### Port Already in Use
```bash
# On Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# On Mac/Linux
lsof -i :8080
kill -9 <PID>
```

## Deployment

### Deploy Frontend to Render
1. Create a `render.yaml` in your repo root:
```yaml
services:
  - type: static_site
    name: todo-frontend
    buildCommand: "echo 'Frontend ready'"
    staticPublicPath: ./frontend
    envVars:
      - key: API_BASE_URL
        value: "https://your-backend.onrender.com"
```

2. Or use Vercel (recommended for static sites):
   - Import your GitHub repo to Vercel
   - Set root directory to `frontend`
   - Deploy

### Update API URL for Production
Before deploying, update `app.js`:
```javascript
const API_BASE_URL = 'https://your-backend.onrender.com';
```

## Development Tips
- Use browser DevTools (F12) to debug API calls
- Check the Network tab to see request/response details
- Use Console tab to see error messages
- Mobile device testing: Use your machine's IP address instead of localhost

## License
MIT
