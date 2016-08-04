# -*- coding: utf-8 -*-

from link.crdt.utils import TYPES
from link.crdt.register import Register
from link.crdt.counter import Counter
from link.crdt.flag import Flag
from link.crdt.set import Set
from link.crdt.map import Map


class CRDTDiff(object):
    def counter(self, crdt, a, b):
        crdt.increment(b - a)

    def flag(self, crdt, a, b):
        if b:
            crdt.enable()

        else:
            crdt.disable()

    def register(self, crdt, a, b):
        crdt.assign(b)

    def set(self, crdt, a, b):
        for item in a:
            if item not in b:
                crdt.discard(item)

        for item in b:
            crdt.add(item)

    def map(self, crdt, a, b):
        for key in a:
            if key not in b:
                del crdt[key]

        suffix = lambda tn: '_{0}'.format(tn)

        for key in b:
            if key.endswith(suffix(Counter._type_name)):
                self.counter(crdt[key], a.get(key, 0), b[key])

            elif key.endswith(suffix(Flag._type_name)):
                self.flag(crdt[key], a.get(key, False), b[key])

            elif key.endswith(suffix(Register._type_name)):
                self.register(crdt[key], a.get(key, ''), b[key])

            elif key.endswith(suffix(Set._type_name)):
                self.set(crdt[key], a.get(key, set()), b[key])

            elif key.endswith(suffix(Map._type_name)):
                self.map(crdt[key], a.get(key, {}), b[key])

    def __call__(self, a, b):
        amro = set(a.__class__.mro())
        bmro = set(b.__class__.mro())

        if not (amro.issubset(bmro) or bmro.issubset(amro)):
            raise TypeError('Supplied arguments must be of the same type')

        for crdt_type in TYPES.values():
            if isinstance(a, crdt_type._py_type):
                crdt = crdt_type(value=a)

                method = getattr(self, crdt_type._type_name)
                method(crdt, a, b)

                return crdt

        raise TypeError('Supplied arguments are not recognized by any CRDT')


def crdt_diff(a, b):
    cd = CRDTDiff()
    return cd(a, b)
