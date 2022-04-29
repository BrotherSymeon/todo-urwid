import urwid

palette = [
    ("reversed", "standout", ""),
    ("b", "black", "dark gray"),
    ("highlight", "black", "light blue"),
    ("bg", "black", "dark blue"),
]


class PayrollUI:
    def __init__(self):
        pass

    def input_name(self, button, name_field):
        name = name_field.get_edit_text().rstrip()
        print(name)
        self.initialize_list_ui()

    def initialize_list_ui(self):
        self.top.original_widget = self.employee_list_ui()

    def new_employee_screen(self):
        txt = urwid.Text("Enter Employee Name below: ")
        name_field = urwid.Edit(
            caption="New Todo",
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
        div = urwid.Divider(u"─",bottom=2)
        name_button = urwid.AttrMap(btn, None, focus_map="reversed")
        urwid.connect_signal(btn, "click", self.input_name, name_field)
        wid = urwid.Pile([txt, name_field, div, name_button])
        new = urwid.Filler(urwid.AttrMap(wid, None,
            focus_map=""),top=0,bottom=0)
        ok_screen_box = urwid.Padding(
            urwid.LineBox(
                new,
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
            ),
            align="center",
            min_width=None,
            left=10,
            right=10,
        )

        self.top.original_widget = ok_screen_box

    def header_widget(self):
        self.todos_count_label = urwid.Text("Total Todos", align="left")
        self.todos_count_display = urwid.Text("0", align="left")
        self.nocomp_count_label = urwid.Text("Todos Not Comleted", align="right")
        self.nocomp_count_display = urwid.Text("0", align="right")
        cols = urwid.Columns(
            [
                (12, self.todos_count_label),
                self.todos_count_display,
                (19, self.nocomp_count_label),
                self.nocomp_count_display,
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

    def employee_list_ui(self):
        self.header = self.header_widget()

        # making the list
        self.list_walker = urwid.SimpleFocusListWalker([])

        list_heading = urwid.Columns(
            [
                (6, urwid.Text("Id", align="left")),
                urwid.Text("Todo", align="left"),
                urwid.Text("Done", align="right"),
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
                (1, urwid.Filler(urwid.Divider())),
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

        payroll_ui = urwid.Frame(
            self.body, header=self.header, footer=None, focus_part="body"
        )

        return urwid.Padding(payroll_ui, right=0, left=0)

    def handle_keys(self, key):
        if key == "q":
            raise urwid.ExitMainLoop()

        key_dict = {"l": self.load_employees, "n": self.new_employee_screen}

        try:
            key_dict[key]()
        except:
            pass


if __name__ == "__main__":
    print(__name__)
    payroll_ui = PayrollUI()
    ui = payroll_ui.draw_ui()
    loop = urwid.MainLoop(ui, palette, unhandled_input=payroll_ui.handle_keys)
    loop.run()
else:
    print(__name__)
