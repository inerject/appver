import sys
import argparse
import logging

from .appver import AppVer

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
logging.basicConfig(
    format='%(levelname)s: %(message)s',
    level=logging.INFO,
)

newline_variants = {
    'system': None,
    'windows': '\r\n',
    'unix': '\n'
}
ver = AppVer(args.file, newline_variants[args.newline])

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
    print(ver)
    sys.exit()
elif opt_counter != 1:
    logging.error(f'Select strictly one option! Curr version: {ver}')
    sys.exit(1)

#
input_ver_repr = str(ver)

if args.reset:
    ver.reset()
if args.patch:
    ver.inc_patch()
if args.minor:
    ver.inc_minor()
if args.major:
    ver.inc_major()

logging.info(f'{ver.path}: {input_ver_repr} -> {ver}')
