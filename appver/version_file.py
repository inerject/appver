import logging
from pathlib import Path
import re


logger = logging.getLogger(__name__)


#
FILE_PATTERN = r'^__version__ = (["\'])([^"\']*)\1$'

NEWLINE_VARIANTS = ['\n', '\r\n']
QUOTES_VARIANTS = ['"', "'"]
DEFAULT_QUOTES = "'"


class VersionFile:
    def __init__(self, path, newline=None, quotes=None):
        try:
            self.path = Path(path).resolve(strict=True)
        except Exception:
            raise RuntimeError(f'Cannot resolve path "{path}"!')

        self.newline = newline
        self.quotes = DEFAULT_QUOTES if (quotes is None) else quotes
        self.major, self.minor, self.patch = 0, 1, 0

        if self.path.is_file():
            if self.path.suffix != '.py':
                raise RuntimeError(f'".py" file expected!')

            self._load(quotes)

        elif self.path.is_dir():
            self.path /= '_version.py'
            if self.path.is_file():
                self._load(quotes)
            else:
                self._dump()
                logger.info(f'Version file created: "{self.path}"')

        else:
            raise RuntimeError(f'Unexpected path type!')

        #
        assert (self.newline is None) or (self.newline in NEWLINE_VARIANTS)
        assert self.quotes in QUOTES_VARIANTS
        for ver_part in [self.major, self.minor, self.patch]:
            assert isinstance(ver_part, int)

    @property
    def version_str(self) -> str:
        return f'{self.major}.{self.minor}.{self.patch}'

    def reset(self):
        self.major, self.minor, self.patch = 0, 1, 0
        self._dump()

    def inc_patch(self):
        self.patch += 1
        self._dump()

    def inc_minor(self):
        self.minor += 1
        self.patch = 0
        self._dump()

    def inc_major(self):
        self.major += 1
        self.minor = 0
        self.patch = 0
        self._dump()

    def _load(self, quotes):
        with open(self.path) as f:
            text = f.read()
            if self.newline is None:
                self.newline = f.newlines

        match = re.search(FILE_PATTERN, text, re.MULTILINE)
        if match:
            if quotes is None:
                self.quotes = match.group(1)

            v = match.group(2).split('.')
            self.major, self.minor, self.patch = int(v[0]), int(v[1]), int(v[2])

        else:
            raise RuntimeError()

    def _dump(self):
        q = self.quotes
        with open(self.path, 'w', newline=self.newline) as f:
            f.write(f'__version__ = {q}{self.version_str}{q}\n')
