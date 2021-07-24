import functools

import more_itertools

from icl import *
import random


def make_itvs(pairs):
    return [Itv(pair[0], pair[1]) for pair in pairs]


def test_iter():
    l1 = [(1, 5), (3, 9), (-3, 8)]
    l2 = [(-3, 9)]
    s = ItvSet(make_itvs(l1))
    assert list(s) == make_itvs(l2)

    l1 = [(1, 5), (5, 11), (21, 33), (33, 55), (inf, -inf)]
    l2 = [(1, 11), (21, 55)]
    random.shuffle(l1)
    s = ItvSet(make_itvs(l1))
    assert list(s) == make_itvs(l2)


def test_height():
    def generate_sets(n=10, seed=2333):
        random.seed(seed)
        idxs = sorted({random.randint(1, 1 << 30) for _ in range(n)})
        itvs = Itv(0, 1 << 30).splits(idxs, True)
        random.shuffle(itvs)
        itv_sets = [ItvSet([v]) for v in itvs]
        return itv_sets

    s1 = ItvSet.union(*generate_sets(1 << 15))
    print(len(s1))
    print(s1._root.height())


def test_or_merge():
    def generate_sets(n=10):
        random.seed(2333)
        idxs = sorted({random.randint(1, 10000) for _ in range(n)})
        itvs = Itv(0, 10000).splits(idxs)
        itvs = [v.create_like() for v in itvs]

        random.shuffle(itvs)
        itv_sets = [ItvSet([v]) for v in itvs]
        return itv_sets

    def merge_test_impl(ss, i, j):
        size = j - i
        if size < 1:
            return ItvSet()
        if size == 1:
            return ss[i]

        mid = i + size // 2
        s1 = merge_test_impl(ss, i, mid)
        s2 = merge_test_impl(ss, mid, j)
        res = s1 | s2
        return res

    def merge_test(ss):
        return merge_test_impl(ss, 0, len(ss))

    itv_sets = generate_sets(1000)
    s = merge_test(itv_sets)
    assert s == ItvSet([Itv(0, 10000)])


def test_and():
    # (1, 5) & (3, 7) = (3, 5)
    s1 = ItvSet(make_itvs([(1, 5)]))
    s2 = ItvSet(make_itvs([(3, 7)]))
    s3 = s1 & s2
    assert list(s3) == make_itvs([(3, 5)])


def test_and_1():
    def generate_sets(n=10, seed=2333):
        random.seed(seed)
        idxs = sorted({random.randint(1, 10000) for _ in range(n)})
        itvs = Itv(0, 10000).splits(idxs, True)
        itvs = [v for v in itvs]
        random.shuffle(itvs)
        itv_sets = [ItvSet([v]) for v in itvs]
        return itv_sets

    s1 = ItvSet.union(*generate_sets(100, seed=2333))
    s2 = ItvSet.union(*generate_sets(100, seed=2334))
    s3 = s1 & s2
    print(s1)
    print(s2)
    print(s3)
    print(len(s1), len(s2), len(s3))


def test_sub():
    s1 = ItvSet(make_itvs([(1, 5)]))
    s2 = ItvSet(make_itvs([(3, 7)]))
    s3 = s1 - s2
    assert s3 == ItvSet([Itv(1, 3, '[)')])
    s3 = s2 - s1
    assert s3 == ItvSet([Itv(5, 7, '(]')])

    s1 = ItvSet(make_itvs([(1, 7)]))
    s2 = ItvSet(make_itvs([(3, 5)]))
    s3 = s1 - s2
    assert s3 == ItvSet([Itv(1, 3, '[)'), Itv(5, 7, '(]')])