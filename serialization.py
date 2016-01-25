import io
from array import array


_BATCH_SIZE = 2 ** 22
_VALUE_SIZE = 4


def _make_array():
    return array('f')


def content_length(f: io.BufferedIOBase, preserve_pos=True):
    if preserve_pos:
        pos = f.tell()

    f.seek(0, io.SEEK_END)
    res = f.tell() // _VALUE_SIZE

    if preserve_pos:
        f.seek(pos)

    return res


def read_content(f: io.BufferedIOBase, count=None):
    while True:
        size = _BATCH_SIZE if count is None else min(count * _VALUE_SIZE, _BATCH_SIZE)
        b = f.read(size)
        if not b:
            return

        arr = _make_array()
        arr.frombytes(b)
        yield from arr
        if count is not None:
            count -= len(arr)

        if count == 0:
            return


def write_content(f: io.BufferedIOBase, values):
    arr = _make_array()
    for x in values:
        arr.append(x)
        if len(arr) >= _BATCH_SIZE / _VALUE_SIZE:
            arr.tofile(f)

    if arr:
        arr.tofile(f)
