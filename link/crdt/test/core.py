# -*- coding: utf-8 -*-

from link.crdt.test.base import UTCase
from unittest import main

from link.crdt.counter import Counter
from link.crdt.flag import Flag
from link.crdt.register import Register
from link.crdt.set import Set
from link.crdt.map import Map


class TestCounter(UTCase):
    def test_merge_different_types(self):
        c = Counter()
        f = Flag()
        r = Register()
        s = Set()
        m = Map()

        tuples = [
            (Counter, c, f),
            (Flag, f, r),
            (Register, r, s),
            (Set, s, m),
            (Map, m, c)
        ]

        for cls, a, b in tuples:
            with self.assertRaises(TypeError):
                cls.merge(a, b)

    def test_context(self):
        m = Map()
        Counter(context=m)

        with self.assertRaises(TypeError):
            Counter(context=42)


if __name__ == '__main__':
    main()
