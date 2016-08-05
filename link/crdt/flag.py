# -*-coding: utf-8 -*-

from link.crdt.core import CRDT


class Flag(CRDT):

    _py_type = bool
    _type_name = 'flag'
    _type_err_msg = 'Flags can only be booleans'

    @classmethod
    def merge(cls, a, b):
        cls._assert_mergeable(a, b)

        crdt = cls()
        crdt._mutation = a._mutation if a._vclock >= b._vclock else b._mutation
        crdt._vclock = max(a._vclock, b._vclock)
        crdt._update_vclock()
        return crdt

    def _post_init(self):
        self._mutation = None

    def _default_value(self):
        return False

    def _check_type(self, value):
        return isinstance(value, self._py_type)

    def enable(self):
        self._mutation = 'enable'
        self._update_vclock()

    def disable(self):
        self._mutation = 'disable'
        self._update_vclock()

    def isdirty(self):
        return self._mutation is not None

    def mutation(self):
        return {self._mutation: None}

    @CRDT.current.getter
    def current(self):
        if self._mutation is None:
            return self._value

        else:
            return self._mutation == 'enable'
