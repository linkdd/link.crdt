# -*- coding: utf-8 -*-


class CRDT(object):
    """
    Base class for Convergent, Replicated Data Types
    """

    _type_err_msg = 'Invalid value type'

    @classmethod
    def _check_same_value(cls, a, b):
        return a._value == b._value

    @classmethod
    def _assert_mergeable(cls, a, b):
        if not isinstance(a, cls) or not isinstance(b, cls):
            raise TypeError(
                'Supplied arguments are not {0}'.format(cls.__name__)
            )

        if not cls._check_same_value(a, b):
            raise ValueError(
                'Supplied arguments does not have the same initial value'
            )

    @classmethod
    def merge(cls, a, b, context=None):
        raise NotImplementedError()

    def __init__(self, value=None, context=None):
        if context is not None and not isinstance(context, CRDT):
            raise TypeError(
                'context must be a CRDT, got: {0}'.format(
                    type(context).__name__
                )
            )

        if value is None:
            value = self._default_value()

        self._context = context
        self._vclock = 0

        self._set_value(value)
        self._post_init()

    def _update_vclock(self):
        self._vclock += 1

        if self._context is not None:
            self._context._update_vclock()

    def _post_init(self):
        pass

    @classmethod
    def _match_py_type(cls, pytype):
        return cls._py_type in pytype.mro()

    @classmethod
    def _check_type(cls, value):
        raise NotImplementedError()

    def _assert_type(self, value):
        if not self._check_type(value):
            raise TypeError(self._type_err_msg)

    def _coerce_value(self, value):
        return value

    def _set_value(self, new_value):
        self._assert_type(new_value)
        self._value = self._coerce_value(new_value)

    def _default_value(self):
        raise NotImplementedError()

    def isdirty(self):
        raise NotImplementedError()

    def mutation(self):
        raise NotImplementedError()

    @property
    def current(self):
        raise NotImplementedError()
