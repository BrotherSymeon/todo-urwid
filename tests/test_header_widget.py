import pytest
from clitodoapp.widgets.header import Header


class TestHeader(object):
    def test_can_set_completed(self):
        h = Header("Todo System") 
        h.completed = 9
        assert h.completed == 9
    
    def test_can_set_not_completed(self):
        h = Header("Todo System") 
        h.not_completed = 9
        assert h.not_completed == 9
