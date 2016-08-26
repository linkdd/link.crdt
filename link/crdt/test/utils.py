# -*- coding: utf-8 -*-

from link.crdt.test.base import UTCase
from unittest import main

from link.crdt.utils import get_crdt_type_by_name, get_crdt_type_by_py_type
from link.crdt.counter import Counter
from link.crdt.flag import Flag
from link.crdt.register import Register
from link.crdt.set import Set
from link.crdt.map import Map

from six import string_types
import collections


class TestUtils(UTCase):
    def test_get_type_by_name(self):
        l = [
            (Counter, 'counter'),
            (Flag, 'flag'),
            (Register, 'register'),
            (Set, 'set'),
            (Map, 'map')
        ]

        for crdt_type, name in l:
            got = get_crdt_type_by_name(name)
            self.assertIs(got, crdt_type)

        got = get_crdt_type_by_name('unknown')
        self.assertIsNone(got)

    def test_get_type_by_py_type(self):
        l = [
            (Counter, int),
            (Flag, bool),
            (Register, str),
            (Set, collections.Set),
            (Map, dict)
        ]

        for crdt_type, py_type in l:
            got = get_crdt_type_by_py_type(py_type)
            self.assertIs(got, crdt_type)

        got = get_crdt_type_by_py_type(UTCase)
        self.assertIsNone(got)

if __name__ == '__main__':
    main()
