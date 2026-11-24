# MySQL Database Backup & Restore Automation

A Python command-line project for creating timestamped MySQL database backups, restoring the latest backup into a separate test database, and recording operational logs. Built as a hands-on database administration (DBA) project to practice backup and recovery, system automation, and error handling.

## Features

- Logical database backups using `mysqldump`.
- Automatic creation of the backup directory and timestamped SQL filenames.
- Backup file size and execution-time logging.
- Detection of failed backup commands and cleanup of incomplete output files.
- Automatic selection of the most recently modified SQL backup.
- Restore into a dedicated test database, with missing-folder and empty-file checks.
- Password-free restore execution using a locally configured MySQL login path.
- Separate backup and restore logs, with a nonzero exit code on failure.
- No third-party Python packages required.

## Technologies

| Technology | Purpose |
| --- | --- |
| Python 3.12+ | Automation and scripting |
| MySQL Community Server | Relational database |
| `mysqldump` and `mysql` | Logical backup and restore |
| `subprocess` | External command execution and stream redirection |
| `os`, `datetime` | File management and timestamped filenames |
| `logging`, `time`, `sys` | Operational logs, timing, and exit codes |

## Project structure

```text
database_backup/
├── backup.py        # Creates SQL backups
├── restore.py       # Restores the latest SQL backup
├── backup/          # SQL backup files
├── backup.log       # Backup execution log
├── restore.log      # Generated when restore.py runs
└── README.md
```

## Getting started

### 1. Prerequisites

- Python 3.12 or newer (the backup script uses modern f-string syntax).
- A running local MySQL server and the MySQL command-line tools.
- `mysql`, `mysqldump`, and `mysql_config_editor` available on your PATH.
- Git, if cloning the repository.

The project was developed for a Windows command-line environment.

```bat
python --version
mysql --version
mysqldump --version
```

### 2. Clone the repository

```bat
git clone https://github.com/KhaldJallad/database_backup.git
cd database_backup
```

### 3. Prepare the databases

Connect to MySQL:

```bat
mysql -u root -p
```

Create the source and test databases if they do not already exist:

```sql
CREATE DATABASE IF NOT EXISTS backup_project;
CREATE DATABASE IF NOT EXISTS backup_project_test;
```

Populate the source database with test tables and sample records before creating a backup. The original practice dataset consists of departments, employees, and attendance records. Exit the MySQL shell before running the Python scripts.

### 4. Create a backup

```bat
python backup.py
```

Enter the MySQL root password when prompted. The script exports the source database into the `backup/` directory.

Example output filename:

```text
backup/backup_2026-11-24_08-30-00.sql
```

Review `backup.log` for the operation status, file size, duration, and errors. The current backup script requires manual password entry.

### 5. Configure restore authentication

Run the following command once from CMD under the same Windows account that will run the restore script:

```bat
mysql_config_editor set --login-path=restore --host=localhost --user=root --password
```

Enter your MySQL password when prompted. This stores connection information locally without placing the password in the Python source code.

### 6. Restore the latest backup

```bat
python restore.py
```

The restore script selects the newest SQL file by modification time, checks that it is not empty, and imports it into `backup_project_test`. Review `restore.log` for the result.

> **Warning:** Restore only trusted SQL dumps into a disposable test database. Restoring may replace existing tables. Check that the dump contains no statements that redirect operations to the original database, such as a conflicting `USE` statement.

## Backup and restore workflow

```text
Source database → mysqldump → Timestamped SQL file
                                    ↓
Test database   ← mysql     ← Latest SQL file
```

The backup script redirects standard output to the SQL file; the restore script reads the SQL file through standard input. Both scripts inspect the subprocess exit code and record operational information.

## Verify the restored data

A successful import alone does not establish data integrity. Connect to the test database and check the schema, record counts, and sample data.

```sql
USE backup_project_test;

SHOW TABLES;

SELECT COUNT(*) FROM departments;
SELECT COUNT(*) FROM employees;
SELECT COUNT(*) FROM attendance;
```

For the original practice dataset, the expected counts are 3 departments, 10 employees, and 20 attendance records. Compare these results with the source data at backup time and verify primary keys, foreign keys, and representative rows. These checks are manual in the current version.

## Security and reliability

- Use only non-sensitive test data in a public repository.
- Do not commit real database dumps, operational logs, or credentials. Keep generated backups and logs out of version control (for example, with `backup/` and `*.log` in `.gitignore`).
- For production use, replace root access with separate least-privilege backup and restore accounts.
- Store backups securely outside the source machine and test recovery regularly.
- This is a learning and portfolio project, not a production-ready disaster recovery solution.

## Future improvements

- Configure a dedicated login path for unattended backups.
- Schedule backups with Windows Task Scheduler.
- Automate restore verification and integrity checks.
- Add backup retention, compression, and off-site storage.
- Use temporary output files and atomic publication to avoid selecting incomplete backups.

## Skills demonstrated

Database administration, MySQL logical backup and recovery, Python scripting, process management, file handling, error handling, logging, and recovery testing.

## Author

[KhaldJallad](https://github.com/KhaldJallad)
