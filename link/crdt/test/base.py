# -*- coding: utf-8 -*-

from unittest import TestCase
from six import PY2, PY3


class UTCase(TestCase):
    def assertItemsEqual(self, a, b):
        if PY2:
            return super(UTCase, self).assertItemsEqual(a, b)

        elif PY3:
            return self.assertCountEqual(a, b)
