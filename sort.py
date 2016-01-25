import heapq
import io

from serialization import content_length, read_content, write_content
from util import tmp_file


# assuming that `memory_size` values fit into memory
def merge_sort_stupid(fin: io.BufferedIOBase, fout: io.BufferedIOBase, memory_size: int, left=0, count=None):
    fout.seek(0)
    if count is None:
        count = content_length(fin, preserve_pos=False)

    if count <= memory_size:
        fin.seek(left)
        write_content(fout, sorted(read_content(fin, count)))
        return

    with tmp_file() as left_f, tmp_file() as right_f:
        merge_sort_stupid(fin, left_f, memory_size, left, count=count // 2)
        merge_sort_stupid(fin, right_f, memory_size, left + count // 2, count=count - count // 2)
        left_f.seek(0)
        right_f.seek(0)
        write_content(fout, heapq.merge(read_content(left_f), read_content(right_f)))


def merge_sort_k_blocks(fin: io.BufferedIOBase, fout: io.BufferedIOBase):
    pass
