# Team Manager

A FastAPI-based web application for managing team surveys and employee data.

## Features
- Employee management
- Weekly surveys
- Performance tracking
- Team status monitoring

## Tech Stack
- Python/FastAPI
- SQLite
- TailwindCSS
- Docker

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run with Docker: `docker-compose up -d`
4. Access at: http://localhost:5000

## Project Structure
```
team_manager/
├── app/
│   ├── templates/    # HTML templates
│   ├── static/       # CSS and static files
│   ├── crud.py      # Database operations
│   └── main.py      # Main application
├── data/            # SQLite database
├── scripts/         # Utility scripts
└── tests/           # Unit tests
```

## Backup
Run `./scripts/backup.sh` to create database backups