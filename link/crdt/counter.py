# -*-coding: utf-8 -*-

from link.crdt.core import CRDT


class Counter(CRDT):

    _py_type = int
    _type_name = 'counter'
    _type_err_msg = 'Counters can only be integers'

    @classmethod
    def merge(cls, a, b, context=None):
        cls._assert_mergeable(a, b)

        crdt = cls(value=a._value, context=context)
        crdt._increment = a._increment + b._increment
        crdt._vclock = max(a._vclock, b._vclock)
        crdt._update_vclock()
        return crdt

    def _post_init(self):
        self._increment = 0

    def _default_value(self):
        return 0

    @classmethod
    def _match_py_type(cls, pytype):
        return cls._py_type in pytype.mro() and bool not in pytype.mro()

    @classmethod
    def _check_type(cls, value):
        return isinstance(value, cls._py_type) and not isinstance(value, bool)

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
