import logging

import PyInstaller.__main__

from _version import __version__


#
logging.basicConfig(
    format='%(levelname)s: %(message)s',
    level=logging.INFO,
)

proj = 'appver'
PyInstaller.__main__.run([
    f'{proj}/__main__.py',
    '-n', proj,
    '--distpath', f'dist/{proj}_{__version__}',
    '--workpath', 'build',
    '--optimize', '1',
    '--clean',
    '--onefile',
    '--console',
])
