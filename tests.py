import time
import io
import itertools
import random
import unittest

from serialization import read_content, write_content
from sort import merge_sort_stupid, merge_sort_k_blocks
from util import tmp_file


class TestSort(unittest.TestCase):

    _memory_size = 2**16

    def setUp(self):
        self._start = time.time()

    def tearDown(self):
        print('{}: {:.2f} seconds'.format(self.__class__.__name__, time.time() - self._start))

    def _predefined_values(self):
        yield []
        yield [-10]
        yield [
            1.6,
            2.5,
            1,
            -1,
        ]
        yield [
            -100.,
            -350.,
            -200.,
        ]
        yield itertools.chain.from_iterable(itertools.repeat([
            1.6,
            3.5,
            99,
            4,
            -5,
            6.6,
            3,
            -9000,
        ], 2**19))

    def _random_values(self, n=2**20):
        for i in range(n):
            yield random.random()

    def _launch_predefined_tests(self, sort_f):
        for values in self._predefined_values():
            self._test_simple(values, merge_sort_stupid)

    def _test_simple(self, values, sort_f):
        with tmp_file() as input_file, tmp_file() as output_file:
            write_content(input_file, values)
            input_file.seek(0)
            sort_f(input_file, output_file, self._memory_size)
            self._check_sorted(input_file, output_file)

    def _check_sorted(self, source: io.BufferedIOBase, res: io.BufferedIOBase):
        hashes_size = 2**20

        def h(value):
            return hash(value) % hashes_size

        source.seek(0)
        source_content = list(itertools.repeat(0, hashes_size))
        for v in read_content(source):
            source_content[h(v)] += 1

        res.seek(0)
        res_content = list(itertools.repeat(0, hashes_size))
        prev = None
        for cur in read_content(res):
            res_content[h(cur)] += 1
            self.assertTrue(prev is None or prev <= cur)
            prev = cur

        self.assertTrue(source_content == res_content, 'Content differs')


class TestStupidSort(TestSort):

    def test_predefined(self):
        self._launch_predefined_tests(merge_sort_stupid)

    def test_random(self):
        self._test_simple(self._random_values(), merge_sort_stupid)


class TestBlocksSort(TestSort):

    def test_predefined(self):
        self._launch_predefined_tests(merge_sort_k_blocks)

    def test_random(self):
        self._test_simple(self._random_values(), merge_sort_k_blocks)


if __name__ == '__main__':
    unittest.main()
