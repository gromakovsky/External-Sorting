import heapq
import io
from math import sqrt

from serialization import content_length, go_to_pos, read_content, write_content
from util import tmp_file


# Assuming that `memory_size` values can be sorted in memory when memory_size values are also in memory.
# So approximately 3 * `memory_size` values fit into memory.
# It's also important that buffering stores float using 4 bytes for each one, while sorting operates on python floats,
# which are much fatter, but let's ignore it.
# P. S. It holds for each function

def merge_sort_stupid(fin: io.BufferedIOBase, fout: io.BufferedIOBase, memory_size: int, left=0, count=None):
    fout.seek(0)
    if count is None:
        count = content_length(fin, preserve_pos=False)

    if count <= memory_size:
        go_to_pos(fin, left)
        write_content(fout, sorted(read_content(fin, count=count)), batch_size=memory_size)
        return

    with tmp_file() as left_f, tmp_file() as right_f:
        merge_sort_stupid(fin, left_f, memory_size, left, count=count // 2)
        merge_sort_stupid(fin, right_f, memory_size, left + count // 2, count=count - count // 2)
        left_f.seek(0)
        right_f.seek(0)
        write_content(fout, heapq.merge(read_content(left_f, batch_size=memory_size // 2),
                                        read_content(right_f, batch_size=memory_size // 2)),
                      batch_size=memory_size)


def _to_sorted_blocks(fin: io.BufferedIOBase, memory_size):
    while True:
        sorted_values = sorted(read_content(fin, memory_size))
        if not sorted_values:
            break

        f = tmp_file()
        write_content(f, sorted_values)
        f.seek(0)
        yield f


def _merge_blocks(tmp_files, fout: io.BufferedIOBase, memory_size: int):
    # let's make output buffer slightly larger
    # we can use 3 times `memory_size` for buffers
    buffer_size = 3 * memory_size // (len(tmp_files) + 2)
    generators = [read_content(f, batch_size=buffer_size) for f in tmp_files]
    write_content(fout, heapq.merge(*generators), batch_size=2 * buffer_size)
    for f in tmp_files:
        f.close()


# The same same is true about `memory_size` here
def merge_sort_k_blocks(fin: io.BufferedIOBase, fout: io.BufferedIOBase, memory_size: int):
    _merge_blocks(list(_to_sorted_blocks(fin, memory_size)), fout, memory_size)


def merge_sort_k_blocks_two_passes(fin: io.BufferedIOBase, fout: io.BufferedIOBase, memory_size: int):
    tmp_files = list(_to_sorted_blocks(fin, memory_size))
    if len(tmp_files) < 10:
        larger_tmp_files = tmp_files
    else:
        larger_tmp_files = []
        larger_blocks_count = int(sqrt(len(tmp_files)))
        for i in range(0, len(tmp_files), larger_blocks_count):
            larger_f = tmp_file()
            _merge_blocks(tmp_files[i:min(len(tmp_files), i + larger_blocks_count)], larger_f, memory_size)
            larger_f.seek(0)
            larger_tmp_files.append(larger_f)

        for tmp_f in tmp_files:
            tmp_f.close()

    _merge_blocks(larger_tmp_files, fout, memory_size)
