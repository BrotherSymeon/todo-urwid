"""
A RadioButton List for setting the current filter

The options are All, Done and NotDone

"""
import logging
import urwid
import enum

from clitodoapp.helpers.ui_layouts import SimpleLayout

LOG = logging.getLogger(__name__)



class FilterEnum(enum.Enum):
    ALL = 1
    DONE = 2
    NOT_DONE = 3


class Filter(urwid.WidgetWrap):

    signals = ['filter-changed']
    filters = FilterEnum

    def __init__(self, default_filter):

        self.filter_group = []
        self.filters = []

        self.filter_all = urwid.RadioButton(
            self.filter_group,
            "All",
            bool(default_filter.name == Filter.filters.ALL.name),
        )
        self.filter_done = urwid.RadioButton(
            self.filter_group,
            "Done",
            bool(default_filter.name == Filter.filters.DONE.name),
        )
        self.filter_not_done = urwid.RadioButton(
            self.filter_group,
            "Not Done",
            bool(default_filter.name == Filter.filters.NOT_DONE.name),
        )
        self.filters.append(self.filter_all)
        self.filters.append(self.filter_done)
        self.filters.append(self.filter_not_done)

        # connect all the RadioButtons
        urwid.connect_signal(
            self.filter_all,
            "change",
            lambda *args: self._emit(
                "filter-changed",
                self.filter_all,
                Filter.filters.ALL
            ),
        )
        urwid.connect_signal(
            self.filter_done,
            "change",
            lambda *args: self._emit(
                "filter-changed",
                self.filter_done,
                Filter.filters.DONE
            ),
        )
        urwid.connect_signal(
            self.filter_not_done,
            "change",
            lambda *args: self._emit(
                "filter-changed",
                self.filter_not_done,
                Filter.filters.NOT_DONE
            ),
        )

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
        self.__super.__init__(widget)


    @property
    def current_filter(self):
        for w in self.filters:
            if w.state == True:
                return w.label.upper()




class FilterTestLayout(SimpleLayout):

    def body(self):
        self.header_label = urwid.Text("Testing the Filter")
        header = urwid.Pile([self.header_label], focus_item=None)
        head_final_widget = header
        self.filter = Filter(Filter.filters.NOT_DONE)
        body = urwid.LineBox(urwid.Padding(urwid.Filler(self.filter)))

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



    def handle_keys(self, key):
        if key == "f8":
            raise urwid.ExitMainLoop()
        if key == "i":
            pass



if __name__ == "__main__":
    FilterTestLayout().start()
