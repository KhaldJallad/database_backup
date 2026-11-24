import subprocess
import os
import logging
import time
import sys

main_folder = os.path.dirname(os.path.abspath(__file__))
backup_folder = os.path.join(main_folder, "backup")
log_file = os.path.join(main_folder, "restore.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

start_time = time.perf_counter()

try:
    logging.info("Restore started")

    # Check if backup folder exists
    if not os.path.isdir(backup_folder):
        raise Exception("Backup folder does not exist")

    # Get the latest SQL backup
    with os.scandir(backup_folder) as files:
        latest_file = max(
            (
                file for file in files
                if file.is_file() and file.name.endswith(".sql")
            ),
            key=lambda file: file.stat().st_mtime,
            default=None
        )

    if latest_file is None:
        raise Exception("No backup files found")

    logging.info(f"Selected file: {latest_file.name}")

    file_size = os.path.getsize(latest_file.path)

    if file_size == 0:
        raise Exception("Backup file is empty")

    logging.info(f"File size: {file_size / 1024:.2f} KiB")

    # Restore database
    with open(latest_file.path, "rb") as file:
        result = subprocess.run(
            [
                "mysql",
                "--login-path=restore",
                "backup_project_test"
            ],
            stdin=file,
            stderr=subprocess.PIPE
        )

    if result.returncode == 0:
        logging.info("Restore completed successfully")
        print("Restore completed successfully")
    else:
        raise Exception(
            result.stderr.decode(errors="replace")
        )

except Exception as err:
    logging.error(f"Restore failed: {err}")
    print(f"Error: {err}")
    sys.exit(1)

finally:
    duration = time.perf_counter() - start_time
    logging.info(f"Execution time: {duration:.2f} seconds")
    logging.info("Restore process ended")