from icl import *

def make_itvs(pairs):
    return [Itv(pair[0], pair[1]) for pair in pairs]

def test_iter():
    l1 = [(1,5), (3, 9), (-3, 8)]
    l2 = [(-3, 9)]
    s = ItvSet(make_itvs(l1))
    assert list(s) == make_itvs(l2)

def test_and():
    # (1, 5) & (3, 7) = (3, 5)
    s1 = ItvSet(make_itvs([(1,5)]))
    s2 = ItvSet(make_itvs([(3,7)]))
    s3 = s1&s2
    assert list(s3) == make_itvs([(3,5)])


def test_or():
    # (1, 5) | (3, 7) = (1, 7)
    s1 = ItvSet(make_itvs([(1,5)]))
    s2 = ItvSet(make_itvs([(3,7)]))
    s3 = s1&s2
    assert list(s3) == make_itvs([(1,7)])

