# Log Scripts

This directory contains scripts for extracting and analyzing errors from log files. These scripts help automate the process of identifying and summarizing errors from various types of logs, including upgrade logs and catalina logs.

## Directory Structure

```
log_scripts/
├── extract_errors.py
├── watchdog_parser.py
├── output/
│   └── [parsed log files]
```

- **extract_errors.py**: Script to extract essential error information from a log file.
- **watchdog_parser.py**: Script to monitor the log directory and automatically run `extract_errors.py` when a new log file is added.
- **output/**: Directory where the output files are saved.

## Installation

### Prerequisites

- Python 3.x
- Watchdog library for Python

### Installing Watchdog

You can install Watchdog using pip:

```bash
pip install watchdog
```

### Setting Up Automatic Script Execution on Linux

#### Using systemd

1. **Create a Service File**:
   Create a new service file for `watchdog_parser.py`:

   ```bash sh
   sudo nano /etc/systemd/system/watchdog_parser.service
   ```

   Add the following content to the file:

   ```ini
   [Unit]
   Description=Watchdog Parser Service
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /path/to/watchdog_parser.py
   WorkingDirectory=/path/to
   Restart=always
   User=your_username
   Group=your_groupname

   [Install]
   WantedBy=multi-user.target
   ```

2. **Reload systemd and Enable the Service**:

   ```sh
   sudo systemctl daemon-reload
   sudo systemctl enable watchdog_parser.service
   sudo systemctl start watchdog_parser.service
   ```

3. **Check the Service Status**:

   ```sh
   sudo systemctl status watchdog_parser.service
   ```

## Usage

### Extract Errors from a Log File

To manually extract errors from a log file, run the `extract_errors.py` script with the log file name as an argument:

```sh
python3 extract_errors.py <log_file_name>
```

Example:

```sh
python3 extract_errors.py catalina.out
```

The script will save the output in the `output` directory.

### Monitor Log Directory

To automatically extract errors whenever a new log file is added to the `log_scripts` directory, run the `watchdog_parser.py` script:

```sh
python3 watchdog_parser.py
```

This script will monitor the directory and trigger the `extract_errors.py` script for any new log files.

## Configuration

### extract_errors.py

- **log_dir**: Directory where log files are located.
- **output_dir**: Directory where output files should be saved.

### watchdog_parser.py

- **path**: Path to the directory to be monitored.

## Example Workflow

1. Place a new log file (e.g., `catalina.log`) in the `log_scripts` directory.
2. `watchdog_parser.py` detects the new log file and runs `extract_errors.py`.
3. `extract_errors.py` processes the log file and saves the output in the `output` directory.

## Common Issues

### Permission Denied

If you encounter a "Permission denied" error, ensure you have the appropriate permissions to read the log files and write to the output directory.

### Log File Not Found

Ensure the log file exists in the specified directory and the path is correct.
```
