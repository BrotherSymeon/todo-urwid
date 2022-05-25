import urwid
import sys
import logging


LOG = logging.getLogger(__name__)


def eprint(*args, **kargs):
    if __name__ == "__main__":
        sys.stderr.flush()
        print(*args, file=sys.stderr, **kargs)
        sys.stderr.flush()
    else:
        LOG.info(*args, **kargs)


class OkDialog(urwid.WidgetWrap):
    signals = ["ok-click"]

    def __init__(self, title="", mesg=[""]):
        t = []
        t.append(title)
        t.extend(mesg)
        self.width = self.maxlength(t) + 8
        self.height = len(mesg) + 7
        # Header
        header_text = urwid.Text(("banner", title), align="center")
        header = urwid.AttrMap(header_text, "banner")

        # Body
        body_text = urwid.Text(mesg, align="center")
        body_filler = urwid.Filler(body_text, valign="top")
        body_padding = urwid.Padding(body_filler, left=1, right=1)
        body = urwid.LineBox(body_padding)

        # Footer
        ok_btn = urwid.Button("Okay")
        urwid.connect_signal(ok_btn, "click", lambda button: self._emit("ok-click"))
        footer = urwid.AttrWrap(ok_btn, "selectable", "focus")
        footer = urwid.GridFlow([footer], 8, 1, 1, "right")

        # Layout
        layout = urwid.Frame(body, header=header, footer=footer, focus_part="footer")

        self.__super.__init__(urwid.LineBox(layout))

    def maxlength(self, mesg_array):
        max = 0
        for i in mesg_array:
            if len(i) > max:
                max = len(i)
        return max


class TodoDetailDialog(urwid.WidgetWrap):
    """A dialog that has controls to create or update a todo"""

    signals = ["close-ok", "close-cancel"]

    def __init__(self, title):
        # the description of the todo
        self.todo_desc = ""
        # done or not this is set when the user clicks the radiobutton
        self.done = False
        # priority of the todo 1, 2 or 3. this is set when the user clicks the radiobutton
        self.priority = 2
        # if its blocked or not. this is set when the user clicks the radiobutton
        self.blocked = False
        # reason for the blockage. this is set when the user clicks the radiobutton
        self.blocked_reason = ""

        try:
            todo_cols = self.todo_colums()
            done_cols = self.done_columns()
            priority_cols = self.priority_columns()
            blocked_cols = self.blocked_columns()
            ok_cancel_cols = self.ok_cancel_columns()
            pile = urwid.Pile(
                [
                    todo_cols,
                    done_cols,
                    priority_cols,
                    blocked_cols,
                    urwid.Text(" "),
                    ok_cancel_cols,
                ]
            )
            pile = self.line_box(pile, title)
            fill = urwid.Filler(pile)

            self.__super.__init__(urwid.AttrWrap(fill, "popbg"))
        except Exception as e:
            LOG.error(e)

    def set_blocked_reason(self, reason):
        self.blocked_reason = reason
        self.blocked_edit.set_edit_text(reason)
        if len(self.blocked_reason) > 0:
            self.blocked = True
        else:
            self.blocked = False

    def get_blocked_reason(self):
        return self.blocked_reason

    def set_priority(self, priority):
        if priority == 1:
            # low
            self.priority = 1
            self.priority_low.set_state(True)
        elif priority == 2:
            # medium
            self.priority = 2
            self.priority_medium.set_state(True)
        elif priority == 3:
            # high
            self.priority = 3
            self.priority_high.set_state(True)
        else:
            raise ValueError("The priority can only be set to 1, 2 or 3")

    def get_priority(self):
        return self.priority

    def set_done(self, done):
        self.ckbx_done.set_state(bool(done))

    def get_done(self):
        return self.ckbx_done.get_state()

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

    def todo_desc_changed(self, widget, data, user_data=None):
        """set the todo_desc"""
        eprint("todo_dec_changed: data = {0}".format(data))
        eprint("todo_dec_changed: user_data = {0}".format(user_data))
        eprint("todo_dec_changed: widget = {0}".format(widget))

        self.todo_desc = data

    def todo_colums(self):
        todo_label = urwid.Text("Todo: ")
        self.todo_edit = urwid.Edit()
        urwid.connect_signal(self.todo_edit, "change", self.todo_desc_changed)
        todo_cols = urwid.Columns(
            [
                (16, todo_label),
                (25, self.todo_edit),
            ]
        )
        return todo_cols

    def ok_cancel_columns(self):
        ok_btn = urwid.Button("Ok")
        cancel_btn = urwid.Button("Cancel")

        self.ok_button = ok_btn
        self.cancel_button = cancel_btn

        urwid.connect_signal(
            self.ok_button, "click", lambda button: self._emit("close-ok")
        )
        urwid.connect_signal(
            self.cancel_button, "click", lambda button: self._emit("close-cancel")
        )

        ok_btn_attr = urwid.AttrMap(ok_btn, None, focus_map="reversed")
        cancel_btn_attr = urwid.AttrMap(cancel_btn, None, focus_map="reversed")

        ok_cancel_cols = urwid.Columns(
            [
                (8, ok_btn_attr),
                (10, cancel_btn_attr),
            ],
            dividechars=2,
            focus_column=None,
            min_width=1,
            box_columns=None,
        )
        ok_cancel_cols = urwid.GridFlow(
            [ok_btn_attr, cancel_btn_attr], 10, 1, 1, "right"
        )
        return ok_cancel_cols

    def done_columns(self):
        done_label = urwid.Text("Done: ")
        self.ckbx_done = urwid.CheckBox("       ", False)
        urwid.connect_signal(self.ckbx_done, "change", self.on_ckbx_done_changed)
        done_cols = urwid.Columns(
            [
                (15, done_label),
                (28, self.ckbx_done),
            ]
        )
        return done_cols

    def on_ckbx_done_changed(self, widget, user_data):
        eprint("on_ckbx_done_changed: user_data = {0}".format(user_data))
        eprint("on_ckbx_done_changed: widget = {0}".format(widget))
        self.done = not widget.state
        eprint("self.done = {0}".format(self.done))

    def priority_columns(self):
        self.priority_group = []
        priority_label = urwid.Text("Priority: ")
        self.priority_high = urwid.RadioButton(self.priority_group, "High")
        self.priority_medium = urwid.RadioButton(self.priority_group, "Medium")
        self.priority_low = urwid.RadioButton(self.priority_group, "Low")
        urwid.connect_signal(
            self.priority_high, "change", self.on_priority_high_clicked
        )
        urwid.connect_signal(
            self.priority_medium, "change", self.on_priority_medium_clicked
        )
        urwid.connect_signal(self.priority_low, "change", self.on_priority_low_clicked)
        priority_cols = urwid.Columns(
            [
                (15, priority_label),
                (10, self.priority_high),
                (12, self.priority_medium),
                (13, self.priority_low),
            ]
        )
        return priority_cols

    def on_priority_high_clicked(self, widget, user_data):
        eprint(
            "on_priority_high_clicked: widget={0} user_data={1}".format(
                widget, user_data
            )
        )
        if widget.state is False:
            self.priority = 1
        eprint("self.priority = {0}".format(self.priority))

    def on_priority_medium_clicked(self, widget, user_data):
        eprint(
            "on_priority_medium_clicked: widget={0} user_data={1}".format(
                widget, user_data
            )
        )
        if widget.state is False:
            self.priority = 2
        eprint("self.priority = {0}".format(self.priority))

    def on_priority_low_clicked(self, widget, user_data):
        eprint(
            "on_done_no_rdbtn_clicked: widget={0} user_data={1}".format(
                widget, user_data
            )
        )
        if widget.state is False:
            self.priority = 3
        eprint("self.priority = {0}".format(self.priority))

    def on_blocked_reason_changed(self, widget, data):
        eprint("on_blocked_reason_changed: data = {0}".format(data))
        eprint("on_blocked_reason_changed: widget = {0}".format(widget))
        self.blocked_reason = data
        if self.blocked_reason == "":
            self.blocked = False
        else:
            self.blocked = True
        eprint("self.blocked_reason = {0}".format(self.blocked_reason))
        eprint("self.blocked = {0}".format(self.blocked))

    def blocked_columns(self):
        blocked_label = urwid.Text("Blocked Reason: ")
        self.blocked_edit = urwid.Edit()
        urwid.connect_signal(
            self.blocked_edit, "change", self.on_blocked_reason_changed
        )
        blocked_cols = urwid.Columns(
            [
                (16, blocked_label),
                (25, self.blocked_edit),
            ]
        )
        return blocked_cols


class TodoDetailLauncher(urwid.PopUpLauncher):
    def __init__(self):
        LOG.info("TodoDetailLauncher: init object")
        self.__super.__init__(urwid.Button(""))
        urwid.connect_signal(
            self.original_widget, "click", lambda button: self.open_pop_up()
        )
        LOG.info("TodoDetailLauncher: init DONE")

    def create_pop_up(self):
        LOG.info("TodoDetailLauncher: create_pop_up called")
        pop_up = TodoDetailDialog("Todo Detail")
        urwid.connect_signal(pop_up, "close-ok", self.on_ok_clicked)
        urwid.connect_signal(pop_up, "close-cancel", self.on_cancel_clicked)
        LOG.info("TodoDetailLauncher: create_pop_up done")
        return pop_up

    def on_cancel_clicked(self, user_data):
        self.close_pop_up()

    def on_ok_clicked(self, user_data):
        self.close_pop_up()

    def get_pop_up_parameters(self):
        LOG.info("TodoDetailLauncher: get_pop_up_parameter called")
        return {"left": -5, "top": 1, "overlay_width": 60, "overlay_height": 8}


class SimpleLayout:
    _palette = [
        ("banner", "black", "light gray"),
        ("selectable", "white", "black"),
        ("focus", "black", "light gray"),
    ]

    def __init__(self):
        self._body = self.body()
        self._loop = urwid.MainLoop(
            self._body, self._palette, unhandled_input=self.handle_keys
        )

    def reset_layout(self, widget):
        self._loop.widget = widget

    def body(self):
        raise Exception("you have to overload this")

    def handle_keys(self, key):
        raise Exception("you have to overload this")

    def start(self):
        self._loop.run()


class OpenOkDialogScreen(SimpleLayout):
    """
    This is just to test out the OkDialog
    """

    def body(self):

        header_label = urwid.Text("Simple Screen", align="center")
        header = urwid.Pile([header_label], focus_item=None)
        head_final_widget = urwid.LineBox(header)

        body = urwid.LineBox(urwid.Padding(urwid.Filler(urwid.Text(""))))

        footer_text = (
            "foot",
            [
                "Simple Footer ",
                ("key", "F8"),
                " quit    ",
                ("key", "o"),
                " open okDialog",
            ],
        )
        footer = urwid.AttrMap(urwid.Text(footer_text), "foot")
        simple_ui = urwid.Frame(
            body, header=head_final_widget, footer=footer, focus_part="body"
        )

        return urwid.Padding(simple_ui, right=0, left=0)

    def on_ok_clicked(self, widget):
        self.reset_layout(self._body)

    def open_ok_dialog(self):
        ok = OkDialog(
            "hello",
            ["This is a line\n", "\n", "and this is a line\n", "\n", "So Cool\n"],
        )

        urwid.connect_signal(ok, "ok-click", self.on_ok_clicked)

        w = urwid.Overlay(
            ok,
            self._body,
            "center",
            ok.width,
            "middle",
            ok.height,
        )

        self._loop.widget = w

    def handle_keys(self, key):
        if key == "f8":
            raise urwid.ExitMainLoop()
        if key == "o":
            self.open_ok_dialog()


def run_ok_dialog_ui():
    OpenOkDialogScreen().start()


def run_todo_detai_ui():
    fill = urwid.Filler(urwid.Padding(TodoDetailLauncher(), "center", 15))
    loop = urwid.MainLoop(fill, [("popbg", "white", "dark blue")], pop_ups=True)
    loop.run()


if __name__ == "__main__":
    menu = [
        "1. Run Todo Detail UI",
        "2. Run OkDialog UI",
    ]
    for i in menu:
        print(i)

    selection = int(input("What now>"))
    if selection == 1:
        run_todo_detai_ui()
    else:
        run_ok_dialog_ui()
