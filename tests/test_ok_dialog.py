import panwid.dialog as pan
import urwid


def line_box(widget, caption="", align_title="center"):
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


def main():
    screen = urwid.raw_display.Screen()
    screen.set_terminal_properties(16) 

    pile_list = urwid.Pile( 
        [ 
            ('pack', urwid.Text("Name:", align="left")),
            ('weight', 1, urwid.Filler(urwid.Text("Address: ", align="left"))),
        ] 
    )

    test_body = line_box(pile_list)
    test_footer_text = (
        "foot",
        [
            "my footer   ",
            ("key", "F8"),
        ],
    )
    test_footer = urwid.AttrMap(urwid.Text(test_footer_text), "foot")
    my_frame = urwid.Frame(
        body=test_body, focus_part="body"
    )
    my_frame_filler =  urwid.Filler(my_frame) 
    loop = urwid.MainLoop(
        my_frame, screen=screen, unhandled_input=handle_keys
    )
    loop.run()



if __name__ == "__main__":
    main()
