from pathlib import Path
import re


class AppVer:
    def __init__(self, path, newline=None):
        path = Path(path)
        if path.is_dir():
            self.path = path.resolve() / '_version.py'
        elif path.is_file():
            self.path = path.resolve()
        else:
            path = path.resolve()
            path.parent.resolve(strict=True)
            self.path = path

        self.newline = newline

    def __repr__(self):
        return self.get()

    def get(self) -> str:
        try:
            with open(self.path) as f:
                version_file_text = f.read()

            ver_pattern = r'^__version__ = ["\']([^"\']*)["\']'
            match = re.search(ver_pattern, version_file_text, re.MULTILINE)
            if match:
                self.repr = match.group(1)
            else:
                raise RuntimeError()

            v = self.repr.split('.')
            self.major, self.minor, self.patch = int(v[0]), int(v[1]), int(v[2])

        except Exception:
            self.repr = 'undefined'
            self.major, self.minor, self.patch = None, None, None

        return self.repr

    def set(self, major, minor, patch):
        with open(self.path, 'w', newline=self.newline) as f:
            f.write(f"__version__ = '{major}.{minor}.{patch}'\n")

    def reset(self):
        self.set(0, 1, 0)

    def inc_patch(self):
        self._check()
        self.patch += 1
        self.set(self.major, self.minor, self.patch)

    def inc_minor(self):
        self._check()
        self.minor += 1
        self.patch = 0
        self.set(self.major, self.minor, self.patch)

    def inc_major(self):
        self._check()
        self.major += 1
        self.minor = 0
        self.patch = 0
        self.set(self.major, self.minor, self.patch)

    def _check(self):
        if self.get() == 'undefined':
            raise ValueError('Version-file is undefined!')
