"""
使用treep实现itvset
"""

import functools
import random
from typing import Tuple, Union
from .itv import *

__all__ = [
    'ItvSet'
]


class Node:
    def __init__(self, itv: Itv):
        self.itv = itv
        self.priority = random.random()
        self.lch: 'Node' = None
        self.rch: 'Node' = None
        self.prnt: 'Node' = None

    @property
    def k(self):
        return self.itv.a

    @property
    def a(self):
        return self.itv.a

    @property
    def b(self):
        return self.itv.b

    def set_rch(self, rch: 'Node'):
        self.rch = rch
        if rch is not None:
            rch.prnt = self

    def set_lch(self, lch: 'Node'):
        self.lch = lch
        if lch is not None:
            lch.prnt = self

    def find(self, x):
        """
        x是一个点，返回落入的区间的节点
        """
        if x in self.itv:
            return self
        if x <= self.k:
            ch = self.lch
        else:
            ch = self.rch
        if ch is not None:
            return ch.find(x)

    def find_neareast(self, x):
        return _find_nearest(self, x)

    def find_by_lower(self, x):
        """
        x表示下界，是一个点
        如果落入了某个区间，则返回这个区间
        否则返回以x为下界的最接近x的区间
        """
        return _find_by_lower(self, x)

    def find_by_upper(self, x):
        return _find_by_upper(self, x)

    def abc_order_iter(self):
        """
        左中右DFS
        """
        yield from _abc_order_iter(self)

    def cba_order_iter(self):
        """
        右中左DFS
        """
        yield from _cba_order_iter(self)

    def min(self):
        lch = self.lch
        if lch is None:
            return self
        else:
            return lch.min()

    def max(self):
        rch = self.rch
        if rch is None:
            return self
        else:
            return rch.max()

    def next_low(self):
        lch = self.lch
        if lch is not None:
            return lch.max()

        prnt = self.prnt
        n = self
        while prnt is not None:
            if prnt.rch is n:
                return prnt
            else:
                n = prnt
                prnt = n.prnt

    def next_high(self):
        rch = self.rch
        if rch is not None:
            return rch.min()

        prnt = self.prnt
        n = self
        while prnt is not None:
            if prnt.lch is n:
                return prnt
            else:
                n = prnt
                prnt = n.prnt


def _abc_order_iter(n):
    if n is None:
        return
    yield from _abc_order_iter(n.lch)
    yield n
    yield from _abc_order_iter(n.rch)


def _cba_order_iter(n):
    if n is None:
        return
    yield from _cba_order_iter(n.rch)
    yield n
    yield from _cba_order_iter(n.lch)


def _iter_from_nearest(self, x, it_next=_abc_order_iter):
    if self is None:
        return

    if x in self.itv:
        yield self
    if x <= self.k:
        yield from _iter_from_nearest(self.lch, x)
        yield self
        yield from it_next(self.rch)
    else:
        yield from _iter_from_nearest(self.rch, x)
        yield self
        yield from it_next(self.lch)


def _find_nearest(self, x):
    if self is None:
        return

    if x in self.itv:
        return self
    if x <= self.k:
        n = _find_nearest(self.lch, x)
    else:
        n = _find_nearest(self.rch, x)
    if n is None:
        return self
    return n


def _find_by_lower(self, x):
    if self is None:
        return

    if x in self.itv:
        return self
    if x <= self.k:
        n = _find_by_lower(self.lch, x)
        if n is None:
            return self
        return n
    else:
        return _find_by_lower(self.rch, x)


def _find_by_upper(self, x):
    if self is None:
        return

    if x in self.itv:
        return self
    if x <= self.k:
        return _find_by_upper(self.lch, x)
    else:
        n = _find_by_upper(self.rch, x)
        if n is None:
            return self
        return n


def _split(n: Node, x, t1=None, t2=None) -> Union[Tuple[None, None], Tuple[Node, Node]]:
    if n is None:
        return None, None

    if n.itv.a <= x:
        t1 = n
        rch, t2 = _split(n.rch, x, n.rch, t2)
        n.set_rch(rch)
    else:
        t2 = n
        t1, lch = _split(n.lch, x, n.lch, t1)
        n.set_lch(lch)
    return t1, t2


def _merge(t1: Node, t2: Node) -> Node:
    if t1 is None:
        return t2
    if t2 is None:
        return t1

    if t1.priority > t2.priority:
        t1.set_rch(_merge(t1.rch, t2))
        return t1
    else:
        t2.set_lch(_merge(t1, t2.lch))
        return t2


class ItvSet:
    """
    interval set
    """

    def __init__(self, iterable=None):
        """
        iterable中的元素类型为Itv
        """
        self._root: Node = None
        for itv in iterable:
            self.add(itv)

    def add(self, itv: Itv):
        """
        插入区间，并且合并相交的区间
        """
        if itv.empty():
            return

        if self._root is None:
            self._root = Node(itv)
            return

        root = self._root

        t1, t2, t3 = None, None, None
        t1, t2 = _split(root, itv.a)
        if t2 is not None:
            t2, t3 = _split(t2, itv.b)

        create_flag = True
        if t1 is not None:
            t1_max = t1.max()
            if itv.intersect_or_near(t1_max.itv):
                itv |= t1_max.itv
                t1_max.itv = itv
                create_flag = False

        if t2 is not None:
            t2_max = t2.max()
            if itv.intersect_or_near(t2_max.itv):
                itv |= t2_max.itv

        n = None
        if create_flag:
            n = Node(itv)

        self._root = _merge(_merge(t1, n), t3)

    def remove(self, itv: Itv):
        """
        删除区间
        """

    def __in__(self, x):
        """
        判定一个点是否在集合内
        """

    def __iand__(self, s: 'ItvSet'):
        """
        相交集合
        """

    def __ior__(self, s: 'ItvSet'):
        """
        合并集合
        """

    def __isub__(self, s: 'ItvSet'):
        """
        减去集合
        """

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __str__(self):
        return str(list(self))

    def __iter__(self):  # 从小到大返回
        for n in _abc_order_iter(self._root):
            yield n.itv