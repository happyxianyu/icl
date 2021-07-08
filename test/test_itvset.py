from icl import *

def make_itvs(pairs):
    return[Itv(pairs[0], pairs[1]) for pair in pairs]

def test_iter():
    l = [(1,5), (3, 9), (-3, 8)]
    s = ItvSet(make_itvs(l))
    l.sort()
    assert list(s) == make_itvs(l)

def test_and():
    s1 = ItvSet(make_itvs([(1,5)]))
    s2 = ItvSet(make_itvs([(3,7)]))
    s3 = s1&s2
    assert list(s3) == make_itvs([(1,7)])

