import urwid
import sys
import traceback
import pdb

import logging

from clitodoapp.models.todo import Todos, TodoData
from clitodoapp.widgets.popups import TodoDetailDialog, OkDialog
from clitodoapp.widgets.square_button import SquareButton
from panwid.dialog import *

LOG = logging.getLogger(__name__)


palette = [
    ("reversed", "standout", ""),
    ("foot", "light gray", "dark blue", "bold"),
    ("basic", "yellow", "dark blue"),
    ("b", "black", "dark gray"),
    ("highlight", "black", "light blue"),
    ("bg", "black", "dark blue"),
    ("popbg", "white", "dark blue"),
]


class TodoUI:
    """Our main view"""

    palette = [
        ("reversed", "standout", ""),
        ("foot", "light gray", "dark blue", "bold"),
        ("basic", "yellow", "dark blue"),
        ("b", "black", "dark gray"),
        ("highlight", "black", "light blue"),
        ("bg", "black", "dark blue"),
        ("popbg", "light gray", "default"),
    ]

    def __init__(self, todos):
        self.Todos = todos
        self.filter_group = []
        self.filter = "NOT DONE"
        self._body = self.todo_list_ui()
        self.update_header_counts()
        self._loop = urwid.MainLoop(
            self._body, self.palette, unhandled_input=self.handle_keys
        )

    def start(self):
        """starts the main loop for the view"""
        self._loop.run()

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

    def delete_todo(self, widget, user_data):
        LOG.debug("deleting todo with id {0}".format(user_data[0]))
        try:
            done = self.Todos.delete_by_id(user_data[0])
            if done:
                self.load_filtered_todos()
            else:
                LOG.info("The todo was not deleted from the database")
                self.ok_dialog(
                    "Warning.",
                    [
                        "The todo was not deleted from the database\n",
                        "Please contact you system Administrator",
                    ],
                )
        except Exception as e:
            LOG.error(e)

    def on_edit_dialog_ok_clicked(self, widget, user_args, todo_id=0):
        mesg = "on_edit_dialog_ok_clicked user_args={0}, widget={1}, todo_id={2}"
        LOG.debug(mesg.format(user_args, widget, todo_id))
        try:
            breakpoint()
            work_done = False
            if len(user_args) == 1:
                LOG.info("on_edit_dialog_ok_cliked: This is a new todo")
                # this is a new todo
                if len(widget.get_description()) > 0:
                    t = TodoData(desc=widget.get_description())
                    t.done = int(widget.get_done())
                    self.Todos.save(t)
                    work_done = True

            else:
                # this is an existing todo and we are editing it
                LOG.info("on_edit_dialog_ok_cliked: This is an existing todo")
                if len(widget.get_description()) > 0:
                    t = self.Todos.get_by_id(user_args[1])
                    t.desc = widget.get_description()
                    t.done = int(widget.get_done())
                    self.Todos.save(t)
                    work_done = True

            self.reset_layout(self._body)
            if work_done:
                self.load_filtered_todos()
                self.ok_dialog(
                    "Congratulations!!",
                    ["You have sucessfully edited\n", "your first todo item"],
                )

        except Exception as e:
            LOG.error(e)
            self.ok_dialog("Error", ["Please contact you administrator"])

    def on_edit_dialog_cancel_clicked(self, widget, user_args, todo_id=0):
        LOG.info(
            "on_edit_dialog_cancel_clicked args={0}".format(
                (widget, user_args, todo_id)
            )
        )
        self.reset_layout(self._body)

    def reset_layout(self, widget):
        self._loop.widget = widget

    def on_ok_clicked(self, widget):
        self.reset_layout(self._body)

    def ok_dialog(self, title="", mesg=[""]):
        ok = OkDialog(title, mesg)

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

    def todo_detail_screen(self, widget=None, user_data=("new",)):
        """
        pops up a screen to create or edit a todo
        :type {new|edit}
        defaults to new but edit will make it an edit screen
        """

        def get_edit_text():
            if len(user_data) == 1:
                return ""
            else:
                todo = self.Todos.get_by_id(user_data[1])
                return todo.desc
            pass

        try:
            todo = None
            if len(user_data) > 1:
                todo = self.Todos.get_by_id(user_data[1])

            title = "Edit Todo"

            if user_data[0] == "new":
                title = "New Todo"

            self.edit_dialog = TodoDetailDialog(title)

            if todo:
                self.edit_dialog.set_done(todo.done)
                self.edit_dialog.set_description(todo.desc)
            # hook up the close-ok and close-cancel events
            urwid.connect_signal(
                self.edit_dialog, "close-ok", self.on_edit_dialog_ok_clicked, user_data
            )
            urwid.connect_signal(
                self.edit_dialog,
                "close-cancel",
                self.on_edit_dialog_cancel_clicked,
                user_data,
            )

            w = urwid.Overlay(self.edit_dialog, self._body, "center", 60, "middle", 8)
            self._loop.widget = w

        except Exception as e:
            LOG.error(e)

    def filter_changed(self, widget, state):
        LOG.info("filter changed")
        # breakpoint()
        if state:
            LOG.info("changed filter to {0}".format(widget.label.upper()))
            self.filter = widget.label.upper()
            self.load_filtered_todos()
            # self.initialize_list_ui()
            # self.set_filter_buttons()

    def filter_widget(self):
        # breakpoint()
        try:
            self.filter_all = urwid.RadioButton(
                self.filter_group,
                "All",
                bool(self.filter == "ALL"),
                on_state_change=self.filter_changed,
            )
            self.filter_done = urwid.RadioButton(
                self.filter_group,
                "Done",
                bool(self.filter == "DONE"),
                on_state_change=self.filter_changed,
            )
            self.filter_not_done = urwid.RadioButton(
                self.filter_group,
                "Not Done",
                bool(self.filter == "NOT DONE"),
                on_state_change=self.filter_changed,
            )
            self.set_filter_buttons()
            cols = urwid.Columns(
                [
                    ("weight", 1, self.filter_not_done),
                    ("weight", 1, self.filter_done),
                    ("weight", 1, self.filter_all),
                ],
                dividechars=0,
                focus_column=None,
                min_width=1,
                box_columns=None,
            )
            widget = urwid.Pile([cols], focus_item=None)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
        return widget

    def header_widget(self):
        self.todos_count_label = urwid.Text("Total Todos", align="left")
        self.todos_count_display = urwid.Text("0", align="left")
        self.nocomp_count_label = urwid.Text("Todos Not Completed", align="right")
        self.nocomp_count_display = urwid.Text("0", align="right")
        cols = urwid.Columns(
            [
                (12, self.todos_count_label),
                ("weight", 5, self.todos_count_display),
                # (24, urwid.Text("│")),
                (19, self.nocomp_count_label),
                (3, self.nocomp_count_display),
            ],
            dividechars=0,
            focus_column=None,
            min_width=1,
            box_columns=None,
        )
        # cols.pack((1, 1))
        header = urwid.Pile([cols], focus_item=None)
        head_final_widget = self.line_box(header, "Todo System")

        return head_final_widget

    def update_todo_count(self, count):
        self.todos_count_display.set_text(str(count))

    def update_non_comp_count(self, count):
        self.nocomp_count_display.set_text(str(count))

    def set_filter_buttons(self):
        # breakpoint()
        if self.filter == "ALL":
            self.filter_all.set_state(True, do_callback=True)
        elif self.filter == "DONE":
            self.filter_done.set_state(True, do_callback=True)
        elif self.filter == "NOT ALL":
            self.filter_not_done.set_state(True, do_callback=True)

    def update_todo_done(self, widget, new_state, user_data):
        todo = user_data[0]
        todo.done = new_state
        self.Todos.save(todo)
        self.load_filtered_todos()

    def load_employees(self):
        print("loading employees")

    def row_item(self, todo, index):
        idCol = ("fixed", 4, urwid.Text(str(todo.id), align="left"))
        doneCol = (
            "fixed",
            6,
            urwid.CheckBox(
                "",
                state=bool(todo.done),
                on_state_change=self.update_todo_done,
                user_data=(todo,),
            ),
        )
        todoCol = ("weight", 4, urwid.Text(todo.desc, align="left"))
        editBtnCol = SquareButton(
            "Edit", self.todo_detail_screen, ("edit", todo.id, index)
        )
        delBtnCol = SquareButton("Delete", self.delete_todo, (todo.id, index))
        edit_btn_attr = urwid.AttrMap(editBtnCol, None, focus_map="reversed")
        del_btn_attr = urwid.AttrMap(delBtnCol, None, focus_map="reversed")
        cols = urwid.Columns(
            [
                ("fixed", 8, edit_btn_attr),
                ("fixed", 10, del_btn_attr),
            ],
            dividechars=1,
            focus_column=None,
            min_width=1,
            box_columns=None,
        )
        # breakpoint()
        todo_buttons = urwid.Padding(cols, align="right", width="pack")
        row = urwid.Columns(
            [
                idCol,
                doneCol,
                todoCol,
                todo_buttons,
            ]
        )

        return row

    def row_items(self, todo_list):
        retList = []
        index = 0
        for todo in todo_list:
            row = self.row_item(todo, index)
            retList.append(row)
            index += 1

        return retList

    def get_filtered_todos(self):
        if self.filter == "ALL":
            todo_list = self.Todos.get_all()
        elif self.filter == "DONE":
            todo_list = self.Todos.get_done()
        elif self.filter == "NOT DONE":
            todo_list = self.Todos.get_not_done()
        return todo_list

    def update_header_counts(self):
        todo_list = self.Todos.get_all()
        self.update_todo_count(len(todo_list))
        nocomp_todos = [t for t in todo_list if bool(t.done) == False]
        self.update_non_comp_count(len(nocomp_todos))

    def load_filtered_todos(self):
        LOG.info("Loading filtered todos")
        todo_list = self.get_filtered_todos()
        row_items = self.row_items(todo_list)
        self.list_box.body = row_items
        self.update_header_counts()
        # breakpoint()

    def todo_list_ui(self):
        """
        creates the initial view
        """
        LOG.info("createing initial view in todo_list_ui")
        # this should be daone after the view is built
        todo_list = self.get_filtered_todos()

        self.header = self.header_widget()

        # making the list
        self.list_walker = urwid.SimpleFocusListWalker(self.row_items(todo_list))

        # breakpoint()
        list_heading = urwid.Columns(
            [
                (5, urwid.Text("Id", align="left")),
                (7, urwid.Text("Done", align="left")),
                ("pack", urwid.Text("Todo", align="left")),
            ],
            dividechars=0,
            focus_column=None,
            min_width=1,
            box_columns=None,
        )
        self.list_box = urwid.ListBox(self.list_walker)
        self.list_pile = urwid.Pile(
            [
                (1, urwid.Filler(self.filter_widget())),
                (1, urwid.Filler(urwid.Divider("─"))),
                (
                    1,
                    urwid.Filler(
                        list_heading,
                        valign="top",
                        height="pack",
                        min_height=None,
                        top=0,
                        bottom=0,
                    ),
                ),
                (1, urwid.Filler(urwid.Divider("─"))),
                self.list_box,
            ],
            focus_item=2,
        )

        self.body = self.line_box(self.list_pile)

        footer_text = (
            "foot",
            [
                "Todo System    ",
                ("key", "F8"),
                " quit    ",
                ("key", "N"),
                " new todo",
            ],
        )
        self.footer = urwid.AttrMap(urwid.Text(footer_text), "foot")
        todo_ui = urwid.Frame(
            self.body, header=self.header, footer=self.footer, focus_part="body"
        )

        return urwid.Padding(todo_ui, right=0, left=0)

    def handle_keys(self, key):
        if key == "q":
            raise urwid.ExitMainLoop()
        if key == "f8":
            raise urwid.ExitMainLoop()

        key_dict = {"l": self.load_employees, "n": self.todo_detail_screen}

        try:
            key_dict[key]()
        except:
            pass


if __name__ == "__main__":

    screen = urwid.raw_display.Screen()
    # screen.set_terminal_properties(1<<24)
    screen.set_terminal_properties(16)

    NORMAL_FG_MONO = "white"
    NORMAL_FG_16 = "light gray"
    NORMAL_BG_16 = "black"
    NORMAL_FG_256 = "light gray"
    NORMAL_BG_256 = "g0"

    todos = Todos("todo.db")
    TodoUI(todos).start()
