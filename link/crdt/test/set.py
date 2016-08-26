# -*- coding: utf-8 -*-

from link.crdt.test.base import UTCase
from unittest import main

from link.crdt.set import Set


class TestSet(UTCase):
    def test_default(self):
        crdt = Set()
        self.assertEqual(crdt.current, set())

    def test_enable(self):
        crdt = Set(value={'1', '2'})

        self.assertEqual(crdt.current, {'1', '2'})

        crdt.add('3')
        crdt.discard('2')

        self.assertEqual(crdt.current, {'1', '3'})
        self.assertEqual(crdt._adds, {'3'})
        self.assertEqual(crdt._removes, {'2'})
        self.assertEqual(crdt._vclock, 2)
        self.assertTrue(crdt.isdirty())
        self.assertEqual(crdt.mutation(), {
            'adds': {'3'},
            'removes': {'2'}
        })

    def test_merge(self):
        a = Set(value={'1', '2'})
        b = Set(value={'1', '2'})

        b.add('3')
        a.discard('2')

        c = Set.merge(a, b)

        self.assertEqual(c.current, {'1', '3'})
        self.assertEqual(c._adds, {'3'})
        self.assertEqual(c._removes, {'2'})
        self.assertEqual(c._vclock, 2)
        self.assertTrue(c.isdirty())
        self.assertEqual(c.mutation(), {
            'adds': {'3'},
            'removes': {'2'}
        })

    def test_fail_merge(self):
        a = Set(value={'1'})
        b = Set(value={'2'})

        with self.assertRaises(ValueError):
            Set.merge(a, b)

    def test_fail_type(self):
        with self.assertRaises(TypeError):
            not_set = 42
            Set(value=not_set)

        with self.assertRaises(TypeError):
            Set(value={42})

    def test_api(self):
        s = Set(value={'1', '2'})

        self.assertIn('1', s)
        self.assertEqual(len(s), 2)

        s2 = {item for item in s}
        self.assertEqual(s.current, s2)

        with self.assertRaises(TypeError):
            s.add(42)


if __name__ == '__main__':
    main()
