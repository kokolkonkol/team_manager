# Team Manager

A FastAPI-based web application for managing team surveys and employee performance tracking.

## Features
- Employee management
- Weekly performance surveys
- Team status monitoring
- Automated database backups

## Tech Stack
- Python/FastAPI
- SQLite
- TailwindCSS
- Docker

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
│   ├── backup.sh    # Database backup script
│   └── rebuild.sh   # Docker rebuild script
└── tests/           # Unit tests
```

## Setup
1. Clone the repository:
```bash
git clone https://github.com/kokolkonkol/team_manager.git
cd team_manager
```

2. Build and run with Docker:
```bash
docker-compose up -d
```

3. Access the application at: http://localhost:5000

## Database Backup
Run the backup script:
```bash
./scripts/backup.sh
```

## Development
To rebuild the Docker container after changes:
```bash
./scripts/rebuild.sh
```