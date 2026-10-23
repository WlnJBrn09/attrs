# SPDX-License-Identifier: MIT

"""
Tests for compatibility against other Python modules.
"""

import pytest

from hypothesis import given

import attr

from .strategies import simple_classes


cloudpickle = pytest.importorskip("cloudpickle")


class TestCloudpickleCompat:
    """
    Tests for compatibility with ``cloudpickle``.
    """

    @given(simple_classes(cached_property=False))
    def test_repr(self, cls):
        """
        attrs instances can be pickled and un-pickled with cloudpickle.
        """
        inst = cls()
        # Exact values aren't a concern so long as neither direction
        # raises an exception.
        pkl = cloudpickle.dumps(inst)
        cloudpickle.loads(pkl)

    def test_hash_key(self):
        """
        A field hash key survives cloudpickle and still hashes the key value.
        """

        @attr.define(frozen=True)
        class C:
            x = attr.field(hash=tuple)

        inst = C([1, 2])
        restored = cloudpickle.loads(cloudpickle.dumps(inst))

        assert hash(inst) == hash(restored)
        assert tuple is attr.fields(type(restored)).x.hash_key
