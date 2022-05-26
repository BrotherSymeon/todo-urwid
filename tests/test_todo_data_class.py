from clitodoapp.models.todo import TodoData
import unittest


class TodoDataTestCase(unittest.TestCase):
    def test_tododata_exists(self):
        t = TodoData(desc="This is my description")
        assert t is not None

    def test_throws_if_id_is_string(self):
        with self.assertRaises(ValueError):
            t = TodoData(id="john")

    def test_throws_if_desc_is_none(self):
        with self.assertRaises(ValueError):
            t = TodoData(desc=None)

    def test_priority_defaults_to_2(self):
        t = TodoData(desc="hello")
        assert t.priority == 2 or TodoData.PRIORITIES.MEDIUM

    def test_blocked_is_false_if_no_reason(self):
        t = TodoData(desc="hello", blocked_reason='')
        assert t.blocked == False
    
    def test_blocked_is_true_if_reason_given(self):
        t = TodoData(desc="hello", blocked_reason='Here is the reason')
        assert t.blocked == True
