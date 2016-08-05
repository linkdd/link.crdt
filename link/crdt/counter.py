# -*-coding: utf-8 -*-

from link.crdt.core import CRDT


class Counter(CRDT):

    _py_type = int
    _type_name = 'counter'
    _type_err_msg = 'Counters can only be integers'

    @classmethod
    def merge(cls, a, b):
        cls._assert_mergeable(a, b)

        crdt = cls()
        crdt._increment = a._increment + b._increment
        crdt._vclock = max(a._vclock, b._vclock)
        crdt._update_vclock()
        return crdt

    def _post_init(self):
        self._increment = 0

    def _default_value(self):
        return 0

    def _check_type(self, value):
        return isinstance(value, self._py_type)

    def increment(self, amount=1):
        self._assert_type(amount)
        self._increment += amount
        self._update_vclock()

    def decrement(self, amount=1):
        self._assert_type(amount)
        self._increment -= amount
        self._update_vclock()

    def isdirty(self):
        return self._increment != 0

    def mutation(self):
        return {'increment': self._increment}

    @CRDT.current.getter
    def current(self):
        return self._value + self._increment
