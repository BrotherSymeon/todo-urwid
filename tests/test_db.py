from clitodoapp.models.todo import Todo, TodoData, Todos
from unittest.mock import patch
import unittest
from peewee import SqliteDatabase

MODELS = [Todo]

# use an in-memory SQLite for tests.
db = SqliteDatabase(":memory:")


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        db.connect()
        db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        db.drop_tables(MODELS)

        # Close connection to db.
        db.close()

        # If we wanted, we could re-bind the models to their original
        # database here. But for tests this is probably not necessary.


class DatabaseTestCase(BaseTestCase):
    def test_todos_can_create_todo(self):
        ts = Todos()
        todo = ts.new("Get some breakfast")
        assert type(todo) == TodoData
        assert todo.desc == "Get some breakfast"
        assert todo.done == False
        assert todo.id != None

    def test_todos_can_insert_todo(self):
        ts = Todos()
        todo = ts.new("Get some breakfast")
        assert type(todo) == TodoData
        assert todo.desc == "Get some breakfast"
        assert todo.done == False
        assert todo.id != None
        todo.desc = "something different"
        ts.save(todo)
        assert todo.desc == "something different"

    def test_todos_can_get_by_id(self):
        ts = Todos()
        todo = ts.new("Get some breakfast")
        todo2 = ts.get_by_id(todo.id)
        assert todo.id == todo2.id
        assert todo.desc == todo2.desc
        assert todo.done == todo2.done

    def test_todos_can_get_all(self):
        ts = Todos()
        todo = ts.new("Get some breakfast")
        todo1 = ts.new("Get some breakfast")
        todo2 = ts.new("Get some breakfast")
        todoList = ts.get_all()
        assert len(todoList) == 3  # stupid test
