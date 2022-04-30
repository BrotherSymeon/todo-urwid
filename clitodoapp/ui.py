import urwid
import sys
import traceback 
import pdb


from clitodoapp.models.todo import Db, Todos, Todo


palette = [
    ("reversed", "standout", ""),
    ("basic", "yellow","dark blue"),
    ("b", "black", "dark gray"),
    ("highlight", "black", "light blue"),
    ("bg", "black", "dark blue"),
]


class TodoUI:
    def __init__(self, todos):
        self.Todos = todos
        pass
    
    def line_box(self, widget, caption='', align_title='center'):
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
        todo = self.Todos.new(name)
        self.initialize_list_ui()

    def initialize_list_ui(self):
        self.top.original_widget = self.employee_list_ui()

    def on_init_list(self, t, e ):
        self.initialize_list_ui()

    def new_todo_screen(self):

        try:
            txt_box = urwid.Text("New Todo")
            txt_box = urwid.Padding(txt_box, align='center', left=18, right=0)
            txt = self.line_box(txt_box)
            name_field = urwid.Edit(
                caption="",
                edit_text="",
                multiline=False,
                align="left",
                wrap="space",
                allow_tab=False,
                edit_pos=None,
                layout=None,
                mask=None,
            )
            btn = urwid.Button("OK", user_data=None)
            btn_cancel = urwid.Button("Cancel", user_data=None)
            div = urwid.Divider("─",bottom=2)
            ok_btn_attr = urwid.AttrMap(
                        btn,
                        None,
                        focus_map="reversed"
                    )
            cancel_btn_attr = urwid.AttrMap(
                        btn_cancel,
                        None,
                        focus_map="reversed"
                    )

            cols = urwid.Columns(
                    [
                        (10, ok_btn_attr ),
                        (10, cancel_btn_attr),
                    ],
                    dividechars=2,
                    focus_column=None,
                    min_width=1,
                    box_columns=None,
            )
            name_button = urwid.Padding(
                cols,
                align='center',
                width='pack',
                left=25
            )

            urwid.connect_signal(btn, "click", self.input_name, name_field)
            urwid.connect_signal(btn_cancel, "click", self.on_init_list,
                    name_field)
            wid = urwid.Pile([txt, name_field, div, name_button])
            new = urwid.AttrMap(wid, None, focus_map="")
            background = urwid.AttrMap(urwid.SolidFill(' '), 'basic')
            interior = urwid.Filler(new)
            window = self.line_box(interior)
            topw = urwid.Overlay(window, background, 'center', 50, 'middle', 10)

        except Exception as e:
            traceback.print_exc(file=sys.stdout)

        self.top.original_widget = urwid.Padding(topw, right=0, left=0)

    def header_widget(self):
        self.todos_count_label = urwid.Text("Total Todos", align="left")
        self.todos_count_display = urwid.Text("0", align="left")
        self.nocomp_count_label = urwid.Text("Todos Not Completed", align="right")
        self.nocomp_count_display = urwid.Text("0", align="right")
        cols = urwid.Columns(
            [
                (12, self.todos_count_label),
                ('pack', self.todos_count_display),
                (24, urwid.Text("│")),
                (19, self.nocomp_count_label),
                (3,self.nocomp_count_display),
            ],
            dividechars=0,
            focus_column=None,
            min_width=1,
            box_columns=None,
        )
        cols.pack((1, 1))
        header = urwid.Pile([cols], focus_item=None)
        head_final_widget = urwid.LineBox(
            header,
            title="Todo System ",
            title_align="center",
            tlcorner="┌",
            tline="─",
            lline="│",
            trcorner="┐",
            blcorner="└",
            rline="│",
            bline="─",
            brcorner="┘",
        )
        return head_final_widget

    def update_employee_count(self, count):
        self.emp_count_display.set_text(str(count))

    def load_employees(self):
        print("loading employees")

    def draw_ui(self):

        self.top = self.employee_list_ui()

        return self.top

    def row_items(self, todo_list):
        retList = []
        for todo in todo_list:
            idCol = (6, urwid.Text(str(todo.id), align='left'))
            doneCol = urwid.Text(str(bool(todo.done)), align='left')
            todoCol = urwid.Text(todo.todo)
            row = urwid.Columns([idCol, doneCol, todoCol])
            retList.append(row)
        return retList

    def employee_list_ui(self):
        #breakpoint()
        self.header = self.header_widget()
        todo_list =  self.Todos.get_all()

        # making the list
        self.list_walker = urwid.SimpleFocusListWalker(self.row_items(todo_list))


        list_heading = urwid.Columns(
            [
                (6, urwid.Text("Id", align="left")),
                urwid.Text("Done", align="left"),
                urwid.Text("Todo"),
            ],
            dividechars=0,
            focus_column=None,
            min_width=1,
            box_columns=None,
        )
        self.list_box = urwid.ListBox(self.list_walker)
        self.list_pile = urwid.Pile(
            [
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

        self.body = urwid.LineBox(
            self.list_pile,
            title="",
            title_align="center",
            tlcorner="┌",
            tline="─",
            lline="│",
            trcorner="┐",
            blcorner="└",
            rline="│",
            bline="─",
            brcorner="┘",
        )

        todo_ui = urwid.Frame(
            self.body, header=self.header, footer=None, focus_part="body"
        )

        return urwid.Padding(todo_ui, right=0, left=0)

    def handle_keys(self, key):
        if key == "q":
            raise urwid.ExitMainLoop()

        key_dict = {"l": self.load_employees, "n": self.new_todo_screen}

        try:
            key_dict[key]()
        except:
            pass


if __name__ == "__main__":
    todos = Todos('todo.db')
    todo_ui = TodoUI(todos)
    ui = todo_ui.draw_ui()
    loop = urwid.MainLoop(ui, palette, unhandled_input=todo_ui.handle_keys)
    loop.run()
