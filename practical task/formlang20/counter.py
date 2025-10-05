from operator import contains

from .int_type import IntWithInf


class CounterFactory:
    @staticmethod
    def get_counter(target_char):
        class Counter:
            def __init__(self, char=None):
                self._count = [IntWithInf(0) for _ in range(4)]

                if char == target_char:
                    self._count[3] = IntWithInf(1)

                self._contains_empty = char == '1'

            def star(self):
                if self._count[1] and self._count[2]:
                    self._count[0] = IntWithInf.max(self._count[0], self._count[1] + self._count[2])

                if self._count[3]:
                    self._count[3] = IntWithInf('INF')

                    if self._count[1] and self._count[2]:
                        self._count[0] = IntWithInf('INF')

                    if self._count[1]:
                        self._count[1] = IntWithInf('INF')

                    if self._count[2]:
                        self._count[2] = IntWithInf('INF')

                return self

            def __mul__(self, other):
                if not isinstance(other, Counter):
                    raise TypeError('Object should be of type Counter')
                other_count = other.get_count()
                new_count = [IntWithInf(0) for _ in range(4)]
                contains_empty = self._contains_empty and other.contains_empty()

                new_count[0] = IntWithInf.max(self._count[0], other_count[0])
                new_count[1] = IntWithInf.max(self._count[1], self._count[3])
                new_count[2] = IntWithInf.max(other_count[2], other_count[3])

                if self._contains_empty:
                    new_count[1] = IntWithInf.max(new_count[1], other_count[1], other_count[3])
                    new_count[3] = IntWithInf.max(new_count[3], other_count[3])
                if other.contains_empty():
                    new_count[2] = IntWithInf.max(new_count[1], self._count[2], self._count[3])
                    new_count[3] = IntWithInf.max(new_count[3], self._count[3])

                if other_count[0] or other_count[2]:
                    new_count[1] = IntWithInf.max(new_count[1], self._count[3])
                if self._count[0] or self._count[1]:
                    new_count[2] = IntWithInf.max(new_count[2], other_count[3])

                if self._count[2] and other_count[1]:
                    new_count[0] = IntWithInf.max(new_count[0], self._count[2] + other_count[1])

                if self._count[3] and other_count[1]:
                    new_count[1] = IntWithInf.max(new_count[1], self._count[3] + other_count[1])

                if self._count[2] and other_count[3]:
                    new_count[2] = IntWithInf.max(new_count[2], self._count[2] + other_count[3])

                if self._count[3] and other_count[3]:
                    new_count[3] = IntWithInf.max(new_count[3], self._count[3] + other_count[3])

                result = Counter()
                result.set_count(new_count)
                result.set_contains_empty(contains_empty)
                return result

            def __add__(self, other):
                if not isinstance(other, Counter):
                    raise TypeError('Object should be of type Counter')
                other_count = other.get_count()
                new_count = [IntWithInf(0) for _ in range(4)]
                contains_empty = self._contains_empty or other.contains_empty()

                for i in range(4):
                    new_count[i] = IntWithInf.max(self._count[i], other_count[i])

                result = Counter()
                result.set_count(new_count)
                result.set_contains_empty(contains_empty)
                return result

            def __repr__(self):
                return self._count.__repr__()

            def get_count(self):
                return self._count

            def set_count(self, count):
                if len(count) != 4:
                    raise ValueError('Counter must have 4 elements')
                self._count = [IntWithInf(i) for i in count]

            def contains_empty(self):
                return self._contains_empty

            def set_contains_empty(self, contains_empty):
                self._contains_empty = contains_empty

            def clear(self):
                self._count = [IntWithInf(0) for _ in range(4)]

        return Counter
