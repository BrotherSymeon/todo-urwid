 - Start breaking down the main view into smaller chunks by writing them into widgets usoing the widget wrap
 I think that doing this first will result in an easier time of converting to MVC
    - FilterWidget
        -Encapsulates the filter activity and emits filter-changed event
    - HeaderWidget
        - Encapulates the reporting part at the top.
        - It jsut need the ability to update the datapoints
        - Total Todos
        - Completed Todos
    - TodoListWidget
        - Alot of the functionality will end up getting moved to this widget
        - It should emit 
            - delete-clicked
            - edit-clicked
            - done-clicked
    - FooterWidget
        - I would kinda like to see a little more happening there Like
            - live messages like 
                - sucessfull updates
                - error messages
                    -BTW thats e.args[0]
                - eh

- This will be a great exercise


```python
def foo():
    if bar:
        print("Ello!")
```
