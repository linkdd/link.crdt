# -*- coding: utf-8 -*-

from link.crdt.test.base import UTCase
from unittest import main

from link.crdt.map import Map


class TestMap(UTCase):
    def test_enable(self):
        expected = {
            'a_counter': 5,
            'b_flag': False,
            'c_register': 'test',
            'd_set': {'1', '2'},
            'e_map': {
                'a_counter': 5
            }
        }
        crdt = Map(value=expected)

        self.assertEqual(crdt.current, expected)

        crdt['a_counter'].increment(3)
        crdt['b_flag'].enable()
        crdt['c_register'].assign('test2')
        crdt['d_set'].add('3')
        del crdt['e_map']
        crdt['e_register'].assign('test')

        expected = {
            'a_counter': 8,
            'b_flag': True,
            'c_register': 'test2',
            'd_set': {'1', '2', '3'},
            'e_register': 'test'
        }

        self.assertEqual(crdt.current, expected)
        self.assertIn('a_counter', crdt._value)
        self.assertIn('b_flag', crdt._value)
        self.assertIn('c_register', crdt._value)
        self.assertIn('d_set', crdt._value)
        self.assertIn('e_register', crdt._updates)
        self.assertEqual(crdt._vclock, 7)
        self.assertTrue(crdt.isdirty())
        self.assertItemsEqual(crdt.mutation(), [
            {'remove': 'e_map'},
            {
                'update': 'a_counter',
                'mutation': {
                    'increment': 3
                }
            },
            {
                'update': 'b_flag',
                'mutation': {
                    'enable': None
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
                    'adds': {'3'},
                    'removes': set()
                }
            },
            {
                'update': 'e_register',
                'mutation': {
                    'assign': 'test'
                }
            }
        ])

    def test_merge(self):
        a = Map(value={'a_counter': 5})
        b = Map(value={'a_counter': 5})

        a['a_counter'].increment(3)
        b['a_counter'].increment(3)
        b['a_counter'].decrement(2)

        c = Map.merge(a, b)

        self.assertEqual(c.current, {'a_counter': 9})
        self.assertIn('a_counter', c._updates)
        self.assertEqual(c._vclock, 3)
        self.assertTrue(c.isdirty())
        self.assertEqual(c.mutation(), [
            {
                'update': 'a_counter',
                'mutation': {
                    'increment': 4
                }
            }
        ])

    def test_fail_merge(self):
        a = Map(value={'a_counter': 5})
        b = Map(value={'b_counter': 5})

        with self.assertRaises(ValueError):
            Map.merge(a, b)

    def test_fail_type(self):
        with self.assertRaises(TypeError):
            not_dict = 42
            Map(value=not_dict)

        with self.assertRaises(TypeError):
            Map(value={'a_counter': 'not int'})


if __name__ == '__main__':
    main()
