import pytest
import requests
from uuid import uuid4

#CRUD
BASE_URL = 'http://127.0.0.1:5000'
tasks = []

def test_create_task():
    new_task_data = {
        'title': 'Task 1',
        'description': 'This is task 1'
    }

    response = requests.post(f'{BASE_URL}/tasks', json=new_task_data)
    assert response.status_code == 201
    response_json = response.json()
    assert response_json['Message'] == 'Task created successfully'
    assert 'id' in response_json
    tasks.append(response_json['id'])


def test_get_task():
    response = requests.get(f'{BASE_URL}/tasks')
    assert response.status_code == 200
    response_json = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json  

def test_get_task_by_id():
    if tasks:
        task_id = tasks[0]
        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200
        response_json = response.json()
        assert task_id == response_json['id']

def test_update_task():
    if tasks:
        task_id = tasks[0]
        update_data = {
            'title': 'Task 1 Updated',
            'description': 'This is task 1 updated',
            'completed': True
        }
        response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=update_data)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['Message'] == 'Task updated successfully'

        # New request to get the updated task
        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['title'] == update_data['title']
        assert response_json['description'] == update_data['description']
        assert response_json['completed'] == update_data['completed']

def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['Message'] == 'Task deleted successfully'

        # New request to get the deleted task
        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 404

def test_failed_create_task():
    new_task_data = {
        'description': 'Task 1',
    }

    response = requests.post(f'{BASE_URL}/tasks', json=new_task_data)
    assert response.status_code == 400
    response_json = response.json()
    assert response_json['Message'] == 'Title is required'

def test_failed_get_task_by_id():
    task_id = uuid4()
    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 404
    response_json = response.json()
    assert response_json['Message'] == 'Task not found'      

def test_failed_update_task():
    task_id = uuid4()
    update_data = {
        'title': 'Task 1 Updated',
        'description': 'This is task 1 updated',
        'completed': True
    }
    response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=update_data)
    assert response.status_code == 404
    response_json = response.json()
    assert response_json['Message'] == 'Task not found'

def test_failed_delete_task():
    task_id = uuid4()
    response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 404
    response_json = response.json()
    assert response_json['Message'] == 'Task not found'              
