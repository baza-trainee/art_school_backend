# !/bin/bash


# Name of the database container
DB_CONTAINER=postgres_db

# Path to the backup folder on the host machine
BACKUP_DIR=./backup-postgres-db

# Database
DATABASE_URI=postgresql://admin:admin@postgres:5432/school_db

# Backup max count
MAX_BACKUPS=3

# Check if the backup folder exists and create it if it doesn't
if [ ! -d "$BACKUP_DIR" ]; then
  mkdir -p $BACKUP_DIR
fi

# Get the current time in the format YYYYMMDD_HHMMSS
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Path to the backup file inside the folder
BACKUP_PATH=$BACKUP_DIR/backup_$TIMESTAMP.sql

# Create a backup of the database inside the container
docker exec $DB_CONTAINER pg_dump $DATABASE_URI > $BACKUP_PATH

# Delete the oldest backup file if there are more than three
if [ $(ls $BACKUP_DIR | wc -l) -gt $MAX_BACKUPS ]; then
  rm -rf $BACKUP_DIR/$(ls -t $BACKUP_DIR | tail -1)
fi
