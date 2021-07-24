import random

from icl import *


def test_str():
    kinds = ['()', '(]', '[)', '[]']
    itvs = [Itv(1, 8, kind) for kind in kinds]
    print(itvs)


def test_empty():
    not_empty_itvs = [Itv(1, 1), Itv(-inf, inf)]
    empty_itvs = [Itv(1, 1, '()'), Itv(1, 1, '(]'), Itv(1, 1, '[)'),
                  Itv(1, 0), Itv(inf, 3)
                  ]
    for itv in not_empty_itvs:
        assert not itv.empty()

    for itv in empty_itvs:
        assert itv.empty()


def test_and():
    a, b = Itv(0, 1, '()'), Itv(1, 2, '()')
    res = a & b
    assert res.empty()

    a, b = Itv(0, 1, '()'), Itv(1, 2, '()')
    a.right_open = False
    res = a & b
    assert res.empty()

    a, b = Itv(0, 1, '()'), Itv(1, 2, '()')
    b.right_open = False
    res = a & b
    assert res.empty()

    a, b = Itv(0, 1, '(]'), Itv(1, 2, '[)')
    b.right_open = False
    res = a & b
    print(res)
    assert not res.empty()

    a, b = Itv(0, 2, '(]'), Itv(1, 2, '[)')
    res = a & b
    print(res)
    assert res == Itv(1, 2, '[)')


def test_splits():
    random.seed(2333)
    v = Itv(0, 1000)
    idxs = {random.randint(1, 1000) for _ in range(50)}
    idxs = sorted(idxs)
    print(idxs)
    res = v.splits(idxs)
    print(res)
