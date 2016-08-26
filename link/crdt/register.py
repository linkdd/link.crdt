# -*- coding: utf-8 -*-

from link.crdt.core import CRDT

from six import string_types


class Register(CRDT):

    _py_type = string_types
    _type_name = 'register'
    _type_err_msg = 'Registers can only be strings'

    @classmethod
    def merge(cls, a, b, context=None):
        cls._assert_mergeable(a, b)

        crdt = cls(value=a._value, context=context)
        crdt._new = a._new if a._vclock >= b._vclock else b._new
        crdt._vclock = max(a._vclock, b._vclock)
        crdt._update_vclock()
        return crdt

    def _post_init(self):
        self._new = None

    def _default_value(self):
        return ''

    @classmethod
    def _match_py_type(cls, pytype):
        return any([
            string_type in pytype.mro()
            for string_type in string_types
        ])

    @classmethod
    def _check_type(cls, value):
        return isinstance(value, cls._py_type)

    def assign(self, value):
        self._assert_type(value)
        self._new = value
        self._update_vclock()

    def __len__(self):
        return len(self.current)

    def isdirty(self):
        return self._new is not None

    def mutation(self):
        return {'assign': self._new}

    @CRDT.current.getter
    def current(self):
        return self._new if self._new is not None else self._value
