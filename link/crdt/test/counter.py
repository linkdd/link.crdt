# -*- coding: utf-8 -*-

from link.crdt.test.base import UTCase
from unittest import main

from link.crdt.counter import Counter


class TestCounter(UTCase):
    def test_default(self):
        crdt = Counter()
        self.assertEqual(crdt.current, 0)

    def test_increment(self):
        crdt = Counter(value=5)
        self.assertEqual(crdt.current, 5)

        crdt.increment()

        self.assertEqual(crdt.current, 6)
        self.assertEqual(crdt._increment, 1)
        self.assertEqual(crdt._vclock, 1)
        self.assertTrue(crdt.isdirty())
        self.assertEqual(crdt.mutation(), {'increment': 1})

        crdt.decrement()

        self.assertEqual(crdt.current, 5)
        self.assertEqual(crdt._increment, 0)
        self.assertEqual(crdt._vclock, 2)
        self.assertFalse(crdt.isdirty())
        self.assertEqual(crdt.mutation(), {'increment': 0})

    def test_merge(self):
        a = Counter(value=5)
        b = Counter(value=5)

        b.increment(3)
        b.increment(2)
        a.increment(2)

        c = Counter.merge(a, b)

        self.assertEqual(c.current, 12)
        self.assertEqual(c._increment, 7)
        self.assertEqual(c._vclock, 3)
        self.assertTrue(c.isdirty())
        self.assertEqual(c.mutation(), {'increment': 7})

    def test_fail_merge(self):
        a = Counter(value=5)
        b = Counter(value=7)

        with self.assertRaises(ValueError):
            Counter.merge(a, b)

    def test_fail_type(self):
        with self.assertRaises(TypeError):
            Counter(value='not int')


if __name__ == '__main__':
    main()
