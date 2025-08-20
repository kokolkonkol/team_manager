#!/bin/bash

# Set variables
BACKUP_DIR="/home/pawel/team_manager/backups"
DB_FILE="/home/pawel/team_manager/data/survey.db"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="survey_db_backup_${DATE}.db"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Copy database file with timestamp
cp "$DB_FILE" "$BACKUP_DIR/$BACKUP_FILE"

# Keep only last 5 backups
cd "$BACKUP_DIR" && ls -t | tail -n +6 | xargs -r rm --

# Print success message
echo "Backup created: $BACKUP_FILE"