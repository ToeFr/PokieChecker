import argparse
import logging

logger = logging.getLogger(__name__)
hash_types = ['MD5', 'SHA1', 'SHA224', 'SHA256', 'SHA384', 'SHA512', 'SHA3_224', 'SHA3_256', 'SHA3_384', 'SHA3_512']

def create_parser():
    logger.info("Creating CLI parser.")
    

    parser = argparse.ArgumentParser(
        prog="Pokie",
        description="Pokie: A File Integrity Monitoring System",
        epilog="Credit: Pokie is developed by ToeFr (all platforms)",
        usage="%(prog)s [-m] MODE [-f / -d] FILE/DIR [options]"
    )

    parser.add_argument("--version", action="version", version="%(prog)s - 0.1b")
    parser.add_argument("-d", "--directories", help="The directories to monitor", nargs='+', required=False, type=str)
    parser.add_argument("-f", "--files", help="The files to monitor", required=False, nargs='+', type=str)
    parser.add_argument("-if", "--ignore_files", help="The file names to ignore", required=False, nargs='+', type=str, default=[])
    parser.add_argument("-id", "--ignore_directories", help="The directory names to ignore", required=False, nargs='+', type=str, default=[])
    parser.add_argument("-ht", "--hash_type", help=f"The hash type to use choices=[{', '.join(hash_types)}]", required=False, type=str)
    parser.add_argument("-m", "--mode", help="The mode of operation (Alert, Create, Update, Check)", required=True, type=str, choices=['Alert', 'Create', 'Update', 'Check'])
    parser.add_argument("-t", "--timer", help="The time interval to check for changes", required=False, type=int, default=500)
    parser.add_argument("-hf", "--hash_file", help="The data file that stores the hashes", required=False, type=str, default="data.json")

    logger.info("CLI parser created successfully.")
    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    print(args)
