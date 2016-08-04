# -*- coding: utf-8 -*-


from link.crdt.register import Register
from link.crdt.counter import Counter
from link.crdt.flag import Flag
from link.crdt.set import Set
from link.crdt.map import Map

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


def get_crdt_type_by_name(name):
    return TYPES.get(name, None)


def get_crdt_type_by_py_type(pytype):
    for crdt_type in TYPES.values():
        if crdt_type._py_type in pytype.mro():
            return crdt_type

    return None
