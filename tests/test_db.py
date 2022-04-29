
from clitodoapp.models.todo import Db, Todo, Todos
import logging

logging.basicConfig(filename='test.log', level=logging.DEBUG)

logging.debug('ok we are starting testing')
def test_db_exists():
    db = Db(':memory:')
    assert(db != None)

def test_db_can_init():
    db = Db(':memory:')
    db.init_db()

def test_todos_can_create_todo():
    ts = Todos(':memory:')
    todo = ts.new('Get some breakfast')    
    assert(type(todo) == Todo)
    assert(todo.todo == 'Get some breakfast')
    assert(todo.done == False)
    assert(todo.id != None)
    
def test_todos_can_insert_todo():
    ts = Todos(':memory:')
    todo = ts.new('Get some breakfast')    
    assert(type(todo) == Todo)
    assert(todo.todo == 'Get some breakfast')
    assert(todo.done == False)
    assert(todo.id != None)
    todo.todo = 'something different'
    ts.save(todo)
    assert(todo.todo == 'something different')

def test_todos_can_get_by_id():
    ts = Todos(':memory:')
    todo = ts.new('Get some breakfast')    
    todo2 = ts.get_by_id(todo.id)
    assert(todo.id == todo2.id)
    assert(todo.todo == todo2.todo)
    assert(todo.done == todo2.done)

def test_todos_can_get_all():
    ts = Todos(':memory:')
    todo = ts.new('Get some breakfast')    
    todo2 = ts.new('Get some breakfast')    
    todo3 = ts.new('Get some breakfast')    
    todo4 = ts.new('Get some breakfast')    
    todoList = ts.get_all()
    assert(len(todoList) == 4)
