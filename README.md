# Skill Swap Platform - Backend Implementation

A comprehensive Django-based backend for a Skill Swap Platform that enables users to exchange skills through structured swap requests and availability-based interactions.

## 🎯 Project Overview

This platform allows users to:
- **List their skills** (both offered and wanted)
- **Search for other users** by skills and availability
- **Create swap requests** with proper validation
- **Manage swap lifecycle** (pending → accepted/rejected/deleted)
- **Control profile visibility** and availability settings

## 👥 Team: CodeSync
| Name           | Role                     | Email                    |
|----------------|--------------------------|--------------------------|
| Harshil Patel  | Backend Developer        | 23dce081@charusat.edu.in |
| Harnish Patel  | Workflow Logic Developer | 23dce080@charusat.edu.in |
| Jay Prajapati  | Frontend Developer       | 23dce101@charusat.edu.in |
| Vansh Vyas     | UI/UX & Demo Lead        | vyasm5857@gmail.com      |

## 🧑‍🏫 Mentor
**Kartik Chavda**

## 🏗️ Architecture

### Core Components
- **Models**: User, Skill, Profile, SwapRequest
- **Services**: Business logic and workflow management
- **API Views**: RESTful endpoints with validation
- **Constants**: Centralized enums and error messages

### Key Features Implemented

#### ✅ Swap Request Lifecycle (State Machine)
```
[pending] → [accepted]
         ↘ [rejected]
         ↘ [deleted]
```

#### ✅ Profile Privacy & Availability Logic
- Users can only browse **public** profiles
- Users can only **accept swaps** if they're available
- Swap search respects profile visibility

#### ✅ Validation & Constraints
- Prevent sending swaps to oneself
- Only **one pending request** allowed between two users
- Cannot accept/reject swaps not addressed to you
- Only sender can delete their own pending swap

#### ✅ Error Handling & Fallbacks
- Descriptive errors for invalid operations
- Proper HTTP status codes
- Standardized API responses

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
```bash
cd ODOO2/Skill_Swap_Platform
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Run the development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## 📚 API Documentation

### Authentication
All endpoints require authentication. Use Django's session authentication or implement token-based auth.

### Core Endpoints

#### 🔄 Swap Management

**Create Swap Request**
```
POST /api/swaps/create/
Content-Type: application/json

{
    "receiver_id": 2,
    "skill_offered_id": 1,
    "skill_requested_id": 3,
    "message": "I'd love to learn Python in exchange for teaching you JavaScript!"
}
```

**Respond to Swap**
```
POST /api/swaps/{swap_id}/respond/
Content-Type: application/json

{
    "action": "accept"  // or "reject" or "delete"
}
```

**List User's Swaps**
```
GET /api/swaps/?status=pending&type=sent
```

**Get Pending Swaps**
```
GET /api/swaps/pending/
```

**Get Swap Details**
```
GET /api/swaps/{swap_id}/
```

#### 👤 Profile Management

**Search Public Profiles**
```
GET /api/profiles/search/?skill=Python&availability=weekends&location=New York
```

#### 🛠️ Skills Management

**List All Skills**
```
GET /api/skills/
```

**Search Skills**
```
GET /api/skills/?search=python&category=programming
```

#### 🔔 Notifications (Bonus Feature)

**Get User Notifications**
```
GET /api/notifications/
```

### Response Format

All API responses follow this standardized format:

```json
{
    "status": "success|error|warning",
    "message": "Human-readable message",
    "data": {
        // Response data
    },
    "errors": [
        // List of error messages (if any)
    ]
}
```

## 🗄️ Database Schema

### Models Overview

#### User (Django Auth)
- Standard Django User model
- Extended with Profile relationship

#### Skill
```python
- name: CharField (unique)
- description: TextField
- category: CharField
- created_at, updated_at: DateTimeField
```

#### Profile
```python
- user: OneToOneField(User)
- bio, location, phone: CharField
- skills_offered, skills_wanted: ManyToManyField(Skill)
- availability: CharField (weekdays, weekends, evenings, etc.)
- is_public, visibility: Boolean/CharField
- created_at, updated_at: DateTimeField
```

#### SwapRequest
```python
- sender, receiver: ForeignKey(User)
- skill_offered, skill_requested: ForeignKey(Skill)
- status: CharField (pending, accepted, rejected, deleted)
- message: TextField
- created_at, updated_at: DateTimeField
```

## 🔧 Business Logic Implementation

### Swap Validation Service
- Validates swap creation requests
- Ensures business rules are followed
- Prevents duplicate pending requests

### Swap Workflow Service
- Manages state transitions
- Handles atomic operations
- Implements proper authorization

### Profile Service
- Manages profile visibility
- Handles skill-based searches
- Filters by availability

## 🛡️ Security & Validation

### Input Validation
- All inputs are validated using Django serializers
- Custom validation for business rules
- Proper error messages for each validation failure

### Authorization
- Users can only modify their own swaps
- Profile visibility is enforced
- Proper permission checks for all operations

### Data Integrity
- Database constraints prevent invalid states
- Atomic transactions ensure consistency
- Proper foreign key relationships

## 🚀 Performance Optimizations

### Database Queries
- `select_related()` for foreign key relationships
- `prefetch_related()` for many-to-many relationships
- Proper indexing on frequently queried fields

### Caching Strategy
- Query optimization for profile searches
- Efficient filtering by skills and availability

## 🧪 Testing Strategy

### Unit Tests
- Service layer business logic
- Model validation and constraints
- API endpoint functionality

### Integration Tests
- Complete swap workflow
- Profile search functionality
- Error handling scenarios

## 📊 Monitoring & Logging

### Error Tracking
- Comprehensive error handling
- Detailed error messages
- Proper HTTP status codes

### Performance Monitoring
- Query optimization
- Response time tracking
- Database performance metrics

## 🔄 Deployment

### Production Setup
1. Set `DEBUG = False`
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure CORS settings
5. Set up proper logging

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com
```

## 📈 Future Enhancements

### Planned Features
- Real-time notifications using WebSockets
- Advanced skill matching algorithms
- Rating and review system
- Mobile app API endpoints
- Advanced search filters

### Scalability Considerations
- Database sharding for large datasets
- Caching layer for frequently accessed data
- API rate limiting
- Microservices architecture

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is part of the CodeSync hackathon submission.

## 🆘 Support

For technical support or questions, please contact the development team.

---

**Built with ❤️ by CodeSync Team**


