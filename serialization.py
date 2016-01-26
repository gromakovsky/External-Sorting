import io
from array import array


_VALUE_SIZE = 4
# all units below and in other files are values, i. e. count=100 means «read 100 values»
_DEFAULT_BATCH_SIZE = 2 ** 22


def _make_array():
    res = array('f')
    assert res.itemsize == _VALUE_SIZE
    return res


def content_length(f: io.BufferedIOBase, preserve_pos=True):
    if preserve_pos:
        pos = f.tell()

    f.seek(0, io.SEEK_END)
    res = f.tell() // _VALUE_SIZE

    if preserve_pos:
        f.seek(pos)

    return res


def go_to_pos(f: io.BufferedIOBase, i: int):
    f.seek(i * _VALUE_SIZE)


def read_content(f: io.BufferedIOBase, count=None, batch_size=_DEFAULT_BATCH_SIZE):
    while True:
        values_to_read = batch_size if count is None else min(count, batch_size)
        b = f.read(values_to_read * _VALUE_SIZE)
        if not b:
            return

        arr = _make_array()
        arr.frombytes(b)
        yield from arr
        if count is not None:
            count -= len(arr)

        if count == 0:
            return


def write_content(f: io.BufferedIOBase, values, batch_size=_DEFAULT_BATCH_SIZE):
    arr = _make_array()
    for x in values:
        arr.append(x)
        if len(arr) >= batch_size:
            arr.tofile(f)
            del arr[:]

    if arr:
        arr.tofile(f)
