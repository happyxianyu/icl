"""
采用红黑树作为基础实现区间树
参考 https://www.boost.org/doc/libs/1_76_0/libs/icl/doc/html/index.html#boost_icl.introduction
按照joining规则实现ItvSet
"""


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
        a,b分别表示左断点和右端点
        """
        self.a = a
        self.b = b
        self.left_open = kind[0] == '('
        self.right_open = kind[1] == ')'
        self._canonicalize()

    @property
    def kind(self):
        return (self.left_open << 1)+ self.right_open

    def _canonicalize(self):
        """
        保证空集表示一致
        """
        if self.a > self.b or \
            (self.a == self.b and (self.left_open or self.right_open) ):
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
    
    def left_to_b(self, b):
        """
        x在b断点的左边
        """
        if self.right_open:
            return self.b > x
        else:
            return self.b >= x 

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
        a,b = self.a, self.b
        l = '[('[self.left_open]
        r = '])'[self.right_open]
        return f'{l}{a}, {b}{r}'




# 每个节点的区间保证不相交
# 按照node.a构建二叉搜索树
# 使用红黑树为基础
class ItvNode:
    def __init__(self, itv: Itv, red=True):
        self.itv = itv
        self.lch: 'ItvNode' = None  # 左子节点
        self.rch: 'ItvNode' = None  # 右子节点
        self.prnt: 'ItvNode' = None # 父节点
        self.red = red    # 是否为红色

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

    @property
    def left_open(self):
        return self.itv.left_open
    
    @left_open.setter
    def _(self, x):
        self.itv.left_open = x
    
    @property
    def right_open(self):
        return self.itv.right_open

    @right_open.setter
    def _(self, x):
        self.itv.right_open = x

    def rotate_l(self):
        x = self
        y = x.rch
        b = y.lch

        y.lch = x
        x.rch = b
        self._rotate_set_prnt(y)
        return y

    def rotate_r(self):
        y = self
        x = y.lch
        b = x.rch

        x.rch = y
        y.lch = b
        self._rotate_set_prnt(x)
        return x

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

    def find(self, x):
        """
        x是一个点，返回落入的区间的节点
        """
        if x in self.itv:
            return self
        if x <= self.a:
            ch = self.lch
        else:
            ch = self.rch
        if ch is not None:
            return ch.find(x)

    def find_by_lower(self, x):
        """
        x表示下界，是一个点
        如果落入了某个区间，则返回这个区间
        否则返回以x为下界的最接近x的区间
        """
        return _find_by_lower(self, x)
    
    def find_by_upper(self, x):
        return _find_by_upper(self, x)

    def _rotate_set_prnt(self, n):
        prnt = self.prnt
        if prnt is None:
            return
        if self is prnt.lch:
            prnt.lch = n
        else:
            prnt.rch = n

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

    def is_root(self):
        return self.prnt is None

    @property
    def sibling(self):
        prnt = self.prnt
        if prnt is None:
            return
        
        lch = prnt.lch
        if self is lch:
            return prnt.rch
        else:
            return lch


def _abc_order_iter(n: ItvNode):
    if n is None:
        return
    yield from _abc_order_iter(n.lch)
    yield n
    yield from _abc_order_iter(n.rch)

def _cba_order_iter(n: ItvNode):
    if n is None:
        return
    yield from _cba_order_iter(n.rch)
    yield n
    yield from _cba_order_iter(n.lch)


def _find_by_lower(self: ItvNode, x):
    if self is None:
        return

    if x in self.itv:
        return self
    if x <= self.a:
        n = _find_by_lower(self.lch, x)
        if n is None:
            return self
        return n
    else:
        return _find_by_lower(self.rch, x)

def _find_by_upper(self: ItvNode, x):
    if self is None:
        return

    if x in self.itv:
        return self
    if x <= self.a:
        return _find_by_upper(self.lch, x)
    else:
        n = _find_by_upper(self.rch, x)
        if n is None:
            return self
        return n


def _find_max(n: ItvNode):
    for x in _cba_order_iter(n):
        return x

def _find_min(n: ItvNode):
    for x in _abc_order_iter(n):
        return x


def _resolve_insert(n: ItvNode):
    prnt = n.prnt
    if prnt is None or not prnt.red:
        return

    # pprnt 一定存在
    prnt_s = prnt.sibling
    if prnt_s is not None and prnt_s.red:
        prnt.red = False
        prnt_s.red = False
        pprnt = prnt.prnt
        pprnt.red = True
        n = pprnt

    if n is prnt.rch:
        prnt.rotate_l()
        n = prnt    # 使得n为lch
        prnt = n.prnt
    prnt.red = False
    pprnt = prnt.prnt
    pprnt.red = True
    pprnt.rotate_r()


def _resolve_remove(n: ItvNode):
    pass



class ItvSet:
    """
    interval set
    """

    def __init__(self, iterable=None):
        """
        iterable中的元素类型为Itv
        """
        self._root:ItvNode = None
        for itv in iterable:
            self.add(ItvNode(itv))

    def add(self, itv: Itv):
        """
        插入区间，并且合并相交的区间
        """
        root = self._root
        if root is None:
            self._root=ItvNode(itv, False)
            return

        n1 = root.find_by_lower(itv.a)
        if n1 is None: # 在最右侧添加节点
            n2 = _find_max(root)
            n = ItvNode(itv)
            n2.rch = n
            _resolve_insert(n)
            return

        if n1.itv.right_to_a(itv.b):    # 相交，需要合并
            n1.itv=itv  
            # TODO: 删除右边相交的节点
        else: # 不相交，在n1左侧添加新的节点
            n = ItvNode(itv)
            n1.lch = n
            _resolve_insert(n)

    def remove(self, itv: Itv):
        """
        删除区间
        """
    
    def __iand__(self, s: ItvSet):
        """
        相交集合
        """

    def __ior__(self, s:ItvSet):
        """
        合并集合
        """

    def __isub__(self, s:ItvSet):
        """
        减去集合
        """

    def __in__(self, x):
        """
        判定一个点是否在集合内
        """

    def min(self):
        pass

    def max(self):
        pass

    def iter_from_lower(self, x):
        pass

    def inter_from_upper(self, x):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __str__(self):
        return super().__str__()

    def __iter__(self):  # 从小到大返回
        yield

