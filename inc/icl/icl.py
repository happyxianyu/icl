import typing
from infinity import inf  # 用于表示无穷大

__all__ = [
    'inf',
    'Itv',
    'ItvSet'
]

class Itv:
    """
    Interval
    """
    def __init__(self, a, b, kind='[]'):
        """
        kind表示区间类型, 根据数学上的表示，[]表示闭区间， ()表示开区间
        """
        self.a = a
        self.b = b
        self.left_open = kind[0] == '('
        self.right_open = kind[1] == ')'
        self._canonicalize()

    @property
    def kind(self):
        return self.left_open << 1 + self.right_open

    def _canonicalize(self):
        if self.a > self.b or \
            (self.a == self.b and (self.left_open or self.right_open) ):
            self.a = self.b = None

    def empty(self):
        return self.a is None

    def __and__(self, x: 'Itv'):
        a = max(self.a, x.a)
        b = min(self.b, x.b)
        if a == self.a == self.a:
            left_open = self.left_open or x.left_open
        elif a == self.a:
            left_open = self.left_open
        elif a == x.a:
            left_open = x.left_open
        
        if b == self.b == self.b:
            right_open = self.right_open or x.right_open
        elif b == self.b:
            right_open = self.right_open
        elif b == x.b:
            right_open = x.right_open

        res = Itv(a,b)
        res.left_open = left_open
        res.right_open = right_open
        res._canonicalize()
        return res

    def __iand__(self, x: 'Itv'):
        a = max(self.a, x.a)
        b = min(self.b, x.b)
        if a == self.a == self.a:
            left_open = self.left_open or x.left_open
        elif a == self.a:
            left_open = self.left_open
        elif a == x.a:
            left_open = x.left_open
        
        if b == self.b == self.b:
            right_open = self.right_open or x.right_open
        elif b == self.b:
            right_open = self.right_open
        elif b == x.b:
            right_open = x.right_open

        self.a = a
        self.b = b
        self.left_open = left_open
        self.right_open = right_open
        self._canonicalize()

    def __or__(self, x: 'Itv'):
        a = min(self.a, x.a)
        b = max(self.b, x.b)
        if a == self.a == self.a:
            left_open = self.left_open and x.left_open
        elif a == self.a:
            left_open = self.left_open
        elif a == x.a:
            left_open = x.left_open
        
        if b == self.b == self.b:
            right_open = self.right_open and x.right_open
        elif b == self.b:
            right_open = self.right_open
        elif b == x.b:
            right_open = x.right_open

        res = Itv(a,b)
        res.left_open = left_open
        res.right_open = right_open
        res._canonicalize()
        return res
    
    def __ior__(self, x: 'Itv'):
        a = min(self.a, x.a)
        b = max(self.b, x.b)
        if a == self.a == self.a:
            left_open = self.left_open and x.left_open
        elif a == self.a:
            left_open = self.left_open
        elif a == x.a:
            left_open = x.left_open
        
        if b == self.b == self.b:
            right_open = self.right_open and x.right_open
        elif b == self.b:
            right_open = self.right_open
        elif b == x.b:
            right_open = x.right_open
        
        self.a = a
        self.b = b
        self.left_open = left_open
        self.right_open = right_open
        self._canonicalize()


    def __lt__(self, x):
        if type(x) == Itv:
            if self.b <= x.a:
                return self.right_open or x.left_open or (self.b<x.a)
        else:
            if self.empty():
                return False
            else:
                # TODO: close or open
                return self.b < x

    def __gt__(self, x):
        if type(x) == Itv:
            return x < self
        else:
            pass # TODO

    def __eq__(self, x: 'Itv'):
        return self.kind == x.kind and self.a == x.a and self.b == x.b

    def __str__(self):
        a,b = self.a, self.b
        l = '[('[self.left_open]
        r = '])'[self.right_open]
        return f'{l}{a}, {b}{r}'



class ItvNode:
    def __init__(self, itv: Itv):
        self.itv = itv
        self.lch: 'ItvNode' = None
        self.rch: 'ItvNode' = None
        self.prnt: 'ItvNode' = None

    def rotate_l(self):
        x = self
        y = x.rch
        b = y.lch

        y.lch = x
        x.rch = b
        self._rotate_set_prnt(n)

    def rotate_r(self):
        y = self
        x = y.lch
        b = x.rch

        x.rch = y
        y.lch = b
        self._rotate_set_prnt(n)

    def _rotate_set_prnt(self, n):
        prnt = self.prnt
        if self is prnt.lch:
            prnt.lch = n
        else:
            prnt.rch = n

    def _abc_order_iter(self):
        lch = self.lch
        rch = self.rch
        if lch is not None:
            yield from lch._preorder_iter()
        yield self
        if rch is not None:
            yield from rch._abc_order_iter()
    
    def _cba_order_iter(self):
        lch = self.lch
        rch = self.rch
        if rch is not None:
            yield from rch._abc_order_iter()
        yield self
        if lch is not None:
            yield from lch._preorder_iter()

    def next_high(self):
        rch = self.rch
        prnt = self.prnt
        if rch is not None:
            return rch.next_high()
        if prnt is not None and prnt.lch is self:
            return prnt

    def next_low(self):
        lch = self.lch
        prnt = self.prnt
        if lch is not None:
            return lch.next_low()
        if prnt is not None and prnt.rch is self:
            return prnt

    @property
    def a(self):
        return self.itv.a

    @a.setter
    def _(self, x):
        self.itv.a=x

    @property
    def b(self):
        return self.itv.b

    @b.setter
    def _(self, x):
        self.itv.b = x


class ItvSet:
    """
    interval set
    """

    def __init__(self, iterable=None):
        """
        iterable中的元素类型为Itv
        """
        for itv in iterable:
            self.add(ItvNode(itv))
        self._root:ItvNode = None

    def add(self, x: tuple):
        pass

    def _min(self):
        for n in self._root._abc_order_iter():
            return n

    def _max(self):
        for n in self._root._cba_order_iter():
            return n
    
    def min(self):
        return self._min().itv

    def max(self):
        return self._max().itv

    def iter_from_low(self, x):
        """

        """
        n = self._root
        
        pass

    def inter_from_high(self, x):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __iand__(self, other):
        pass

    def __ior__(self, other):
        pass

    def __isub__(self, other):
        pass

    def __str__(self):
        return super().__str__()

    def __iter__(self):  # 从小到大返回
        yield
