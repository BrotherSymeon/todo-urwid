import urwid
import logging

logging.basicConfig(filename='todo.log', level=logging.INFO)

palette = [
    ('reversed', 'standout', ''),
    ('body','black','dark cyan', 'standout'),
    ('header','black','light blue', 'standout'),
    ('foot','light gray', 'black'),
    ('key','light cyan', 'black', 'underline'),
    ('title', 'white', 'black',),
    ('b', 'black', 'dark gray'),
    ('highlight', 'black', 'light blue'),
    ('bg', 'black', 'dark blue'),
]

footer_text = [
    ('title', "Todo Viewer"), "    ",
    ('key', "UP"), ", ", ('key', "DOWN"), ", ",
    ('key', "PAGE UP"), " and ", ('key', "PAGE DOWN"),
    " move view  ",
    ('key', "Q"), " exits",
]


todo_items = [
    {"todo": "Go to the store", "done": "False", "id": "1"},
]

start = 5
def nextnum():
    global start
    start += 1
    return str(start)

def item(thing):
    todo = urwid.Text(thing["todo"])
    id = urwid.Text(thing["id"])
    done = urwid.CheckBox("", bool(thing["done"]), on_state_change=on_done_changed, user_data=(thing['id'], thing['todo']))
    button = urwid.Button("Edit")
    delete_button = urwid.Button("Delete")
    urwid.connect_signal(delete_button, "click", delete_thing, (id, todo))
    urwid.connect_signal(button, "click", edit_thing, (id, todo))
    col = urwid.Columns(
        [id, done, todo, button, delete_button],
        dividechars=0,
        focus_column=None,
        min_width=1,
        box_columns=None,
    )
    return col 

def items():
    retval = []
    for thing in todo_items:
        retval.append(item(thing))
    return retval

def on_done_changed(box, state, user_data):
    for i in todo_items:
        if i['id'] == user_data[0]:
            i['done'] = str(False)
            logging.info("Here is the updated obj {0}".format(i))

    listbox.body = items()

def edit_thing(button, user_data):
    pass

def delete_thing(button, user_data):
    pass

def exit_on_q(input):
        if input in ('q', 'Q'):
            raise urwid.ExitMainLoop()


class CustomListBox(urwid.ListBox):
    def __init__(self):
        body = urwid.SimpleFocusListWalker(items())
        super(CustomListBox, self).__init__(body)

class TodoBox(urwid.Padding):
    def keypress(self, size,key):
        if key != "enter":
            return super(TodoBox, self).keypress(size,key)
        listbox.body.append(item(self.create_todo(self.original_widget.get_edit_text())))

    def create_todo(self, todo):
        return {"id": nextnum(),
                "done": "False",
                "todo": todo,
                }


listbox = None


def run():
    global listbox
    listbox = CustomListBox()

    edit = urwid.Edit("What do you want to do?\n")
    edit = TodoBox(edit)
    header = urwid.AttrMap(edit, 'header')
    header = urwid.Padding(header, 'center', 120)
    listpad = urwid.Padding(listbox, 'center', 120)
    footer = urwid.AttrMap(urwid.Text(footer_text), 'foot')
    footer = urwid.Padding(footer, 'center', 120)
    view = urwid.Frame(listpad, header=header, footer=footer)
    loop = urwid.MainLoop(view, palette, unhandled_input=exit_on_q)
    loop.run()


if __name__ == "__main__":
    run()
