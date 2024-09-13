# Automated PostgreSQL Backup System with Python and `pg_basebackup`

This project automates PostgreSQL backups using Python and `pg_basebackup`. The script is designed to perform automatic backups, compress and encrypt the backups, manage backup retention, and send email 
notifications upon successful or failed backups.

## Key Features:
1. **Automate daily/weekly backups** using `pg_basebackup`.
2. **Compress and encrypt backups** for security.
3. **Backup retention**: Automatically delete older backups to save space.
4. **Email notifications**: Get notified upon successful or failed backups.

## Prerequisites:
- PostgreSQL installed and running.
- Python 3 installed.
- `pg_basebackup` utility (comes with PostgreSQL).
- Python libraries: `subprocess`, `os`, `shutil`, `smtplib`, `email.mime`, `gnupg`.

## Steps:
1. **Start PostgreSQL**: Restart PostgreSQL service before starting the backup.
2. **Automate Backups**: Use `pg_basebackup` for full database backups.
3. **Compress Backups**: Use `shutil` to compress the backups.
4. **Encrypt Backups**: Use `gnupg` for encrypting backups.
5. **Backup Retention**: Keep the last `N` backups and delete older ones.
6. **Send Notifications**: Send email notifications for backup status (success/failure).

## Configuration:
- Update PostgreSQL details in the Python script (host, port, user, database name).
- Configure email details for notifications.
- Adjust backup retention settings as per your requirements.

## Scheduling Backups:
To schedule the backup script, use `cron`:
```bash
crontab -e
