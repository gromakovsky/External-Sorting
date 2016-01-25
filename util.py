import os
import tempfile


# by default it creates file in /tmp which is relatively small
def tmp_file(**kwargs):
    return tempfile.TemporaryFile(dir=os.getcwd(), **kwargs)
