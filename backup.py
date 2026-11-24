import subprocess
from datetime import datetime
import os
import logging
import time
import sys

folder_path = os.path.dirname(os.path.abspath(__file__))

logFile = os.path.join(folder_path, 'backup.log')
logging.basicConfig(
         filename=logFile,
         level=logging.INFO,
         format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("backup start")

backup_folder = os.path.join(folder_path, "backup")

logging.info("create folder")   

backup_file_path = os.path.join(backup_folder, f"backup_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.sql")

startTime = time.perf_counter()

try:

    os.makedirs(backup_folder, exist_ok=True)
    logging.info("Backup folder is ready")

    logging.info("start backup")
    # # run mysqldump for backup
    with open(backup_file_path, "wb") as file:
        result = subprocess.run(
            ["mysqldump", '-u', 'root', '-p', 'backup_project'],
            stdout=file,
            stderr=subprocess.PIPE
        )

    if result.returncode == 0:
        logging.info('backup created successfuly')
        file_size = os.path.getsize(backup_file_path) / 1024
        logging.info(f"File size: {file_size:.2f} KB")
        endTime = time.perf_counter()
        duration =  endTime - startTime 
        logging.info(f"Execution time: {duration:.2f} seconds")
        print("backup has been saved successfuly")
        logging.info(f"backup end")
    else:
       raise Exception(f"Backup failed:{result.stderr.decode(errors='replace')}")
    
 
except Exception as err:
    print(f'error:{err}')
    logging.error(f"error:{err}")
    if os.path.exists(backup_file_path):
        os.remove(backup_file_path)
        logging.warning('file has been removed')
    sys.exit(1)

