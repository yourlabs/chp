def remove_todo(todo_id):
    todos = todoStore["todos"] or []
    todos = list(filter(lambda t: parseFloat(t["id"]) != todo_id, todos))
    todoStore.todos = todos

def update_todo_name():
    x = document["getElementById"]('myInput')
    todoStore["name"] = x["value"]

def add_todo(todoStore):
    todos = todoStore.todos or []
    t = todos[:]
    t.append({ "name" : todoStore["name"], "id": str(random.random())})
    todoStore["todos"] = t
    todoStore["name"] = ""


store_updates = {
    "add_todo": add_todo,
    "remove_todo": remove_todo,
    "update_todo_name": update_todo_name,
}
