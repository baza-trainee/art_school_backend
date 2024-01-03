#!/bin/bash


# Path to the backup folder on the host machine
BACKUP_DIR=$HOME/backup-postgres-db

# Check if the backup directory exists
if [ ! -d "$BACKUP_DIR" ]; then
  echo "Backup directory does not exist. Exiting."
  exit 1
fi

# Get the list of backup files
BACKUPS=( $(ls -t $BACKUP_DIR) )

# Check if there are backup files
if [ ${#BACKUPS[@]} -eq 0 ]; then
  echo "No backup files found in the directory. Exiting."
  exit 1
fi

# Display a menu to choose a backup file
echo "Оберіть backup-файл зі списку, для відновлення бази даних. Введіть цифру:"
for i in ${!BACKUPS[@]}; do
  echo "$((i+1)) - ${BACKUPS[$i]}"
done

# Get user's choice
read -p "Ваш вибір: " choice

# Get the selected backup file
LATEST_BACKUP=${BACKUPS[$((choice-1))]}

# database connect url
DATABASE_URI=postgresql://$DB_USER:$DB_PASS@$DB_HOST:$DB_PORT/$DB_NAME

# Clear the database
docker exec -i postgres_db psql $DATABASE_URI -c "DROP SCHEMA public CASCADE;"
docker exec -i postgres_db psql $DATABASE_URI -c "CREATE SCHEMA public;"

# Restore data from the backup
docker exec -i postgres_db psql $DATABASE_URI < $BACKUP_DIR/$LATEST_BACKUP
