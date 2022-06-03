# A minimal SQLite shell for experiments

import sqlite3
import tabulate

con = sqlite3.connect("./db.db")
#con.row_factory = sqlite3.Row
con.isolation_level = None
cur = con.cursor()


def load_database(db):
    global con
    print('attempting to load {0}'.format(db))
    con = sqlite3.connect(db)
    con.isolation_level = None
    global cur
    cur = con.cursor()

def flatten_description(desc):
    g = []
    for i in cur.description:
        for j in i:
            if j: g.append(j)
    return g

def print_help():
    print("""
    To load a new database use the load: command.

    example.

    load: ./new.db <return>

    To change the table format use the tablefmt:
    the available formats are
    - fancy_grid
    - grid

    example)

    tablefmt: grid

    To exit type:
    exit <return>
            """)
buffer = ""

print("Enter your SQL commands to execute in sqlite3.")
print("Enter help to view the Help Screen.")
print("Enter exit to leave the screen")

while True:
    line = input()
    if line == "help":
        print_help()
    elif line == "exit":
        break
    elif "load:" in line:
        load_database(line.split(' ')[1])

    buffer += line
    if sqlite3.complete_statement(buffer):
        try:
            buffer = buffer.strip()
            cur.execute(buffer)

            if buffer.lstrip().upper().startswith("SELECT"):
                out = cur.fetchall()
                headers = flatten_description(cur.description)

                print(tabulate.tabulate(out, headers, tablefmt="fancy_grid"))

        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
        buffer = ""

con.close()
