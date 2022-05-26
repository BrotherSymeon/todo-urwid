import urwid

class Header(urwid.WidgetWrap): 
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
    def completed(self):
        """
            >>> from clitodoapp.widgets.header import Header
            >>> h = Header("Todo System")
            >>> h.completed = 9
            >>> h.completed
            9
            >>>

        """
        tup = self.total_display.get_text()
        return int(tup[0])

    @completed.setter
    def completed(self, completed):
        self.total_display.set_text(str(completed))

    @property
    def not_completed(self):
        """
        Gets the not completed display value for this widget

            >>> from clitodoapp.widgets.header import Header
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
        self.not_complete_display.set_text(str(not_completed))

