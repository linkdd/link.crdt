# -*- coding: utf-8 -*-

from link.crdt.test.base import UTCase
from unittest import main

from link.crdt.diff import crdt_diff


class TestDiff(UTCase):
    def test_diff_counter(self):
        crdt = crdt_diff(5, 6)

        self.assertEqual(crdt._value, 5)
        self.assertEqual(crdt._increment, 1)
        self.assertEqual(crdt.current, 6)

    def test_diff_flag(self):
        crdt = crdt_diff(False, True)

        self.assertEqual(crdt._value, False)
        self.assertEqual(crdt.current, True)
        self.assertEqual(crdt._mutation, 'enable')

        crdt = crdt_diff(True, False)

        self.assertEqual(crdt._value, True)
        self.assertEqual(crdt.current, False)
        self.assertEqual(crdt._mutation, 'disable')

    def test_diff_register(self):
        crdt = crdt_diff('test', 'test2')

        self.assertEqual(crdt._value, 'test')
        self.assertEqual(crdt.current, 'test2')
        self.assertEqual(crdt._new, 'test2')

    def test_diff_set(self):
        crdt = crdt_diff({'1', '2'}, {'2', '3'})

        self.assertEqual(crdt._value, {'1', '2'})
        self.assertEqual(crdt.current, {'2', '3'})
        self.assertEqual(crdt._adds, {'2', '3'})
        self.assertEqual(crdt._removes, {'1'})

    def test_diff_map(self):
        a = {
            'a_counter': 5,
            'b_flag': True,
            'c_register': 'test',
            'd_set': {'1', '2'},
            'e_map': {
                'a_counter': 5
            },
            'f_map': {
                'a_counter': 5
            }
        }
        b = {
            'a_counter': 7,
            'b_flag': False,
            'c_register': 'test2',
            'd_set': {'2', '3'},
            'f_map': {
                'a_counter': 6
            }
        }
        crdt = crdt_diff(a, b)

        self.assertIn('a_counter', crdt._value)
        self.assertIn('b_flag', crdt._value)
        self.assertIn('c_register', crdt._value)
        self.assertIn('d_set', crdt._value)
        self.assertIn('f_map', crdt._value)
        self.assertIn('e_map', crdt._removes)
        self.assertEqual(crdt.current, b)
        self.assertItemsEqual(crdt.mutation(), [
            {'remove': 'e_map'},
            {
                'update': 'a_counter',
                'mutation': {
                    'increment': 2
                }
            },
            {
                'update': 'b_flag',
                'mutation': {
                    'disable': None
                }
            },
            {
                'update': 'c_register',
                'mutation': {
                    'assign': 'test2'
                }
            },
            {
                'update': 'd_set',
                'mutation': {
                    'adds': {'2', '3'},
                    'removes': {'1'}
                }
            },
            {
                'update': 'f_map',
                'mutation': [
                    {
                        'update': 'a_counter',
                        'mutation': {
                            'increment': 1
                        }
                    }
                ]
            }
        ])

    def test_fail_diff(self):
        with self.assertRaises(TypeError):
            crdt_diff(1, True)

        with self.assertRaises(TypeError):
            crdt_diff('str', 2)

        with self.assertRaises(TypeError):
            crdt_diff([], [])


if __name__ == '__main__':
    main()
