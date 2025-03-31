import logging
import os
from datetime import datetime

# Generate a unique log file name based on the current timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create a directory to store log files
logs_path = os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path,mode=0o700,exist_ok=True)

# Define the full path for the log file
LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

# Configure logging settings
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

#if __name__=="__main__":
#    logging.info("Logging has Started")