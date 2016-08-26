# -*- coding: utf-8 -*-

from link.crdt.test.base import UTCase
from unittest import main

from link.crdt.flag import Flag


class TestFlag(UTCase):
    def test_default(self):
        crdt = Flag()
        self.assertEqual(crdt.current, False)

    def test_enable(self):
        crdt = Flag(value=False)

        self.assertFalse(crdt.current)
        self.assertFalse(crdt.isdirty())

        crdt.enable()

        self.assertTrue(crdt.current)
        self.assertEqual(crdt._mutation, 'enable')
        self.assertEqual(crdt._vclock, 1)
        self.assertTrue(crdt.isdirty())
        self.assertEqual(crdt.mutation(), {'enable': None})

        crdt.disable()

        self.assertFalse(crdt.current)
        self.assertEqual(crdt._mutation, 'disable')
        self.assertEqual(crdt._vclock, 2)
        self.assertTrue(crdt.isdirty())
        self.assertEqual(crdt.mutation(), {'disable': None})

    def test_merge(self):
        a = Flag(value=False)
        b = Flag(value=False)

        b.enable()
        b.disable()
        a.enable()

        c = Flag.merge(a, b)

        self.assertFalse(c.current)
        self.assertEqual(c._mutation, 'disable')
        self.assertEqual(c._vclock, 3)
        self.assertTrue(c.isdirty())
        self.assertEqual(c.mutation(), {'disable': None})

    def test_fail_merge(self):
        a = Flag(value=False)
        b = Flag(value=True)

        with self.assertRaises(ValueError):
            Flag.merge(a, b)

    def test_fail_type(self):
        with self.assertRaises(TypeError):
            Flag(value='not bool')


if __name__ == '__main__':
    main()
