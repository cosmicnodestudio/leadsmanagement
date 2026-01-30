# Leads Management System

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.0-green.svg)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3+-4FC08D.svg)](https://vuejs.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-00758F.svg)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg)](https://www.docker.com/)

A comprehensive lead management system that helps businesses track, manage, and convert leads efficiently with:

- **Lead Management** - Complete CRUD operations for lead tracking
- **Interaction History** - Track all interactions with leads
- **Secure Authentication** - JWT-based authentication system
- **Analytics Dashboard** - Overview of leads and conversion metrics

## Technology Stack

### Backend
- **Language:** Python 3.11
- **Framework:** Flask 2.3.0
- **ORM:** SQLAlchemy 2.0.23
- **Authentication:** Flask-JWT-Extended 4.5.2
- **Password Hashing:** Werkzeug (built-in)
- **CORS:** Flask-CORS

### Frontend
- **Framework:** Vue.js 3+
- **Build Tool:** Vite
- **State Management:** Pinia
- **HTTP Client:** Axios 1.4.0
- **Routing:** Vue Router 4.2.0
- **UI:** Tailwind CSS 3.4.1
- **Icons:** Lucide Vue Next

### Database
- **DBMS:** MySQL 8.0+
- **Driver:** PyMySQL 1.0.2
- **Migrations:** SQL Scripts

### DevOps
- **Containers:** Docker + Docker Compose
- **Environment Management:** Python dotenv
- **Server:** Gunicorn (production)

---

## Quick Start

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose
- [Git](https://git-scm.com/)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/cosmicnodestudio/leadsmanagement.git
cd leadsmanagement
```

### 2️⃣ Configure environment variables

```bash
# Review and adjust .env if needed
cat .env
```

Environment variables are already configured with default development values.

### 3️⃣ Start Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4️⃣ Access the application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000
- **MySQL:** localhost:3306

### 5️⃣ Default credentials

- **Email:** test@example.com
- **Password:** password123

---

## Features

### MVP (Phase 1)

- [x] JWT Authentication & Authorization
- [x] User Registration & Login
- [x] Lead CRUD Operations
- [x] Lead Status Management (New, Contacted, Qualified, Converted, Lost)
- [x] Interaction Tracking
- [x] Search & Pagination
- [x] Responsive Dashboard
- [x] Profile Management

### Roadmap (Phase 2)

- [ ] Email notifications
- [ ] Export leads to CSV/Excel
- [ ] Advanced filtering and reporting
- [ ] Lead assignment to team members
- [ ] Integration with external CRMs
- [ ] Automated lead scoring

---

## API Documentation

### Main Endpoints

#### Authentication
```
POST   /api/auth/register           # Register new user
POST   /api/auth/login              # Login user
POST   /api/auth/logout             # Logout user
GET    /api/auth/profile            # Get user profile
POST   /api/auth/refresh            # Refresh access token
POST   /api/auth/change-password    # Change password
```

#### Leads
```
GET    /api/leads                   # List all leads (paginated)
POST   /api/leads                   # Create new lead
GET    /api/leads/<id>              # Get lead details
PUT    /api/leads/<id>              # Update lead
DELETE /api/leads/<id>              # Delete lead
GET    /api/leads/search            # Search leads
```

#### Interactions
```
GET    /api/leads/<id>/interactions     # Get lead interactions
POST   /api/leads/<id>/interactions     # Add interaction
DELETE /api/leads/interactions/<id>     # Delete interaction
```

#### Users
```
GET    /api/users/profile           # Get user profile
PUT    /api/users/profile           # Update profile
```
