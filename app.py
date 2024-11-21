from flask import Flask, request, jsonify
from models.task import Task
from uuid import uuid4

# __name__ = __main__
app = Flask(__name__)

tasks = []

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(
        id=uuid4(),
        title=data.get('title'),
        description=data.get('description', '')
    )
    tasks.append(new_task)
    return jsonify({'Message': 'Task created successfully'}), 201

@app.route('/tasks', methods=['GET'])
def list_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }
    return jsonify(output)

@app.route('/tasks/<uuid:id>', methods=['GET'])
def get_task(id):
    for task in tasks:
        if task.id == id:
            return jsonify(task.to_dict())
    return jsonify({'Message': 'Task not found'}), 404
    
@app.route('/tasks/<uuid:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    for task in tasks:
        if task.id == id:
            task.title = data.get('title')
            task.description = data.get('description')
            task.completed = data.get('completed')
            return jsonify({'Message': 'Task updated successfully'})
        return jsonify({'Message': 'Task not found'}), 404    

@app.route('/tasks/<uuid:id>', methods=['DELETE'])
def delete_task(id):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return jsonify({'Message': 'Task deleted successfully'})
    return jsonify({'Message': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)