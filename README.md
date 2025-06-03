# SoftDesk API

A Django REST Framework API for collaborative project management and issue tracking. This application allows users to create projects, manage contributors, track issues, and collaborate through comments.

## 🚀 Features

- **User Management**: Custom user authentication with JWT tokens
- **Project Management**: Create and manage projects with multiple contributors
- **Issue Tracking**: Create, assign, and track issues within projects with status, priority, and type categorization
- **Collaboration**: Add comments to issues for team communication
- **Role-based Access**: Contributor-based permissions for project access control

## 🛠️ Tech Stack

- **Backend**: Django 5.2.1
- **API Framework**: Django REST Framework 3.16.0
- **Authentication**: Django REST Framework SimpleJWT 5.5.0
- **Database**: SQLite (development)
- **Python**: 3.13+
- **Package Management**: Poetry

## 📊 Data Models

### CustomProject
- Project management with name, description, and type
- Associated contributors for access control

### Contributor
- Links users to projects with unique constraints
- Manages project membership and permissions

### Issue
- **Status**: TO_DO, IN_PROGRESS, FINISHED
- **Priority**: LOW, MEDIUM, HIGH
- **Type**: BUG, FEATURE, TASK
- Assigned to contributors with author tracking

### Comment
- Associated with specific issues
- UUID-based identification
- Author and timestamp tracking

## 🔧 Installation & Setup

### Prerequisites
- Python 3.13+
- Poetry package manager

### Installation Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd API-softdesk
```

2. **Install dependencies**
```bash
poetry install
```

3. **Activate virtual environment**
```bash
poetry shell
```

4. **Navigate to Django project**
```bash
cd softdesk
```

5. **Run database migrations**
```bash
python manage.py migrate
```

6. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

7. **Start development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in your request headers:

```
Authorization: Bearer <your-jwt-token>
```

## 📡 API Endpoints

### Authentication
- `POST /auth/login/` - User login
- `POST /auth/register/` - User registration
- `POST /auth/token/refresh/` - Refresh JWT token

### Projects
- `GET /api/projects/` - List all accessible projects
- `POST /api/projects/` - Create new project
- `GET /api/projects/{id}/` - Get project details
- `PUT /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project

### Contributors
- `GET /api/projects/{project_id}/contributors/` - List project contributors
- `POST /api/projects/{project_id}/contributors/` - Add contributor
- `DELETE /api/projects/{project_id}/contributors/{id}/` - Remove contributor

### Issues
- `GET /api/projects/{project_id}/issues/` - List project issues
- `POST /api/projects/{project_id}/issues/` - Create new issue
- `GET /api/projects/{project_id}/issues/{id}/` - Get issue details
- `PUT /api/projects/{project_id}/issues/{id}/` - Update issue
- `DELETE /api/projects/{project_id}/issues/{id}/` - Delete issue

### Comments
- `GET /api/projects/{project_id}/issues/{issue_id}/comments/` - List comments
- `POST /api/projects/{project_id}/issues/{issue_id}/comments/` - Add comment
- `PUT /api/projects/{project_id}/issues/{issue_id}/comments/{id}/` - Update comment
- `DELETE /api/projects/{project_id}/issues/{issue_id}/comments/{id}/` - Delete comment

## 🛡️ Permissions & Security

- **Authentication Required**: Most endpoints require valid JWT tokens
- **Contributor-based Access**: Users must be contributors to access project resources
- **Author Permissions**: Special permissions for resource creators
- **Project-level Security**: Access controlled at the project level through contributor relationships
