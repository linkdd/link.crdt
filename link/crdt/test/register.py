# -*- coding: utf-8 -*-

from link.crdt.test.base import UTCase
from unittest import main

from link.crdt.register import Register


class TestRegister(UTCase):
    def test_default(self):
        crdt = Register()
        self.assertEqual(crdt.current, '')

    def test_enable(self):
        crdt = Register(value='initial')

        self.assertEqual(crdt.current, 'initial')

        crdt.assign('new')

        self.assertEqual(crdt.current, 'new')
        self.assertEqual(crdt._new, 'new')
        self.assertEqual(crdt._vclock, 1)
        self.assertTrue(crdt.isdirty())
        self.assertEqual(crdt.mutation(), {'assign': 'new'})

    def test_merge(self):
        a = Register(value='initial')
        b = Register(value='initial')

        b.assign('1')
        b.assign('2')
        a.assign('1')

        c = Register.merge(a, b)

        self.assertEqual(c.current, '2')
        self.assertEqual(c._new, '2')
        self.assertEqual(c._vclock, 3)
        self.assertTrue(c.isdirty())
        self.assertEqual(c.mutation(), {'assign': '2'})

    def test_fail_merge(self):
        a = Register(value='1')
        b = Register(value='2')

        with self.assertRaises(ValueError):
            Register.merge(a, b)

    def test_fail_type(self):
        with self.assertRaises(TypeError):
            not_str = 42
            Register(value=not_str)

    def test_api(self):
        r = Register(value='hello')
        self.assertEqual(len(r), 5)


if __name__ == '__main__':
    main()
