import os
from tempfile import TemporaryDirectory
import uuid


_dir = TemporaryDirectory(dir=os.getcwd())
_dir_name = _dir.name


# TemporaryFile is not used because we need to reopen files
# NamedTemporaryFile also doesn't guarantee that file may be reopened
def tmp_file():
    return open(os.path.join(_dir_name, uuid.uuid4().hex), 'w+b')
