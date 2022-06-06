import pytest
from clitodoapp.components.filter import Filter
from unittest.mock import patch

class TestFilter(object):
    def test_filter(self):
        f = Filter(Filter.filters.ALL)
        assert f is not None

    def test_filter_sets_rb_all(self):
        f = Filter(Filter.filters.ALL)
        assert f.filter_all.state is True

    def test_filter_sets_rb_done(self):
        f = Filter(Filter.filters.DONE)
        assert f.filter_done.state is True

    def test_filter_sets_rb_not_done(self):
        f = Filter(Filter.filters.NOT_DONE)
        assert f.filter_not_done.state is True
