# -*-coding: utf-8 -*-

from collections import Mapping

from link.crdt.core import CRDT
from link.crdt.register import Register
from link.crdt.counter import Counter
from link.crdt.flag import Flag
from link.crdt.set import Set


class Map(Mapping, CRDT):

    _py_type = dict
    _type_name = 'map'
    _type_err_msg = 'Map must be a dict with keys ending with "_{datatype}"'

    @classmethod
    def _check_same_value(cls, a, b):
        for key in a._value:
            if key in b._value:
                aval = a._value[key]
                bval = b._value[key]

                if not aval._check_same_value(aval, bval):
                    return False

            else:
                return False

        return True

    @classmethod
    def merge(cls, a, b, context=None):
        cls._assert_mergeable(a, b)

        crdt = cls(value=a._compute_value(), context=context)
        crdt._removes = a._removes.union(b._removes)

        # merge a and b values
        for key in a._value:
            if key in b._value:
                suba = a._value[key]
                subb = b._value[key]

                crdt._updates[key] = suba.merge(suba, subb, context=crdt)
                del crdt._value[key]

        # merge a and b updates
        for key in a._updates:
            if key not in b._updates:
                crdt._updates[key] = a._updates[key]

            else:
                suba = a._updates[key]
                subb = b._updates[key]

                crdt._updates[key] = suba.merge(suba, subb, context=crdt)

        # complete with missing keys from a
        for key in b._updates:
            if key not in a._updates:
                crdt._updates[key] = b._updates[key]

        crdt._vclock = max(a._vclock, b._vclock)
        crdt._update_vclock()

        return crdt

    def _post_init(self):
        self._removes = set()
        self._updates = {}

    def _default_value(self):
        return dict()

    @classmethod
    def _check_key(cls, key):
        for typename in TYPES:
            suffix = '_{0}'.format(typename)

            if key.endswith(suffix) and len(key) > len(suffix):
                return

        raise TypeError('Invalid key: {0}'.format(key))

    def _get_key_type(self, key):
        datatype = key.rsplit('_', 1)[1]
        return TYPES[datatype]

    @classmethod
    def _check_type(cls, value):
        if not isinstance(value, cls._py_type):
            return False

        for key in value:
            try:
                cls._check_key(key)

            except TypeError:
                return False

        return True

    def __contains__(self, key):
        self._check_key(key)

        return (key in self._value) or (key in self._updates)

    def __getitem__(self, key):
        self._check_key(key)

        if key in self._value:
            return self._value[key]

        else:
            if key not in self._updates:
                self._updates[key] = self._get_key_type(key)(context=self)
                self._update_vclock()

            return self._updates[key]

    def __delitem__(self, key):
        self._check_key(key)
        self._removes.add(key)
        self._update_vclock()

    def __len__(self):
        return len(self.current)

    def __iter__(self):
        return iter(self.current)

    def isdirty(self):
        return bool(self._removes) or bool(self._updates)

    def _coerce_value(self, value):
        cvalue = {}

        for key in value:
            self._check_key(key)
            cvalue[key] = self._get_key_type(key)(
                value=value[key],
                context=self
            )

        return cvalue

    def mutation(self):
        result = []

        result += [
            {'remove': r}
            for r in self._removes
        ]

        result += [
            {
                'update': key,
                'mutation': data[key].mutation()
            }
            for data in [self._value, self._updates]
            for key in data
            if key not in self._removes
        ]

        return result

    @CRDT.current.getter
    def current(self):
        cvalue = {}

        for key in self._value:
            if key not in self._removes:
                cvalue[key] = self._value[key].current

        for key in self._updates:
            if key not in self._removes:
                cvalue[key] = self._updates[key].current

        return cvalue

    def _compute_value(self):
        return {
            key: v.current if not isinstance(v, Map) else v._compute_value()
            for key, v in self._value.items()
        }


TYPES = {
    cls._type_name: cls
    for cls in [
        Counter,
        Flag,
        Set,
        Register,
        Map
    ]
}
