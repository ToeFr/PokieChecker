Sure, here's the entire content for the `README.md` file wrapped in a code block for easy copying:

```markdown
# File Monitor CLI

## Introduction

File Monitor CLI is a command-line tool designed to monitor files and directories for changes. It uses hashing to detect modifications and provides alerts for any changes. This tool is useful for maintaining the integrity of important files and ensuring that unauthorized changes are detected promptly.

## Features

- **Monitor Directories and Files**: Specify directories or files to monitor.
- **Hashing Algorithms**: Choose from various hashing algorithms for file integrity checks.
- **Alert System**: Alerts users about any file modifications.
- **Update and Check Modes**: Update the hash database and check for file changes.
- **Logging**: Comprehensive logging for all operations.

## Installation

### Prerequisites

- Python 3.x
- pip

### Install Required Packages

```bash
pip install -r requirements.txt
```

## Usage

### Command-Line Arguments

- `-d`, `--directories`: List of directories to monitor.
- `-f`, `--files`: List of files to monitor.
- `-i`, `--ignore-files`: List of files to ignore.
- `-I`, `--ignore-directories`: List of directories to ignore.
- `-H`, `--hash-type`: Hashing algorithm to use (`md5`, `sha1`, `sha256`, etc.).
- `-m`, `--mode`: Mode of operation (`create`, `check`, `update`, `alert`).
- `-t`, `--timer`: Timer interval for the alert mode (in seconds).
- `-o`, `--hash-file`: File to store hash values.

### Examples

#### Create a Hash Database

```bash
python file_monitor.py -d /path/to/directory -H sha256 -m create -o data.json
```

#### Check for File Changes

```bash
python file_monitor.py -m check -o data.json
```

#### Update the Hash Database

```bash
python file_monitor.py -d /path/to/directory -H sha256 -m update -o data.json
```

#### Alert on File Changes

```bash
python file_monitor.py -m alert -o data.json -t 60
```

## Code Snippets

### Initializing the Logger

```python
def initialize_logger():
    try:
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Logger initialized successfully.")
        return logger
    except Exception as e:
        logging.critical(f"Error initializing logger: {e}")
        exit(1)
```

### Directory Scraping

```python
def dir_scrape(directory, ignore_files=None, ignore_directories=None):
    ignore_files = ignore_files or []
    ignore_directories = ignore_directories or []
    logger.info(f"Scraping directory: {directory}")
    files = []

    try:
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.1f}%"),
            transient=True,
            console=console,
        ) as progress:
            task = progress.add_task("Scanning directory for files", total=None)

            for root, dirs, filenames in os.walk(directory):
                dirs[:] = [d for d in dirs if d not in ignore_directories]
                logger.debug(f"Scanning directories: {dirs}")

                for file in filenames:
                    if file not in ignore_files:
                        files.append(os.path.join(root, file))

                progress.advance(task)

        return files
    except Exception as e:
        logger.error(f"Error scraping directory '{directory}': {e}")
        raise
```

### Calculating Hashes

```python
def calculate_hashes(files, hash_type):
    filehasher = FileHasher(hash_type)
    files_to_hash = {}

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.1f}%"),
        transient=True,
        console=console,
    ) as progress:
        task = progress.add_task("Hashing files", total=len(files))

        for file in files:
            try:
                file_hash = filehasher.hash_file(file)
                files_to_hash[file] = file_hash
            except Exception as e:
                logger.error(f"Error hashing file {file}: {e}")
                print_centered(f"Error hashing file {file}: {e}", "red", bold=True)

            progress.advance(task)

    return files_to_hash
```

## Logging

The tool uses a comprehensive logging system to keep track of all operations. Logs are written to a file and also displayed in the console.

### Example Log Messages

- **Info**: `logger.info("Monitoring directory: /path/to/directory")`
- **Warning**: `logger.warning("File /path/to/file has been modified.")`
- **Error**: `logger.error("Error hashing file /path/to/file: [error details]")`
- **Critical**: `logger.critical("Error initializing logger: [error details]")`

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or feedback, please contact [your-email@example.com](mailto:your-email@example.com).

---

*Happy Monitoring!*
```

### Explanation:

1. **Introduction**: Brief description of what the tool does.
2. **Features**: Key features of the tool.
3. **Installation**: Prerequisites and installation steps.
4. **Usage**: Detailed usage instructions with command-line arguments and examples.
5. **Code Snippets**: Example code snippets for key functions.
6. **Logging**: Information about the logging system.
7. **Contributing**: Guidelines for contributing to the project.
8. **License**: License information.
9. **Contact**: Contact information for inquiries or feedback.

This format should make it easy to copy the entire content and paste it into your `README.md` file without any issues.
