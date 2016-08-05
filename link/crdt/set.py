# -*- coding: utf-8 -*-

from link.crdt.core import CRDT

from six import string_types
import collections


class Set(collections.Set, CRDT):

    _py_type = collections.Set
    _type_name = 'set'
    _type_err_msg = 'Sets can only be set of strings'

    @classmethod
    def merge(cls, a, b):
        cls._assert_mergeable(a, b)

        crdt = cls()
        crdt._adds = a._adds.union(b._adds)
        crdt._removes = a._removes.union(b._removes)
        crdt._vclock = max(a._vclock, b._vclock)
        crdt._update_vclock()
        return crdt

    def _post_init(self):
        self._adds = set()
        self._removes = set()

    def _default_value(self):
        return frozenset()

    def _check_element(self, element):
        if not isinstance(element, string_types):
            raise TypeError('Set elements can only be strings')

    def _check_type(self, value):
        if not isinstance(value, self._py_type):
            return False

        for element in value:
            if not isinstance(element, string_types):
                return False

        return True

    def _coerce_value(self, value):
        return frozenset(value)

    def __contains__(self, element):
        return element in self.current

    def __iter__(self):
        return iter(self.current)

    def __len__(self):
        return len(self.current)

    def add(self, element):
        self._check_element(element)
        self._adds.add(element)
        self._update_vclock()

    def discard(self, element):
        self._check_element(element)
        self._removes.add(element)
        self._update_vclock()

    def isdirty(self):
        return len(self._removes | self._adds) > 0

    def mutation(self):
        return {
            'adds': list(self._adds),
            'removes': list(self._removes)
        }

    @CRDT.current.getter
    def current(self):
        return set(self._value) + self._adds - self._removes
