# Skill Swap Platform

A comprehensive Django-based backend system for a Skill Swap Platform that enables users to exchange skills through structured swap requests and availability-based interactions.

## 🎯 Features

- **User Authentication**: Secure registration and login with JWT token support
- **Skill Management**: Users can add, edit, and categorize their skills
- **Profile System**: Comprehensive user profiles with privacy controls
- **Swap Requests**: Create, manage, and respond to skill exchange requests
- **Search & Discovery**: Find users by skills, availability, and location
- **Notification System**: Keep track of swap requests and updates
- **Dashboard Analytics**: Overview of user statistics and activity

## 👥 Team: TEAM2146

| Name           | Role                     | Email                    |
|----------------|--------------------------|--------------------------|
| Harshil Patel  | Backend Developer        | 23dce081@charusat.edu.in |
| Harnish Patel  | Workflow Logic Developer | 23dce080@charusat.edu.in |
| Jay Prajapati  | Frontend Developer       | 23dce101@charusat.edu.in |
| Vansh Vyas     | UI/UX & Demo Lead        | vyasm5857@gmail.com      |

**Mentor**: Kartik Chavda

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **CORS**: django-cors-headers for frontend integration

### Frontend
- **Framework**: React 18
- **Routing**: React Router
- **HTTP Client**: Axios
- **Styling**: Custom CSS with responsive design

### Additional Tools
- **Image Processing**: Pillow
- **Configuration**: python-decouple
- **Testing**: Django's built-in testing framework

## 📁 Project Structure

```
Skill_Swap_Platform/
├── api/                        # Django app for API endpoints
│   ├── models.py              # Database models (User, Skill, Profile, SwapRequest)
│   ├── views.py               # API view functions
│   ├── serializers.py         # DRF serializers for data validation
│   ├── services.py            # Business logic and workflow services
│   ├── constants.py           # Application constants and enums
│   ├── urls.py                # API URL routing
│   └── migrations/            # Database migration files
├── skill_swap_platform/       # Main Django project
│   ├── settings.py            # Django configuration
│   ├── urls.py                # Main URL routing
│   └── wsgi.py                # WSGI configuration
├── frontend/                  # React frontend application
│   ├── src/                   # React source code
│   ├── public/                # Static assets
│   └── package.json           # Node.js dependencies
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── setup.py                   # Automated setup script
├── test_workflow.py           # Test suite for workflow validation
├── load_sample_data.py        # Sample data loader
└── db.sqlite3                 # SQLite database (development)
```

## 🚀 Installation

### Prerequisites
- Python 3.8+ 
- Node.js 16+ (for frontend)
- pip (Python package manager)
- npm (Node.js package manager)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Skill_Swap_Platform
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load sample data (optional)**
   ```bash
   python load_sample_data.py
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start the React development server**
   ```bash
   npm start
   ```

### Quick Setup (Automated)

Run the automated setup script:
```bash
python setup.py
```

This script will:
- Create virtual environment
- Install dependencies
- Run migrations
- Load sample data
- Create superuser
- Run tests

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Frontend Configuration
Create a `.env` file in the `frontend/` directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

## 🔌 API Endpoints

The API is available at `http://localhost:8000/api/`

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `GET /api/auth/me/` - Get current user info
- `GET /api/auth/profile/` - Get user profile

### Skills
- `GET /api/skills/` - List all skills
- `GET /api/skills/<id>/` - Get skill details
- `GET /api/skills/my-skills/` - Get current user's skills

### Swap Requests
- `POST /api/swaps/create/` - Create swap request
- `GET /api/swaps/` - List user's swaps
- `GET /api/swaps/pending/` - Get pending swaps
- `GET /api/swaps/<id>/` - Get swap details
- `POST /api/swaps/<id>/respond/` - Respond to swap (accept/reject/delete)

### Profile & Search
- `GET /api/profiles/search/` - Search public profiles
- `GET /api/dashboard/stats/` - Get dashboard statistics
- `GET /api/notifications/` - Get user notifications

### Sample API Request
```bash
# Create a swap request
curl -X POST http://localhost:8000/api/swaps/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "receiver_id": 2,
    "skill_offered_id": 1,
    "skill_requested_id": 3,
    "message": "I would like to exchange Python skills for your JavaScript expertise!"
  }'
```

## 📊 Database Models

### Core Models

**User** (Django built-in)
- Standard Django User model with authentication

**Skill**
- `name`: Skill name (unique per user)
- `description`: Detailed description
- `category`: Skill category
- `difficulty_level`: beginner/intermediate/advanced
- `user`: Associated user

**Profile**
- `user`: One-to-one with User
- `bio`, `location`, `phone`: Personal information
- `skills_offered`, `skills_wanted`: Many-to-many with Skills
- `availability`: weekdays/weekends/evenings/etc.
- `is_public`: Profile visibility toggle
- `visibility`: public/private/friends_only

**SwapRequest**
- `sender`, `receiver`: Users involved in swap
- `skill_offered`, `skill_requested`: Skills being exchanged
- `status`: pending/accepted/completed/rejected/deleted
- `message`: Optional message from sender

## 🧪 Testing

### Run Test Suite
```bash
python test_workflow.py
```

### Test Coverage
The test suite covers:
- Skill creation and management
- Profile operations
- Swap request workflow
- Status transitions
- API endpoint functionality
- Business logic validation

### Manual Testing
1. Start the server: `python manage.py runserver`
2. Visit `http://localhost:8000/admin/` for admin interface
3. Use the React frontend at `http://localhost:3000`
4. Test API endpoints with tools like Postman or curl

## 👥 User Guide

### Getting Started
1. **Register**: Create an account through the frontend or API
2. **Setup Profile**: Add your bio, location, and skills
3. **Browse Skills**: Search for skills you want to learn
4. **Create Swaps**: Send requests to exchange skills
5. **Manage Requests**: Accept, reject, or track your swaps

### Profile Management
- **Privacy Settings**: Control who can see your profile
- **Availability**: Set when you're available for swaps
- **Skills**: Add skills you offer and want to learn
- **Contact Info**: Manage your contact details

### Swap Workflow
1. **Discovery**: Find users with skills you want to learn
2. **Request**: Send a swap request with your offering
3. **Negotiation**: Communicate through messages
4. **Agreement**: Accept or reject requests
5. **Completion**: Mark swaps as completed

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests for new functionality**
5. **Run the test suite**
   ```bash
   python test_workflow.py
   ```
6. **Submit a pull request**

### Development Guidelines
- Follow Django best practices
- Write comprehensive tests
- Update documentation for new features
- Use consistent code formatting
- Add meaningful commit messages

### Code Style
- Follow PEP 8 for Python code
- Use descriptive variable and function names
- Add docstrings for functions and classes
- Keep functions focused and modular

## 🚀 Deployment

### Production Setup
1. **Set environment variables**
   ```bash
   export DEBUG=False
   export SECRET_KEY=your-production-secret-key
   export ALLOWED_HOSTS=yourdomain.com
   ```

2. **Configure database** (PostgreSQL recommended)
   ```bash
   export DATABASE_URL=postgresql://user:password@localhost/skillswap
   ```

3. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

4. **Run with production server**
   ```bash
   gunicorn skill_swap_platform.wsgi:application
   ```

### Deployment Options
- **Heroku**: Use the provided Procfile
- **AWS**: Deploy with Elastic Beanstalk or EC2
- **DigitalOcean**: Use App Platform or Droplets
- **Railway**: Simple deployment with GitHub integration

## 📄 License

This project is part of the TEAM2146 hackathon submission and is available for educational and demonstration purposes.

## 🆘 Support

For technical support or questions:
- Check the [Issues](https://github.com/HARRY5D/Skill_Swap_Platform/issues) section
- Contact the development team
- Review the documentation and test files

## 📞 Contact

- **Harshil Patel**: 23dce081@charusat.edu.in
- **Harnish Patel**: 23dce080@charusat.edu.in
- **Jay Prajapati**: 23dce101@charusat.edu.in
- **Vansh Vyas**: vyasm5857@gmail.com

---

**Happy Skill Swapping! 🚀**




