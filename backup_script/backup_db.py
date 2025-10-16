import os
import subprocess
from datetime import datetime

def backup_db():
    host = os.environ.get("POSTGRES_HOST", "postgres-db")
    dbname = os.environ.get("POSTGRES_DB", "app_db")
    user = os.environ.get("POSTGRES_USER", "admin")
    password = os.environ.get("POSTGRES_PASSWORD", "admin")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"/var/backups/backup_{timestamp}.sql"

    # Use PGPASSWORD environment for non-interactive password passing
    env = os.environ.copy()
    env["PGPASSWORD"] = password

    cmd = [
        "pg_dump",
        "-h", host,
        "-U", user,
        "-d", dbname,
        "-F", "c",       # custom (compressed) format
        "-f", backup_file
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, env=env, check=True)
    print("Backup written to", backup_file)

if __name__ == "__main__":
    backup_db()

