import os
from datetime import datetime

class Logger:
    """
    A class to handle detailed logging for each Droidscribe agent run.
    It creates a single, comprehensive log file for each run.
    """
    def __init__(self):
        """
        Initializes the logger and creates the run-specific log file.
        """
        run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        self.log_file_path = os.path.join(log_dir, f"run_{run_id}.log")
        print(f"📝 Logging this run to: {self.log_file_path}")

    def log(self, message):
        """
        Logs a message to the console and the single log file.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        with open(self.log_file_path, 'a') as f:
            f.write(log_message + "\n")

    def log_section(self, title, content):
        """
        Saves a formatted block of content to the single log file.
        """
        log_content = f"""
--------------------------------------------------
--- {title.upper()}
--------------------------------------------------
{content}
--------------------------------------------------
"""
        with open(self.log_file_path, 'a') as f:
            f.write(log_content + "\n")
        self.log(f"📄 Saved section: {title}")


