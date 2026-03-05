import argparse
import logging
import sys

from .version_file import VersionFile


logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=logging.INFO,
    )

    #
    parser = argparse.ArgumentParser(
        prog='version',
        description="""Managing version-file in format:
            "__version__ = '<M>.<m>.<p>'\\n".
            With no specified arguments [-p] [-m] [-M] [-r],
            it returns __version__ value to stdout.""",
    )

    parser.add_argument(
        'file', nargs='?', default='_version.py',
        help='Version-file path. "_version.py" by default.')
    parser.add_argument(
        '-p', '--patch', action='store_true',
        help='inc patch')
    parser.add_argument(
        '-m', '--minor', action='store_true',
        help='inc minor')
    parser.add_argument(
        '-M', '--major', action='store_true',
        help='inc major')
    parser.add_argument(
        '-r', '--reset', action='store_true',
        help='reset/create version-file (0.1.0)')
    parser.add_argument(
        '-n', '--newline', choices=['system', 'windows', 'unix'], default='system',
        help=""" Determines what character(s) are used to terminate line in version-file.
            Valid values are 'system' (by default, whatever the OS uses),
            'windows' (CRLF) and 'unix' (LF only)""")

    args = parser.parse_args()

    #
    ver_f = VersionFile(
        args.file,
        {
            'system': None,
            'windows': '\r\n',
            'unix': '\n'
        }[args.newline],
    )

    opt_counter = 0

    if args.patch:
        opt_counter += 1
    if args.minor:
        opt_counter += 1
    if args.major:
        opt_counter += 1
    if args.reset:
        opt_counter += 1

    if opt_counter == 0:
        print(ver_f.version_str)
        sys.exit()
    elif opt_counter != 1:
        logger.error(f'Select strictly one option! Curr version: {ver_f.version_str}')
        sys.exit(1)

    #
    input_version_str = ver_f.version_str

    if args.reset:
        ver_f.reset()
    if args.patch:
        ver_f.inc_patch()
    if args.minor:
        ver_f.inc_minor()
    if args.major:
        ver_f.inc_major()

    logger.info(f'"{ver_f.path}": {input_version_str} -> {ver_f.version_str}')
