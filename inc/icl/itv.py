from .inf import *

__all__ = [
    'Itv'
]


def _left_or_eq_to(a, b, open_a, open_b):
    """
    a <= b 当两个全是close
    a < b 其他情况
    """
    if open_a or open_b:
        return a < b
    else:
        return a <= b


def _left_or_near_to(a, b, open_a, open_b):
    """
    a <= b 一个是close
    a < b 其他情况
    """
    if open_a and open_b:
        return a < b
    else:
        return a <= b


class Itv:
    """
    Interval
    """

    def __init__(self, a, b, kind='[]'):
        """
        kind表示区间类型, 根据数学上的表示，[]表示闭区间， ()表示开区间
        a,b分别表示左断点和右端点
        """
        self.a = a
        self.b = b
        self.left_open = kind[0] == '('
        self.right_open = kind[1] == ')'
        self._canonicalize()

    @property
    def kind(self):
        return (self.left_open << 1) + self.right_open

    def _canonicalize(self):
        """
        保证空集表示一致
        """
        if self.a > self.b or \
                (self.a == self.b and (self.left_open or self.right_open)):
            # 方便比较
            self.a = inf
            self.b = -inf

    def empty(self):
        return self.a > self.b

    def __in__(self, x):
        """
        判定某个点是否在区间内
        """
        return self.right_to_a(x) and self.left_to_b(x)

    def right_to_a(self, x):
        """
        x在a端点的右边
        """
        if self.left_open:
            return self.a < x
        else:
            return self.a <= x

    def left_to_b(self, x):
        """
        x在b断点的左边
        """
        if self.right_open:
            return self.b > x
        else:
            return self.b >= x

    def intersect(self, itv: 'Itv') -> bool:
        """
        是否相交
        """
        return _left_or_eq_to(self.a, itv.b, self.left_open, itv.right_open) \
               and _left_or_eq_to(itv.a, self.b, itv.left_open, self.right_open)

    def intersect_or_near(self, itv: 'Itv') -> bool:
        """
        是否相交或紧挨着
        """
        return _left_or_near_to(self.a, itv.b, self.left_open, itv.right_open) \
               and _left_or_near_to(itv.a, self.b, itv.left_open, self.right_open)

    def __and__(self, x: 'Itv'):
        a = max(self.a, x.a)
        b = min(self.b, x.b)

        if a == self.a == x.a:
            left_open = self.left_open or x.left_open
        elif a == self.a:
            left_open = self.left_open
        elif a == x.a:
            left_open = x.left_open

        if b == self.b == x.b:
            right_open = self.right_open or x.right_open
        elif b == self.b:
            right_open = self.right_open
        elif b == x.b:
            right_open = x.right_open

        res = Itv(a, b)
        res.left_open = left_open
        res.right_open = right_open
        res._canonicalize()
        return res

    def __iand__(self, x: 'Itv'):
        a = max(self.a, x.a)
        b = min(self.b, x.b)
        if a == self.a == x.a:
            left_open = self.left_open or x.left_open
        elif a == self.a:
            left_open = self.left_open
        elif a == x.a:
            left_open = x.left_open

        if b == self.b == x.b:
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
        return self

    def __or__(self, itv: 'Itv'):
        assert self.intersect_or_near(itv)

        a = min(self.a, itv.a)
        b = max(self.b, itv.b)

        if a == self.a == itv.a:
            left_open = self.left_open or itv.left_open
        elif a == self.a:
            left_open = self.left_open
        elif a == itv.a:
            left_open = itv.left_open

        if b == self.b == itv.b:
            right_open = self.right_open or itv.right_open
        elif b == self.b:
            right_open = self.right_open
        elif b == itv.b:
            right_open = itv.right_open

        res = Itv(a, b)
        res.left_open = left_open
        res.right_open = right_open
        res._canonicalize()
        return res

    def __ior__(self, itv: 'Itv'):
        assert self.intersect_or_near(itv)

        a = min(self.a, itv.a)
        b = max(self.b, itv.b)

        if a == self.a == itv.a:
            left_open = self.left_open or itv.left_open
        elif a == self.a:
            left_open = self.left_open
        elif a == itv.a:
            left_open = itv.left_open

        if b == self.b == itv.b:
            right_open = self.right_open or itv.right_open
        elif b == self.b:
            right_open = self.right_open
        elif b == itv.b:
            right_open = itv.right_open

        self.a = a
        self.b = b
        self.left_open = left_open
        self.right_open = right_open
        self._canonicalize()
        return self

    def __gt__(self, x):
        if self.left_open:
            return x <= self.a
        else:
            return x < self.a

    def __ge__(self, x):
        if self.right_open:
            return x < self.b
        else:
            return x <= self.b

    def __lt__(self, x):
        if self.right_open:
            return x >= self.b
        else:
            return x > self.b

    def __le__(self, x):
        if self.left_open:
            return x >= self.a
        else:
            return x > self.a

    def __eq__(self, x: 'Itv'):
        return self.kind == x.kind and self.a == x.a and self.b == x.b

    def __str__(self):
        a, b = self.a, self.b
        l = '[('[self.left_open]
        r = '])'[self.right_open]
        return f'{l}{a}, {b}{r}'

    __repr__ = __str__




