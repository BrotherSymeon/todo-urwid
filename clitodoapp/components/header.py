import logging

import urwid
from clitodoapp.helpers.ui_layouts import SimpleLayout

LOG = logging.getLogger(__name__)

class Header(urwid.WidgetWrap):
    """
        >>> header = Header('Todo System')
        >>> header.total = 9
        >>> canvas = header.render((50,))
        >>> txt = ''
        >>> for i in canvas.text:
        ...     txt = txt + i.decode()
        ...
        >>> assert 'Todo System' in txt
        >>> assert 'Not Complete' in txt
        >>> assert 'Total Todos 9' in txt
    """
    def __init__(self, caption):
        total_label = urwid.Text("Total Todos", align="left")
        not_complete_label = urwid.Text("Not Completed", align="right")

        self.total_display = urwid.Text("0", align="left")
        self.not_complete_display = urwid.Text("0", align="right")
        cols = urwid.Columns(
            [
                (12, total_label),
                ("weight", 5, self.total_display),
                (19, not_complete_label),
                (3, self.not_complete_display),
            ],
            dividechars=0,
            focus_column=None,
            min_width=1,
            box_columns=None,
        )
        header = urwid.Pile([cols], focus_item=None)
        w = urwid.LineBox(
                header,
                title=caption,
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
        self.__super.__init__(w)

    @property
    def total(self):
        """
            >>> from clitodoapp.components.header import Header
            >>> h = Header("Todo System")
            >>> h.total = 9
            >>> h.total
            9
            >>>

        """
        tup = self.total_display.get_text()
        return int(tup[0])

    @total.setter
    def total(self, total):
        try:
            total = int(total)
            self.total_display.set_text(str(total))
        except ValueError as e:
            LOG.error('error while setting total', e)
            raise ValueError('total must be an integer', e)



    @property
    def not_completed(self):
        """
        Gets the not completed display value for this widget

            >>> from clitodoapp.components.header import Header
            >>> h = Header("Todo System")
            >>> h.not_completed = 9
            >>> h.not_completed
            9
            >>>

        """
        tup = self.not_complete_display.get_text()
        return int(tup[0])

    @not_completed.setter
    def not_completed(self, not_completed):
        """
            Sets the not completed display value for this widget
        """
        try:
            not_completed = int(not_completed)
            self.not_complete_display.set_text(str(not_completed))
        except ValueError as e:
            LOG.error('error while setting not_completed', e)
            raise ValueError('not_completed value must be an integer', e)



class HeaderTestLayout(SimpleLayout):
    def __init__(self):
        self.total_count = 0
        self.not_done_count = 0
        super().__init__()

    def body(self):
        self.header_label = Header("Simple Header")
        header = urwid.Pile([self.header_label], focus_item=None)
        head_final_widget = header

        body = urwid.LineBox(urwid.Padding(urwid.Filler(urwid.Text(""))))

        footer_text = (
            "foot",
            [
                "Simple Footer ",
                ("key", "F8"),
                " quit    ",
            ],
        )
        footer = urwid.AttrMap(urwid.Text(footer_text), "foot")
        simple_ui = urwid.Frame(
            body, header=head_final_widget, footer=footer, focus_part="body"
        )

        return urwid.Padding(simple_ui, right=0, left=0)

    def inc_total_count(self):
        self.total_count += 1
        self.header_label.total = self.total_count


    def handle_keys(self, key):
        if key == "f8":
            raise urwid.ExitMainLoop()
        if key == "i":
            self.inc_total_count()




if __name__ == "__main__":
    HeaderTestLayout().start()
