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


def test_and():
    # (1, 5) & (3, 7) = (3, 5)
    s1 = ItvSet(make_itvs([(1, 5)]))
    s2 = ItvSet(make_itvs([(3, 7)]))
    s3 = s1 & s2
    assert list(s3) == make_itvs([(3, 5)])


def test_or():
    # (1, 5) | (3, 7) = (1, 7)
    s1 = ItvSet(make_itvs([(1, 5)]))
    s2 = ItvSet(make_itvs([(3, 7)]))
    s3 = s1 | s2
    assert list(s3) == make_itvs([(1, 7)])


def test_or_1():
    random.seed(2333)
    idxs = sorted({random.randint(1, 10000) for _ in range(10)})
    itvs = Itv(0, 10000).splits(idxs)
    itvs = [v.create_like() for v in itvs]

    print(itvs)
    random.shuffle(itvs)
    itv_sets = [ItvSet([v]) for v in itvs]

    def merge1(ss, i, j):
        size = j - i
        if size < 1:
            return ItvSet()
        if size == 1:
            return ss[i]

        mid = i + size // 2
        s1 = merge1(ss, i, mid)
        s2 = merge1(ss, mid, j)
        res = s1 | s2
        return res

    def merge(ss):
        return merge1(ss, 0, len(ss))

    s = merge(itv_sets)
    assert s == ItvSet([Itv(0, 10000)])
