class Itv:
    """
    Interval
    """

class ItvSet:
    """
    interval set
    """

    def __init__(self, iterable=None):
        """
        iterable中的元素类型为Itv
        """

    def add(self, itv: Itv):
        """
        插入区间，并且合并相交的区间
        """

    def remove(self, itv: Itv):
        """
        删除区间
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