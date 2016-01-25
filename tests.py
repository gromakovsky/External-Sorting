import io
import itertools
import unittest

from serialization import read_content, write_content
from sort import merge_sort_stupid
from util import tmp_file


class TestStupidMergeSort(unittest.TestCase):

    memory_size = 2**15

    def test_empty(self):
        self._test_simple([])

    def test_single(self):
        self._test_simple([-10])

    def test_simple1(self):
        self._test_simple([
            1.6,
            2.5,
            1,
            -1,
        ])

    def test_simple2(self):
        self._test_simple([
            -100.,
            -350.,
            -200.,
        ])

    def test_simple3(self):
        self._test_simple([
            1.6,
            3.5,
            4,
            -5,
            6.6,
            3,
            -9000,
        ] * 2**17)

    def _test_simple(self, values):
        with tmp_file() as input_file, tmp_file() as output_file:
            write_content(input_file, values)
            input_file.seek(0)
            merge_sort_stupid(input_file, output_file, self.memory_size)
            self._check_sorted(input_file, output_file)

    def _check_sorted(self, source: io.BufferedIOBase, res: io.BufferedIOBase):
        source.seek(0)
        source_content = list(itertools.repeat(0, 2**20))
        for v in read_content(source):
            source_content[hash(v) % 2**20] += 1

        res.seek(0)
        res_content = list(itertools.repeat(0, 2**20))
        prev = None
        for cur in read_content(res):
            res_content[hash(cur) % 2**20] += 1
            self.assertTrue(prev is None or prev <= cur)
            prev = cur

        self.assertTrue(source_content == res_content, 'Content differs')


if __name__ == '__main__':
    unittest.main()
