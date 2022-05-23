from clitodoapp.models.todo import TodoData
import unittest


class TodoDataTestCase(unittest.TestCase):
    def test_tododata_exists(self):
        t = TodoData(desc="This is my description")
        assert t is not None

    def test_throws_if_id_is_string(self):
        try:
            t = TodoData(id='john')
        except ValueError as e:
            assert type(e) == ValueError

    def test_throws_if_desc_is_none(self):
        error_thown = False
        try:
            t = TodoData(desc=None)
        except ValueError as e:
            error_thown = True
            assert type(e) is ValueError
        assert error_thown is True

    def test_priority_defaults_to_2(self):
        t = TodoData(desc="hello")
        assert t.priority == 2 or TodoData.PRIORITIES.MEDIUM
