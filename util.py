import os
import tempfile


# By default TemporaryFile creates file in /tmp which is relatively small
def tmp_file(**kwargs):
    return tempfile.TemporaryFile(dir=os.getcwd(), **kwargs)
