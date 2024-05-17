import logging
import os
import json
import time
from rich.console import Console
from rich.progress import track
from rich.align import Align
from src.logger._loginit_ import setup_logging
from src.cli_parser import create_parser
from src.file_hasher import FileHasher
""
# Initialize rich console
console = Console()

def print_centered(text, style="white"):
    console.print(Align.center(f"[{style}]{text}[/{style}]"))

def initialize_logger():
    try:
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Logger initialized successfully.")
        return logger
    except Exception as e:
        logging.critical(f"Error initializing logger: {e}")
        exit(1)

def initialize_parser():
    try:
        parser = create_parser()
        args = parser.parse_args()
        logger.info("CLI parser initialized successfully.")
        return args
    except Exception as e:
        logger.critical(f"Error initializing CLI parser: {e}")
        exit(1)

def dir_scrape(directory, ignore_files=None, ignore_directories=None):
    ignore_files = ignore_files or []
    ignore_directories = ignore_directories or []
    logger.info(f"Scraping directory: {directory}")
    files = []

    try:
        for root, dirs, filenames in track(os.walk(directory), description="Scanning directory for files"):
            dirs[:] = [d for d in dirs if d not in ignore_directories]
            logger.debug(f"Scanning directories: {dirs}")

            for file in filenames:
                if file not in ignore_files:
                    files.append(os.path.join(root, file))

        return files
    except Exception as e:
        logger.error(f"Error scraping directory '{directory}': {e}")
        raise

def validate_directories(directories):
    valid_directories = []

    for directory in directories:
        if not os.path.isdir(directory):
            logger.error(f"Directory {directory} does not exist.")
            print_centered(f"Directory {directory} does not exist.", "red")
        else:
            logger.info(f"Monitoring directory: {directory}")
            print_centered(f"Monitoring directory: {directory}", "green")
            valid_directories.append(directory)

    return valid_directories

def validate_files(files):
    valid_files = []

    for file in files:
        if not os.path.isfile(file):
            logger.error(f"File {file} does not exist.")
            print_centered(f"File {file} does not exist.", "red")
        else:
            logger.info(f"Monitoring file: {file}")
            print_centered(f"Monitoring file: {file}", "green")
            valid_files.append(file)

    return valid_files

def calculate_hashes(files, hash_type):
    filehasher = FileHasher(hash_type)
    files_to_hash = {}

    for file in track(files, description="Hashing files"):
        try:
            file_hash = filehasher.hash_file(file)
            files_to_hash[file] = file_hash
        except Exception as e:
            logger.error(f"Error hashing file {file}: {e}")
            print_centered(f"Error hashing file {file}: {e}", "red")

    return files_to_hash

def find_files(args):
    logger.info("Starting file search...")

    if args.directories and args.files:
        e = "Both directories and files detected. Please specify only one."
        logger.error(e)
        raise ValueError(e)

    if not args.directories and not args.files:
        e = "No directories or files detected. Please specify at least one."
        logger.error(e)
        raise ValueError(e)
    
    if not args.hash_type:
        e = "No hash type specified."
        logger.error(e)
        print_centered(e, "red")
        exit(1)

    files_to_monitor = []

    if args.directories:
        valid_directories = validate_directories(args.directories)
        for directory in valid_directories:
            directory_files = dir_scrape(directory, ignore_files=args.ignore_files, ignore_directories=args.ignore_directories)
            if directory_files:
                files_to_monitor.extend(directory_files)
            else:
                logger.warning(f"Scraping directory '{directory}' - Potentially empty.")
                print_centered(f"Warning: Scraping directory '{directory}' - Potentially empty.", "yellow")

    if args.files:
        valid_files = validate_files(args.files)
        files_to_monitor.extend(valid_files)

    if not files_to_monitor:
        error_msg = "No files to monitor."
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info("Files to monitor: %s", files_to_monitor)

    files_to_hash = calculate_hashes(files_to_monitor, args.hash_type)
    
    data = {args.hash_type: files_to_hash}

    return data

def check():
    try:
        with open("data.json", "r") as f:
            data = json.load(f)

        hash_type = list(data.keys())[0]
        hashes = list(data.values())[0]

        for file, hash in hashes.items():
            filehasher = FileHasher(hash_type)
            try:
                new_hash = filehasher.hash_file(file)
                if new_hash == hash:
                    continue
                else:
                    print_centered(f"File {file} has been modified.", "yellow")
                    logger.warning(f"File {file} has been modified.")
            except Exception as e:
                print_centered(f"Error hashing file {file}: {e}", "red")
                logger.error(f"Error hashing file {file}: {e}")
    except FileNotFoundError:
        logger.error("data.json file not found.")
        print_centered("data.json file not found.", "red")
    except Exception as e:
        logger.error(f"Error during check: {e}")
        raise Exception(f"Error during check: {e}")

def update():
    try:
        logger.info("Updating data file.")
        with open(args.hash_file, "r") as f:
            data = json.load(f)

        hash_type = list(data.keys())[0]
        existing_hashes = data[hash_type]

        files_to_monitor = []

        if args.directories:
            valid_directories = validate_directories(args.directories)
            for directory in valid_directories:
                directory_files = dir_scrape(directory, ignore_files=args.ignore_files, ignore_directories=args.ignore_directories)
                files_to_monitor.extend(directory_files)

        if args.files:
            valid_files = validate_files(args.files)
            files_to_monitor.extend(valid_files)

        if not files_to_monitor:
            error_msg = "No new files to monitor."
            logger.error(error_msg)
            raise ValueError(error_msg)

        new_hashes = calculate_hashes(files_to_monitor, hash_type)
        
        existing_hashes.update(new_hashes)
        data[hash_type] = existing_hashes

        with open("data.json", "w") as f:
            json.dump(data, f, indent=3)

        logger.info("Data file updated successfully.")
    except FileNotFoundError:
        logger.error("data.json file not found.")
        print_centered("data.json file not found.", "red")
    except Exception as e:
        logger.error(f"Error updating data file: {e}")
        raise

def alert():
    while True:
        try:
            with open("data.json", "r") as f:
                data = json.load(f)

            hash_type = list(data.keys())[0]
            existing_hashes = data[hash_type]

            for file, old_hash in existing_hashes.items():
                filehasher = FileHasher(hash_type)
                try:
                    new_hash = filehasher.hash_file(file)
                    if new_hash != old_hash:
                        logger.warning(f"File {file} has been modified.")
                        print_centered(f"Alert: File {file} has been modified.", "yellow")
                        existing_hashes[file] = new_hash
                        with open("alerts.txt", "a") as f:
                            f.write(f"File {file} has been modified.\n")
                except Exception as e:
                    logger.error(f"Error hashing file {file}: {e}")
                    print_centered(f"Error hashing file {file}: {e}", "red")

            data[hash_type] = existing_hashes
            with open("data.json", "w") as f:
                json.dump(data, f, indent=3)

            logger.info("Alert check completed successfully.")
        except FileNotFoundError:
            logger.error("data.json file not found.")
            print_centered("data.json file not found.", "red")
            exit(1)
        except Exception as e:
            logger.error(f"Error in alert function: {e}")
            print_centered(f"Error in alert function: {e}", "red")
            exit(1)

        time.sleep(args.timer)

def main():
    try:
        if args.mode.lower() == "create":
            logger.info("Creating data file.")
            data = find_files(args)
            
            logger.info("Writing data to specified file.")
            with open(args.hash_file, "w") as f:
                json.dump(data, f, indent=3)

        elif args.mode.lower() == "check":
            logger.info("Checking files.")
            check()

        elif args.mode.lower() == "update":
            logger.info("Updating data file.")
            update()

        elif args.mode.lower() == "alert":
            logger.info("Alerting for file changes.")
            alert()
    except Exception as e:
        logger.critical(f"Application error: {e}")
        raise

if __name__ == "__main__":
    print_centered("==== File Monitor CLI ====", "cyan")
    logger = initialize_logger()
    args = initialize_parser()
    main()
    logger.info("Application exited successfully.")
    print_centered("Application exited successfully.", "green")
    exit(0)
