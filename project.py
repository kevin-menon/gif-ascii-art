import argparse
import logging
from pathlib import Path
import sys

import dotenv

from ascii import print_ascii_for_files, print_ascii_for_folder, print_ascii_for_giphy

dotenv.load_dotenv()

logger = logging.getLogger()


def main(args: argparse.Namespace):
    """
    This main functions just forwards the CLI arguments to the appropriate function according to the command
    """
    if args.debug:
        logger.setLevel(logging.DEBUG)
    logging.debug("CLI arguments : " + str(args))
    if args.command == 'FILE':
        print_ascii_for_files(args.FILE, message = args.message, monochrome= args.monochrome)
    elif args.command == 'FOLDER':
        print_ascii_for_folder(directory = args.FOLDER, message = args.message, monochrome= args.monochrome, recurse = args.r)
    elif args.command == "WEB":
        print_ascii_for_giphy(giphy_id = args.id, message = args.message, monochrome = args.monochrome)
    else:
        sys.stderr.write(f"Unsupported operation : {args.command}\n")
        sys.exit(1)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This program will display a GIF image to your tutorial and exit with a message.")
    parser.add_argument('--message', help ="Message to print after each GIF", default = "The End")
    parser.add_argument('--monochrome', action='store_true', default = False, help = "Colorized or not")
    parser.add_argument('--debug', action='store_true', default = False, help = "Will set logging level to debug. Beware it may conflict with the ASCII animation")

    subparsers = parser.add_subparsers(dest='command')

    file_subparser = subparsers.add_parser("FILE", help= "Provide GIF file(s) to render in ASCII")
    file_subparser.add_argument('FILE', nargs = "+", help ="A GIF file", type=argparse.FileType('rb'))

    giphy_subparser = subparsers.add_parser("WEB", help = "Will fetch a meme from the GIPHY API")
    giphy_subparser.add_argument('--id', help='A GIPHY image ID if you wish a specific meme', default=None)

    folder_subparser = subparsers.add_parser("FOLDER", help= "Will animate GIF files in a folder")
    folder_subparser.add_argument('FOLDER', type=Path, default = Path('.'))
    folder_subparser.add_argument('-r', action='store_true', help ="recurse subfolders", default = False)

    args = parser.parse_args()
    main(args)
