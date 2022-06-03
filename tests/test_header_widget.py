import pytest
from clitodoapp.components.header import Header
from unittest.mock import patch

class TestHeader(object):
    def test_can_set_completed(self, capsys):
        h = Header("Todo System") 
        h.total = 9
        assert h.total == 9
    
    def test_can_set_not_completed(self):
        h = Header("Todo System") 
        h.not_completed = 9
        assert h.not_completed == 9

    def get_rendered_txt(self):
        h = Header("Todo System")
        canvas = h.render((50,))
        return self.get_text(canvas)

    def get_text(self, canvas):
        txt = ''
        for i in canvas.text:
            txt = txt + i.decode()
        return txt


    def test_can_render_caption(self):
        test_text = self.get_rendered_txt()
        assert "Todo System" in test_text

    def test_can_render_total(self):
        h = Header("Todo System")
        h.total = 9
        canvas = h.render((50,))
        txt = self.get_text(canvas)

        assert "Total Todos 9" in txt
        
