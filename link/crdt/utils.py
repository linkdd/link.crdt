# -*- coding: utf-8 -*-


from link.crdt.map import TYPES


def get_crdt_type_by_name(name):
    return TYPES.get(name, None)


def get_crdt_type_by_py_type(pytype):
    for crdt_type in TYPES.values():
        if crdt_type._py_type in pytype.mro():
            return crdt_type

    return None
