from clitodoapp.widgets.popups import TodoDetailDialog


def test_dialog_works():
    d = TodoDetailDialog("this")
    assert d.get_description() == ""


def test_dialog_set_done():
    d = TodoDetailDialog("this")
    d.set_done(1)
    assert d.get_done_state() == "Finished"
    assert d.get_done() == True
