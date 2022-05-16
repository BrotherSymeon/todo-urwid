import urwid
import sys
import traceback
import pdb

import logging

from clitodoapp.models.todo import Db, Todos, Todo
from panwid.dialog import *

LOG = logging.getLogger(__name__)


palette = [
    ("reversed", "standout", ""),
    ("foot", "light gray", "dark blue", "bold"),
    ("basic", "yellow", "dark blue"),
    ("b", "black", "dark gray"),
    ("highlight", "black", "light blue"),
    ("bg", "black", "dark blue"),
    ('popbg', 'white', 'dark blue'),
]

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
        return {'left':0, 'top':1, 'overlay_width':78, 'overlay_height':14}



class TodoDetailDialog(urwid.WidgetWrap):
    """A dialog that has controls to create or update a todo """
    signals = ['close-ok', 'close-cancel']
    def __init__(self):
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

        self.ok_button = None

        self.cancel_button = None

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
            ok_cancel_cols
        ])

        fill = urwid.Filler(pile)

        self.__super.__init__(urwid.AttrWrap(fill, 'popbg'))

    def todo_desc_changed(self, user_data):
        """ set the todo_desc"""
        self.todo_desc = user_data


    def todo_colums(self):
        todo_label = urwid.Text(u"Todo: ")
        todo_edit = urwid.Edit()
        urwid.connect_signal(todo_edit, 'change', self.todo_desc_changed)
        todo_cols = urwid.Columns(
            [
                todo_label,
                todo_edit,
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
        return ok_cancel_cols

    def done_columns(self):
        done_label = urwid.Text(u"Done: ")
        done_group = []
        done_yes = urwid.RadioButton(done_group, u"Finished")
        done_no = urwid.RadioButton(done_group, u"Unfinished")
        urwid.connect_signal(
                done_yes,
                'change',
                self.on_done_yes_rdbtn_clicked
        )
        urwid.connect_signal(
                done_no,
                'change',
                self.on_done_no_rdbtn_clicked
        )
        done_cols = urwid.Columns([
            done_label,
            done_yes,
            done_no,
        ])
        return done_cols

    def on_done_yes_rdbtn_clicked(self, user_data):
        self.done = True

    def on_done_no_rdbtn_clicked(self, user_data):
        self.done = False

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
            priority_label,
            urwid.Text(u" "),
            priority_high,
            priority_medium,
            priority_low,
        ])
        return priority_cols


    def on_priority_high_clicked(self, user_data):
        self.priority = 1

    def on_priority_medium_clicked(self, user_data):
        self.priority = 2


    def on_priority_low_clicked(self, user_data):
        self.priority = 3

    def on_blocked_reason_changed(self, user_data):
        self.blocked_reason = user_data
        if self.blocked_reason == '':
            self.blocked = False
        else:
            self.blocked = True


    def blocked_columns(self):
        blocked_label = urwid.Text(u"Blocked Reason: ")
        blocked_edit = urwid.Edit()
        blocked_cols = urwid.Columns(
            [
                blocked_label,
                urwid.Text(u" "),
                blocked_edit,
            ]
        )
        return blocked_cols

class TodoUI:
    def __init__(self, todos):
        self.Todos = todos
        self.filter_group = []
        self.filter = "NOT DONE"
        self.detail_launcher = None

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

    def input_name(self, button, name_field):
        name = name_field.get_edit_text().rstrip()
        if len(name) > 0:
            LOG.info("Adding new todo: {0}".format(name))
            todo = self.Todos.new(name)
            LOG.info("New todo was added to Db: {0}".format(str(todo)))
        self.initialize_list_ui()

    def edit_todo_desc(self, button, user_data):
        # breakpoint()
        desc_field = user_data[0]
        desc = desc_field.get_edit_text().rstrip()
        if len(desc) > 0:
            todo = self.Todos.get_by_id(user_data[1])
            todo.todo = desc
            self.Todos.save(todo)
        self.initialize_list_ui()

    def initialize_list_ui(self):
        self.top = self.todo_list_ui()
        LOG.info("in initialize_list self.top = {0}".format(self.top))
        LOG.info("in initialize_list self.top.original_widget = {0}".format(self.top.original_widget))

    def on_init_list(self, t, e):
        self.initialize_list_ui()

    def delete_todo(self, widget, user_data):
        LOG.info("deleting todo with if {0}".format(user_data[0]))
        todo = self.Todos.get_by_id(user_data[0])
        self.Todos.delete(todo)
        del self.top.original_widget.body.original_widget.widget_list[4].body[user_data[1]]
        #self.initialize_list_ui()

    def open_detail_popup():
        pass

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
                return todo.todo
            pass

        try:

            title = "Edit Todo"

            if user_data[0] == "new":
                title = "New Todo"

            txt_box = urwid.Text(title)
            txt_box = urwid.Padding(txt_box, align="center", left=18, right=0)
            txt = self.line_box(txt_box)
            name_field = urwid.Edit(
                caption="",
                edit_text=get_edit_text(),
                multiline=False,
                align="left",
                wrap="space",
                allow_tab=False,
                edit_pos=None,
                layout=None,
                mask=None,
            )
            btn = urwid.Button(" OK", user_data=None)
            btn_cancel = urwid.Button("Cancel", user_data=None)
            div = urwid.Divider("─", bottom=2)
            ok_btn_attr = urwid.AttrMap(btn, None, focus_map="reversed")
            cancel_btn_attr = urwid.AttrMap(btn_cancel, None, focus_map="reversed")

            cols = urwid.Columns(
                [
                    (8, ok_btn_attr),
                    (10, cancel_btn_attr),
                ],
                dividechars=2,
                focus_column=None,
                min_width=1,
                box_columns=None,
            )
            name_button = urwid.Padding(cols, align="center", width="pack", left=25)
            if user_data[0] == "new":
                urwid.connect_signal(btn, "click", self.input_name, name_field)
            else:
                urwid.connect_signal(
                    btn, "click", self.edit_todo_desc, (name_field, user_data[1])
                )

            urwid.connect_signal(btn_cancel, "click", self.on_init_list, name_field)
            wid = urwid.Pile([txt, name_field, div, name_button])
            new = urwid.AttrMap(wid, None, focus_map="")
            background = urwid.AttrMap(urwid.SolidFill(" "), "basic")
            interior = urwid.Filler(new)
            window = self.line_box(interior)
            topw = urwid.Overlay(window, background, "center", 50, "middle", 10)

        except Exception as e:
            traceback.print_exc(file=sys.stdout)

        self.top.original_widget = urwid.Padding(topw, right=0, left=0)

    def filter_changed(self, widget, state):
        LOG.info("filter changed")
        # breakpoint()
        if state:
            LOG.info("changed filter to {0}".format(widget.label.upper()))
            self.filter = widget.label.upper()
            self.load_filtered_todos()
            #self.initialize_list_ui()
            #self.set_filter_buttons()

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
                    ('weight', 1, self.filter_not_done),
                    ('weight', 1, self.filter_done),
                    ('weight', 1, self.filter_all),
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
        # breakpoint()
        todo = user_data[0]
        todo.done = new_state
        self.Todos.save(todo)
        self.initialize_list_ui()
        #self.set_filter_buttons()

    def load_employees(self):
        print("loading employees")

    def draw_ui(self):

        self.top = self.todo_list_ui()
        LOG.info('self.top = {0} '.format(self.top))
        return self.top

    def row_items(self, todo_list):
        retList = []
        index = 0
        self.detail_launcher = TodoDetailLauncher()
        for todo in todo_list:
            idCol = ('fixed',4, urwid.Text(str(todo.id), align="left"))
            doneCol = (
                'fixed',
                6,
                urwid.CheckBox(
                    "",
                    state=bool(todo.done),
                    on_state_change=self.update_todo_done,
                    user_data=(todo,),
                ),
            )
            todoCol = ("weight", 4, urwid.Text(todo.todo, align="left"))
            editBtnCol = urwid.Button(
                "Edit", self.todo_detail_screen, ("edit", todo.id)
            )
            delBtnCol = urwid.Button("Delete", self.delete_todo, (todo.id, index))
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
            retList.append(row)
            index += 1
        
        last_row = urwid.Columns([
               urwid.Padding(urwid.Text("")),
               urwid.Padding(urwid.Text("")),
               urwid.Padding(urwid.Text("")),
               urwid.Padding(self.detail_launcher),
            ])
        retList.append(last_row)
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
        todo_list = self.get_filtered_todos()
        self.update_todo_count(len(todo_list))
        nocomp_todos = [t for t in todo_list if bool(t.done) == False]
        self.update_non_comp_count(len(nocomp_todos))

    def load_filtered_todos(self):
        LOG.info("Loading filtered todos")
        todo_list = self.get_filtered_todos()
        row_items = self.row_items(todo_list)
        self.top.original_widget.body.original_widget.widget_list[4].body = row_items
        LOG.info(self.top.original_widget.body.original_widget.widget_list)
        #self.list_walker = urwid.SimpleFocusListWalker(self.row_items(todo_list))

    def todo_list_ui(self):
        # breakpoint()
        self.header = self.header_widget()
        todo_list = self.get_filtered_todos()
        self.update_todo_count(len(todo_list))
        nocomp_todos = [t for t in todo_list if bool(t.done) == False]
        self.update_non_comp_count(len(nocomp_todos))
        # making the list
        self.list_walker = urwid.SimpleFocusListWalker(self.row_items(todo_list))
        #breakpoint()
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
        if key == "o":
            #breakpoint()
            self.detail_launcher.keypress((15,), 'enter')
        

        key_dict = {"l": self.load_employees, "n": self.todo_detail_screen}

        try:
            key_dict[key]()
        except:
            pass


if __name__ == "__main__":

    screen = urwid.raw_display.Screen()
    # screen.set_terminal_properties(1<<24)
    screen.set_terminal_properties(256)

    NORMAL_FG_MONO = "white"
    NORMAL_FG_16 = "light gray"
    NORMAL_BG_16 = "black"
    NORMAL_FG_256 = "light gray"
    NORMAL_BG_256 = "g0"

    todos = Todos("todo.db")
    todo_ui = TodoUI(todos)
    ui = todo_ui.draw_ui()
    loop = urwid.MainLoop(
        ui, palette, screen=screen, unhandled_input=todo_ui.handle_keys
    )
    loop.run()
