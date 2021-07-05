from icl import *

def test_iter():
    l = [(1,5), (3, 9), (-3, 8)]
    s = ItvSet(l)
    l.sort()
    assert list(s) == l

def test_and():
    s1 = ItvSet([(1,5)])
    s2 = ItvSet([(3,7)])
    s3 = s1&s2
    assert list(s3) == [(1,7)]

