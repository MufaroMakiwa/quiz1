#!/usr/bin/env python3
import os
import quiz
import pickle
import unittest


TEST_DIRECTORY = os.path.dirname(__file__)

##################################################
#  Problem 1
##################################################


class TestProblem1(unittest.TestCase):

    def test_01(self):
        nrows, ncols = 3, 2
        heaters = [(0, 0), (1, 1)]
        expect = {(2, 0), (2, 1)}
        got = quiz.coolest(nrows, ncols, heaters)
        self.assertEqual(got, expect)

    def test_02(self):
        nrows, ncols = 3, 2
        heaters = [(1, 0)]
        expect = {(r, c) for r in range(nrows) for c in range(ncols)}
        got = quiz.coolest(nrows, ncols, heaters)
        self.assertEqual(got, expect)

    def test_03(self):
        nrows, ncols = 5, 2
        heaters = [(0, 0), (4, 0)]
        expect = {(2, 0), (2, 1)}
        got = quiz.coolest(nrows, ncols, heaters)
        self.assertEqual(got, expect)

    def test_04(self):
        nrows, ncols = 3, 2
        heaters = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
        expect = {(0, 1), (2, 0), (0, 0), (2, 1)}
        got = quiz.coolest(nrows, ncols, heaters)
        self.assertEqual(got, expect)

    def test_05(self):
        nrows, ncols = 3, 2
        heaters = [(0, 0), (0, 1), (2, 0), (2, 1)]
        expect = {(0, 1), (2, 0), (0, 0), (2, 1)}
        got = quiz.coolest(nrows, ncols, heaters)
        self.assertEqual(got, expect)

    def test_06(self):
        nrows, ncols = 200, 300
        heaters = [(r, c) for r in range(nrows) for c in range(ncols)][:-1]
        expect = {(nrows-1, ncols-1)}
        got = quiz.coolest(nrows, ncols, heaters)
        self.assertEqual(got, expect)

    def test_07(self):
        nrows, ncols = 17, 19
        heaters = [(r, c) for r in range(nrows) for c in range(ncols) if (r<8 or r>9) and (c<5 or c>7)]
        expect = {(16, 6), (2, 6), (4, 6), (6, 6), (5, 6), (7, 6), (10, 6), (12, 6), (14, 6),
                  (13, 6), (0, 6), (15, 6), (1, 6), (3, 6), (8, 6), (9, 6), (11, 6)}
        got = quiz.coolest(nrows, ncols, heaters)
        self.assertEqual(got, expect)


##################################################
#  Problem 2
##################################################

class TestProblem2(unittest.TestCase):
    def _run_test(self, test_name):
        with open(os.path.join(TEST_DIRECTORY, 'test_data', 'problem2', f'{test_name}.pickle'), 'rb') as f:
            trees, ns, results = pickle.load(f)
        for tree, n, res in zip(trees, ns, results):
            self.assertEqual(quiz.complete_nary(tree, n), res)

    def test_00(self):
        t = [1, [2], [3], [4]]
        self.assertTrue(quiz.complete_nary(t, 3))
        self.assertFalse(quiz.complete_nary(t, 2))
        self.assertTrue(quiz.complete_nary(t, 3))

        t = [13, [7], [8, [99], [16, [77]], [42]]]
        self.assertFalse(quiz.complete_nary(t, 0))
        self.assertFalse(quiz.complete_nary(t, 2))
        self.assertFalse(quiz.complete_nary(t, 2))

        t = [13, [7], [8, [99], [16, [77], [78], [79], [80]], [42], [43]], [9], [19]]
        self.assertTrue(quiz.complete_nary(t, 4))

        t = [13]
        for i in range(10):
            self.assertTrue(quiz.complete_nary(t, i))

    def test_01(self):
        self._run_test('small')

    def test_02(self):
        self._run_test('med')

    def test_03(self):
        self._run_test('large')



##################################################
#  Problem 3
##################################################

class TestProblem3(unittest.TestCase):
    def check_chain(self, capacities, target, expected_len, x):
        if expected_len is None:
            return x is None
        elif x is None:
            self.assertEqual(x, expected_len, f'Expected a sequence of length {expected_len} but got None.')
        if len(x) != expected_len:
            return False
        if not (x[0] == tuple(0 for c in capacities) and target in x[-1] and len(x[-1]) == len(capacities)):
            return False
        if not all(len(elt) == len(capacities) and all(0<=elt[ix]<=capacities[ix] for ix in range(len(elt))) for elt in x):
            return False
        for c1, c2 in zip(x, x[1:]):
            diffs = {ix: (c2[ix], c1[ix]) for ix in range(len(c2)) if c2[ix] != c1[ix]}
            if len(diffs) == 1:
                ix = list(diffs.keys())[0]
                if diffs[ix][0] not in {0, capacities[ix]}:
                    return False
            elif len(diffs) == 2:
                ixs = list(diffs.keys())
                d1 = diffs[ixs[0]][0] - diffs[ixs[0]][1]
                d2 = diffs[ixs[1]][0] - diffs[ixs[1]][1]
                if abs(d1) != abs(d2):
                    return False
                if (d1 < 0 and d2 < 0) or (d1 > 0 and d2 > 0):
                    return False
            else:
                return False
        return True

    def _run_named_test(self, test_name):
        with open(os.path.join(TEST_DIRECTORY, 'test_data', 'problem3', f'{test_name}.pickle'), 'rb') as f:
            results = pickle.load(f)
            print(results)
        for cups, results in results:
            for n in range(len(results)):
                self._run_test(cups, n, results[n])

    def _run_test(self, capacities, target, expected_len):
        result = quiz.cups_puzzle(capacities, target)
        self.assertTrue(self.check_chain(capacities, target, expected_len, result))

    def test_00(self):
        self._run_test([1, 2, 3], 0, 1)
        self._run_test([3, 7], 2, 7)

    def test_01(self):
        self._run_named_test('small')

    def test_02(self):
        self._run_named_test('med')

    def test_03(self):
        self._run_named_test('large')


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
