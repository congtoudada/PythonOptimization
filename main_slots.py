import sys


class A(object):
    def __init__(self):
        self.x = 42
        self.y = 42
        self.z = 42
        self.t = 42
        self.u = 42
        self.v = 42
        self.w = 42


class B(object):
    __slots__ = ('x', 'y', 'z', 't', 'u', 'v', 'w')

    def __init__(self):
        self.x = 42
        self.y = 42
        self.z = 42
        self.t = 42
        self.u = 42
        self.v = 42
        self.w = 42


print(sys.getsizeof(A()))  # 64
print(sys.getsizeof(B()))  # 64
a = A()
setattr(a, "x", 44)
