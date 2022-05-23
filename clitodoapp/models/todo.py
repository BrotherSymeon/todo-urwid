import collections
import datetime
import logging


from peewee import Model, CharField, BooleanField, IntegerField, DateTimeField
from clitodoapp.models.db import db


LOG = logging.getLogger(__name__)


def create_tables():
    with db:
        db.create_tables([Todo])


class BaseModel(Model):
    class Meta:
        database = db


class Todo(BaseModel):
    desc = CharField()
    done = BooleanField(default=False)
    priority = IntegerField(choices=[(1, "High"), (2, "Medium"), (3, "Low")], default=2)
    blocked_reason = CharField(default='')
    created_date = DateTimeField(default=datetime.datetime.now)



class TodoData:
    """This is used to pass data back and forth so that
    the controller or view are not working with classes 
    that can update the database
    """
    PRIORITIES = {"HIGH":3, "MEDIUM":2, "LOW": 1}

    def __init__(self, id=None, desc=None, done=False, priority=2, blocked_reason=''):
        self.desc = desc if desc is not None else ''
        if self.desc == '':
            raise ValueError('desc can not be an empty string')
        self.done = done
        self.priority = priority
        self.blocked_reason = blocked_reason
        self.blocked = bool(len(self.blocked_reason))
        try:
            self.id = int(id) if id is not None else 0
        except ValueError as e:
            raise ValueError('id must be an integer')

    def __repr__(self):
        priority_map = {3:"High", 2:"Medium", 1:"Low"}
        return "TodoData(id={0}, todo={1}, done={2}, priority={3}, blocked={4})".format(
            self.id, self.desc, bool(self.done), priority_map[self.priority], self.blocked
        )


class Todos:
    """This is the Repository"""
    def new(self, desc):
        return self.convert_single(
                Todo.create(
                    desc=desc,
                    done=False,
                    priority=2,
                    blocked_reason=''
                )
            )

    def convert_single(self, todo):
        ret_todo = TodoData(
                    id=todo.id,
                    desc=todo.desc,
                    done=todo.done,
                    priority=todo.priority,
                    blocked_reason=todo.blocked_reason
                )
        return ret_todo

    def convert_all(self, todo_table_list):
        """convert each Todo obj into a Todo obj"""
        ret_list = []
        for todo_table in todo_table_list:
            todo = self.convert_single(todo_table)
            ret_list.append(todo)
        return ret_list

    def get_by_id(self, id):
        return Todo.get(Todo.id == id)

    def delete_by_id(self, id):
        """deletes a Todo from the database"""
        todo = self.get_by_id(id)
        return todo.delete_instance()

    def get_done(self):
        return self.convert_all(Todo.select().where(Todo.done == True))

    def get_not_done(self):
        return self.convert_all(Todo.select().where(Todo.done == False))

    def get_all(self):
        """gets all of the todos from the database"""
        return self.convert_all(Todo.select())

    def save(self, todo):
        """creates or updates the current todo to the db"""
        return_val = 0
        if todo.id:
            todo_record = self.get_by_id(todo.id)
            todo_record.desc = todo.desc
            todo_record.done = todo.done
            todo_record.priority = todo.priority
            todo_record.blocked_reason = todo.blocked_reason
            return_val = todo_record.save()
            todo.id = todo_record.id
            return return_val
        else:
            todo_record = Todo.create(
                    desc=todo.desc,
                    done=todo.done,
                    priority=todo.priority,
                    blocked_reason=todo.blocked_reason
                )
            return_val = todo_record.save()
            todo.id = todo_record.id
            return return_val


    def delete(self, todo):
        """Depricated: use delete_by_id instead"""
        return Todo.delete().where(Todo.id == todo.id)
