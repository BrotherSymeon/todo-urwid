import sqlite3
import collections


import os
import sys
import logging

logging.basicConfig(filename="example.log", level=logging.CRITICAL)
LOG = logging.getLogger(__name__)


class Db:
    def __init__(self, file_path):
        self.conn = None
        try:
            self.conn = sqlite3.connect(file_path)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            LOG.error(e.args[0])
            raise sqlite3.Error(e)
        self.cur = self.conn.cursor()
        # cur.execute("create table todos(id, todo, done);")

    def run_query(self, sql, params=()):
        retlist = []
        with self.conn:
            if "select" in sql:
                self.cur.execute(sql)
                for row in self.cur:
                    retlist.append(row)
            else:
                self.cur.execute(sql)
                self.con.commit()
        return retlist

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
                    "create table todos(id integer primary key, todo varchar, done bit);"
                )
                self.cur.execute("select 1 from todos;")
            except:
                raise Exception("something went wrong initializing the db")


class Todos(Db):
    SQL_SELECT_BY_ID = "select id, todo, done from todos where id ==(?);"
    SQL_SELECT_ALL = "select id, todo, done from todos;"
    SQL_SELECT_DONE = "select id, todo, done from todos where done=1;"
    SQL_SELECT_NOT_DONE = "select id, todo, done from todos where done=0;"
    SQL_UPDATE_BY_ID = "update todos set todo=?,done=? where id=?;"
    def __init__(self, db_path):
        super().__init__(db_path)
        self.init_db()

    def new(self, desc):
        todo = Todo(desc)
        self.save(todo)
        return todo

    def get_by_id(self, id):
        # TODO:change this to use self.run_query(sql)  <29-04-22, yourname> #
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
            self.cur.execute("select max(id) as max_id from todos;")
            for row in self.cur:
                logging.debug(row)
                max_id = row["max_id"]
                if max_id == None:
                    max_id = 0
                max_id += 1

            self.cur.execute(
                "insert into todos(id, todo, done)values(?,?,?);",
                (max_id, todo.todo, int(todo.done)),
            )
            self.conn.commit()
            self.cur.execute("select id, todo, done from todos where id=?;", (max_id,))
            for row in self.cur:
                todo.id = row["id"]

    def delete(self, todo):
        """deletes a Todo from the database"""
        self.cur.execute("delete from todos where id = ?", (todo.id,))
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
