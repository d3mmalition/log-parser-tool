import logging
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# ** CONFIGURATION VARIABLES **
LOG_DIR = '/path/to/log_scripts'  # Directory to monitor for new log files
EXTRACT_ERRORS_SCRIPT = '/path/to/extract_errors.py'  # Path to the extract_errors.py script

class LogHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.log'):
            logging.info(f'New log file detected: {event.src_path}')
            # Run the extract_errors.py script
            try:
                log_file = os.path.basename(event.src_path)
                subprocess.run(['python3', EXTRACT_ERRORS_SCRIPT, log_file], check=True, cwd=os.path.dirname(EXTRACT_ERRORS_SCRIPT))
            except subprocess.CalledProcessError as e:
                logging.error(f'Error running extract_errors.py: {e}')

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, LOG_DIR, recursive=False)
    observer.start()
    logging.info(f'Started monitoring {LOG_DIR}')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()

# ** INSTALLATION AND SETUP INSTRUCTIONS **

# 1. Ensure Python 3 and pip are installed on your system.
#
# 2. Install the `watchdog` library using pip:
#    ```bash
#    pip install watchdog
#    ```
#    This library is required for monitoring file system events.

# 3. Update the following variables with your specific paths:
#    - **LOG_DIR**: Set this to the directory where you want to monitor for new log files.
#    - **EXTRACT_ERRORS_SCRIPT**: Set this to the full path of your `extract_errors.py` script.

# 4. Test the script from the command line:
#    ```bash
#    python3 watchdog_parser.py
#    ```
# 5. Add this as a Startup Application:
#    - /usr/bin/python3 /path/to/watchdog_parser.py
