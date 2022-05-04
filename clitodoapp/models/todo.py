import sqlite3
import collections


import logging

LOG = logging.getLogger(__name__)


class Db:
    def __init__(self, file_path):
        LOG.info("initializing Db")
        self.conn = None
        try:
            self.conn = sqlite3.connect(file_path)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            LOG.error(e.args[0])
            raise sqlite3.Error(e)
        self.cur = self.conn.cursor()
        # cur.execute("create table todos(id, todo, done);")


    def init_db(self):
        """initialize the db"""
        try:
            LOG.info("testing whether or not there is a todo table yet")
            self.cur.execute("select * from todos;")
            LOG.info("the todo table seems to be in existance")
        except sqlite3.Error as e:
            LOG.info("maybe no todo table: trying to create one")
            try:
                self.cur.execute(
                    "create table todos(id integer primary key AUTOINCREMENT, todo varchar, done bit);"
                )
                self.cur.execute("select * from todos;")
            except Exception as e:
                raise Exception("something went wrong initializing the db")


class Todos(Db):
    SQL_SELECT_BY_ID = "select id, todo, done from todos where id ==(?);"
    SQL_SELECT_ALL = "select id, todo, done from todos;"
    SQL_SELECT_DONE = "select id, todo, done from todos where done=1;"
    SQL_SELECT_NOT_DONE = "select id, todo, done from todos where done=0;"
    SQL_UPDATE_BY_ID = "update todos set todo=?,done=? where id=?;"
    SQL_SELECT_LAST_INSERTED = "select id, todo, done from todos where"
    SQL_SELECT_LAST_INSERTED += " id=last_insert_rowid();"
    SQL_INSERT_TODO = "insert into todos(todo, done)values(?,?);"
    SQL_DELETE_BY_ID = "delete from todos where id = ?;"

    def __init__(self, db_path):
        super().__init__(db_path)
        self.init_db()

    def __str__(self):
        return "Todo(id={0}, todo={1}, done={2})".format(self.id, self.todo, bool(self.done))

    def new(self, desc):
        todo = Todo(desc)
        self.save(todo)
        return todo

    def get_by_id(self, id):
        self.cur.execute(Todos.SQL_SELECT_BY_ID, (id,))
        for row in self.cur:
            todo = Todo(row["todo"])
            todo.id = row["id"]
            todo.done = bool(row["done"])
        return todo

    def get_records(self, cur):
        all_todos = []
        for row in cur:
            todo = Todo(row["todo"])
            todo.id = row["id"]
            todo.done = bool(row["done"])
            all_todos.append(todo)

        return all_todos

    def get_done(self):
        self.cur.execute(Todos.SQL_SELECT_DONE)
        return self.get_records(self.cur)

    def get_not_done(self):
        self.cur.execute(Todos.SQL_SELECT_NOT_DONE)
        return self.get_records(self.cur)

    def get_all(self):
        """gets all of the todos from the database"""
        self.cur.execute(Todos.SQL_SELECT_ALL)
        return self.get_records(self.cur)

    def save(self, todo):
        """creates or updates the current todo to the db
        >>t = Todo('Go to the store')
        >>ts = Todos()
        >>ts.save(t)
        >>all = Todos.get_all()
        """
        if todo.id != None:
            self.cur.execute(
                Todos.SQL_UPDATE_BY_ID,
                (todo.todo, int(todo.done), todo.id),
            )
            self.conn.commit()
        else:

            self.cur.execute(
                Todos.SQL_INSERT_TODO,
                (todo.todo, int(todo.done)),
            )
            self.conn.commit()
            self.cur.execute(Todos.SQL_SELECT_LAST_INSERTED)
            for row in self.cur:
                todo.id = row["id"]

    def delete(self, todo):
        """deletes a Todo from the database"""
        self.cur.execute(Todos.SQL_DELETE_BY_ID, (todo.id,))
        self.conn.commit()


class Todo:
    def __init__(self, desc):
        self.todo = desc
        self.done = False
        self.id = None

    def __repr__(self):
        return "Todo(id={0}, todo={1}, done={2})".format(
            self.id, self.todo, bool(self.done)
        )
