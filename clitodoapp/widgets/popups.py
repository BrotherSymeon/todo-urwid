
import urwid
import sys
import traceback
import pdb

import logging
import sys

LOG = logging.getLogger(__name__)


def eprint(*args, **kargs):
    if __name__ == "__main__":
        sys.stderr.flush()
        print(*args, file=sys.stderr, **kargs)
        sys.stderr.flush()
    else:
        LOG.info(*args, **kargs)

class TodoDetailDialog(urwid.WidgetWrap):
    """A dialog that has controls to create or update a todo """
    signals = ['close-ok', 'close-cancel']
    def __init__(self, title):
        # the description of the todo
        self.todo_desc = ''
        # done or not this is set when the user clicks the radiobutton
        self.done = False
        # priority of the todo 1, 2 or 3. this is set when the user clicks the radiobutton
        self.priority = 0
        # if its blocked or not. this is set when the user clicks the radiobutton
        self.blocked = False
        # reason for the blockage. this is set when the user clicks the radiobutton
        self.blocked_reason = ''

        try:
            todo_cols = self.todo_colums()
            done_cols = self.done_columns()
            priority_cols = self.priority_columns()
            blocked_cols = self.blocked_columns()
            ok_cancel_cols = self.ok_cancel_columns()
            pile = urwid.Pile([
                todo_cols,
                done_cols,
                priority_cols,
                blocked_cols,
                urwid.Text(" "),
                ok_cancel_cols
            ])
            pile = self.line_box(pile, title)
            fill = urwid.Filler(pile)

            self.__super.__init__(urwid.AttrWrap(fill, 'popbg'))
        except Exception as e:
            LOG.error(e)

    def set_done(self, done):
        if bool(done):
            self.done_yes.set_state(True)
            self.done_no.set_state(False)
        else:
            self.done_yes.set_state(False)
            self.done_no.set_state(True)
    def get_done_state(self):
        for l in  self.done_group:
            if l.state == True:
                return l.label

    def get_done(self):
        if self.get_done_state() == "Finished":
            return True
        else:
            return False


    def set_description(self, desc):
        self.todo_edit.set_edit_text(desc)
        self.todo_desc = desc

    def get_description(self):
        return self.todo_edit.get_edit_text()

    def line_box(self, widget, caption="", align_title="center"):
            return urwid.LineBox(
                widget,
                title=caption,
                title_align=align_title,
                tlcorner="┌",
                tline="─",
                lline="│",
                trcorner="┐",
                blcorner="└",
                rline="│",
                bline="─",
                brcorner="┘",
            )


    def todo_desc_changed(self, widget,  data,  user_data=None):
        """ set the todo_desc"""
        eprint('todo_dec_changed: data = {0}'.format(data))
        eprint('todo_dec_changed: user_data = {0}'.format(user_data))
        eprint('todo_dec_changed: widget = {0}'.format(widget))

        self.todo_desc = data


    def todo_colums(self):
        todo_label = urwid.Text(u"Todo: ")
        self.todo_edit = urwid.Edit()
        urwid.connect_signal(self.todo_edit, 'change', self.todo_desc_changed)
        todo_cols = urwid.Columns(
            [
                (16, todo_label),
                (25, self.todo_edit),
            ]
        )
        return todo_cols


    def ok_cancel_columns(self):
        ok_btn = urwid.Button(u"Ok")
        cancel_btn = urwid.Button(u"Cancel")

        self.ok_button = ok_btn
        self.cancel_button = cancel_btn

        urwid.connect_signal(
                self.ok_button,
                'click',
                lambda button:self._emit('close-ok')
            )
        urwid.connect_signal(
                self.cancel_button,
                'click',
                lambda button:self._emit('close-cancel')
            )
 
        ok_btn_attr = urwid.AttrMap(ok_btn, None, focus_map='reversed')
        cancel_btn_attr = urwid.AttrMap(cancel_btn, None, focus_map='reversed')

        ok_cancel_cols = urwid.Columns([
                (8, ok_btn_attr),
                (10, cancel_btn_attr),
            ],
            dividechars=2,
            focus_column=None,
            min_width=1,
            box_columns=None,
        )
        ok_cancel_cols = urwid.GridFlow([ok_btn_attr,cancel_btn_attr], 10, 1, 1, "right")
        return ok_cancel_cols

    def done_columns(self):
        done_label = urwid.Text(u"Done: ")
        self.done_group = []
        self.done_yes = urwid.RadioButton(self.done_group, u"Finished")
        self.done_no = urwid.RadioButton(self.done_group, u"Unfinished")
        urwid.connect_signal(
                self.done_yes,
                'change',
                self.on_done_yes_rdbtn_clicked
        )
        urwid.connect_signal(
                self.done_no,
                'change',
                self.on_done_no_rdbtn_clicked
        )
        done_cols = urwid.Columns([
            (15, done_label),
            (14, self.done_yes),
            (14, self.done_no),
        ])
        return done_cols

    def on_done_yes_rdbtn_clicked(self, widget, user_data):
        #eprint('on_done_yes_rdbtn_clicked: data = {0}'.format(data))
        eprint('on_done_yes_rdbtn_clicked: user_data = {0}'.format(user_data))
        eprint('on_done_yes_rdbtn_clicked: widget = {0}'.format(widget))
        self.done = not widget.state
        eprint('self.done = {0}'.format(self.done))

    def on_done_no_rdbtn_clicked(self, widget, user_data):
        #eprint('on_done_no_rdbtn_clicked: data = {0}'.format(data))
        eprint('on_done_no_rdbtn_clicked: user_data = {0}'.format(user_data))
        eprint('on_done_no_rdbtn_clicked: widget = {0}'.format(widget))
        self.done = widget.state
        eprint('self.done = {0}'.format(self.done))

    def priority_columns(self):
        priority_group = []
        priority_label = urwid.Text(u"Priority: ")
        priority_high = urwid.RadioButton(priority_group, u"High")
        priority_medium = urwid.RadioButton(priority_group, u"Medium")
        priority_low = urwid.RadioButton(priority_group, u"Low")
        urwid.connect_signal(
                priority_high,
                'change',
                self.on_priority_high_clicked
            )
        urwid.connect_signal(
                priority_medium,
                'change',
                self.on_priority_medium_clicked
            )
        urwid.connect_signal(
                priority_low,
                'change',
                self.on_priority_low_clicked
            )
        priority_cols = urwid.Columns([
            (15, priority_label),
            (10,priority_high),
            (12,priority_medium),
            (13,priority_low),
        ])
        return priority_cols


    def on_priority_high_clicked(self, widget, user_data):
        eprint('on_done_no_rdbtn_clicked: user_data = {0}'.format(user_data))
        eprint('on_done_no_rdbtn_clicked: widget = {0}'.format(widget))
        if widget.state is False:
            self.priority = 1
        eprint('self.priority = {0}'.format(self.priority))

    def on_priority_medium_clicked(self, widget, user_data):
        eprint('on_done_no_rdbtn_clicked: user_data = {0}'.format(user_data))
        eprint('on_done_no_rdbtn_clicked: widget = {0}'.format(widget))
        if widget.state is False:
            self.priority = 2
        eprint('self.priority = {0}'.format(self.priority))


    def on_priority_low_clicked(self, widget, user_data):
        eprint('on_done_no_rdbtn_clicked: user_data = {0}'.format(user_data))
        eprint('on_done_no_rdbtn_clicked: widget = {0}'.format(widget))
        if widget.state is False:
            self.priority = 3
        eprint('self.priority = {0}'.format(self.priority))

    def on_blocked_reason_changed(self, widget, data):
        eprint('on_blocked_reason_changed: data = {0}'.format(data))
        eprint('on_blocked_reason_changed: widget = {0}'.format(widget))
        self.blocked_reason = data
        if self.blocked_reason == '':
            self.blocked = False
        else:
            self.blocked = True
        eprint('self.blocked_reason = {0}'.format(self.blocked_reason))
        eprint('self.blocked = {0}'.format(self.blocked))


    def blocked_columns(self):
        blocked_label = urwid.Text(u"Blocked Reason: ")
        blocked_edit = urwid.Edit()
        urwid.connect_signal(blocked_edit, 'change', self.on_blocked_reason_changed)
        blocked_cols = urwid.Columns(
            [
                (16,blocked_label),
                (25, blocked_edit),
            ]
        )
        return blocked_cols



class TodoDetailLauncher(urwid.PopUpLauncher):
    def __init__(self):
        LOG.info("TodoDetailLauncher: init object")
        self.__super.__init__(urwid.Button(""))
        urwid.connect_signal(
                self.original_widget,
                'click',
                lambda button: self.open_pop_up()
        )
        LOG.info("TodoDetailLauncher: init DONE")


    def create_pop_up(self):
        LOG.info("TodoDetailLauncher: create_pop_up called")
        pop_up = TodoDetailDialog()
        urwid.connect_signal(
            pop_up,
            'close-ok',
            self.on_ok_clicked
        )
        urwid.connect_signal(
            pop_up,
            'close-cancel',
            self.on_cancel_clicked
        )
        LOG.info("TodoDetailLauncher: create_pop_up done")
        return pop_up

    def on_cancel_clicked(self, user_data):
        self.close_pop_up()

    def on_ok_clicked(self, user_data):
        self.close_pop_up()


    def get_pop_up_parameters(self):
        LOG.info("TodoDetailLauncher: get_pop_up_parameter called")
        return {'left':-5, 'top':1, 'overlay_width':60, 'overlay_height':8}




if __name__ == "__main__":
    fill = urwid.Filler(urwid.Padding(TodoDetailLauncher(),'center', 15))
    loop = urwid.MainLoop(
            fill,
            [('popbg', 'white', 'dark blue')],
            pop_ups=True
        )
    loop.run()
