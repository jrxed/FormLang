class IntWithInf:
    def __init__(self, x=0):
        if x == 'INF':
            self._is_infinite = True
            self._x = 0
            return

        if isinstance(x, IntWithInf):
            self._is_infinite = x.is_infinite()
            self._x = 0 if self._is_infinite else x.int()
            return

        if not isinstance(x, int):
            raise TypeError('Type of argument should be IntWithInf or integer or string "INF"')
        self._is_infinite = False
        self._x = x

    def int(self):
        if self._is_infinite:
            raise ValueError("Can't write infinite number with digits")
        return self._x

    def is_infinite(self):
        return self._is_infinite

    def __add__(self, other):
        if self.is_infinite() or other.is_infinite():
            return IntWithInf('INF')
        return IntWithInf(self.int() + other.int())

    def __bool__(self):
        return self._is_infinite or self._x != 0

    def __repr__(self):
        return 'INF' if self._is_infinite else str(self._x)

    def __eq__(self, other):
        if isinstance(other, IntWithInf):
            if self._is_infinite:
                return other.is_infinite()
            return not other.is_infinite() and self.int() == other.int()
        return not self.is_infinite() and self._x == other

    @classmethod
    def max(cls, *args):
        if not args:
            raise TypeError("Arguments list can't be empty")
        return IntWithInf('INF' if any(i.is_infinite() for i in args) else max(i.int() for i in args))
