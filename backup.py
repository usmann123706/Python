
---

### backups.py

```python
import subprocess
import os
from datetime import datetime
import shutil
import gnupg
import time
import smtplib
from email.mime.text import MIMEText

# Backup configurations
BACKUP_DIR = '/var/lib/pgsql/basebackup/'  # Directory where backups will be stored
PG_USER = 'postgres'
PG_PASSWORD = 'your_pg_password'
PG_HOST = 'localhost'
PG_PORT = '5428'
DB_NAME = 'your_database'
BACKUP_NAME = f"{DB_NAME}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
BACKUP_PATH = os.path.join(BACKUP_DIR, BACKUP_NAME)

# Restart PostgreSQL
def restart_postgres():
    try:
        cmd = ['/usr/pgsql-16/bin/pg_ctl', '-D', '/var/lib/pgsql/16/', 'restart']
        subprocess.run(cmd, check=True)
        print("Postgres restarted successfully")
    except subprocess.CalledProcessError as e:
        print(f"Postgres failed to restart: {e}")

# Create a backup using pg_basebackup
def create_backup():
    try:
        os.makedirs(BACKUP_PATH, exist_ok=True)
        cmd = [
            'pg_basebackup', 
            '-D', BACKUP_PATH,  
            '-Ft',  
            '-z',   # Compress the backup
            '-h', PG_HOST,
            '-U', PG_USER,
            '-p', PG_PORT,
            '-v',  
            '-P'   
        ]
        subprocess.run(cmd, check=True)
        print(f"Backup created successfully at {BACKUP_PATH}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")
        return False

# Compress the backup
def compress_backup(backup_path):
    zip_path = f"{backup_path}.tar.gz"
    shutil.make_archive(backup_path, 'gztar', backup_path)
    print(f"Backup compressed: {zip_path}")
    return zip_path

# Encrypt the backup
def encrypt_backup(backup_path):
    gpg = gnupg.GPG()
    with open(backup_path, 'rb') as f:
        encrypted_data = gpg.encrypt_file(f, recipients=None, symmetric=True, passphrase='usman')
        with open(f"{backup_path}.gpg", 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data.data)
    print(f"Backup encrypted: {backup_path}.gpg")
    return f"{backup_path}.gpg"

# Manage backup retention
def manage_backup_retention(backup_dir, retention_days=7):
    current_time = time.time()
    for backup_file in os.listdir(backup_dir):
        backup_path = os.path.join(backup_dir, backup_file)
        if os.stat(backup_path).st_mtime < current_time - (retention_days * 86400):
            if os.path.isdir(backup_path):
                shutil.rmtree(backup_path)
            else:
                os.remove(backup_path)
            print(f"Deleted old backup: {backup_path}")

# Send email notifications
def send_email_notification(success, log_msg):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your_email@gmail.com"
    receiver_email = "recipient_email@gmail.com"
    password = "your_email_password"

    subject = "Backup Success" if success else "Backup Failed"
    message = MIMEText(log_msg)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Email notification sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main script
if __name__ == "__main__":
    restart_postgres()
    success = create_backup()
    if success:
        compressed_backup = compress_backup(BACKUP_PATH)
        encrypted_backup = encrypt_backup(compressed_backup)
        manage_backup_retention(BACKUP_DIR)
        send_email_notification(True, f"Backup successful: {encrypted_backup}")
    else:
        send_email_notification(False, "Backup failed!")
