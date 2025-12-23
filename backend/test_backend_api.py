import requests
import time

BASE_URL = "http://localhost:5000"  # Flask


def test_create_task_good():
    res = requests.post(f"{BASE_URL}/tasks", json=
    {
        "title": "task1",
        "description": "desc1"
    })

    assert res.status_code == 201
    assert "tasks/" in res.text


def test_create_task_good_title_only():
    res = requests.post(f"{BASE_URL}/tasks", json=
    {
        "title": "task2",
    })

    assert res.status_code == 201
    assert "tasks/" in res.text


def test_create_task_bad_no_title():
    res = requests.post(f"{BASE_URL}/tasks", json=
    {
        "description": "desc3"
    })

    assert res.status_code == 400
    assert "error" in res.text
    assert "title" in res.text # asserts the error is in title field


def test_create_task_bad_long_title():
    res = requests.post(f"{BASE_URL}/tasks", json=
    {
        "title": "task4"*255 # longer than 255 chars
    })

    assert res.status_code == 400
    assert "error" in res.text
    assert "title" in res.text


def test_create_task_bad_illegal_status():
    res = requests.post(f"{BASE_URL}/tasks", json=
    {
        "title": "task5",
        "status": "bad"
    })

    assert res.status_code == 400
    assert "error" in res.text
    assert "status" in res.text # asserts the error is in status field


def test_get_tasks():
    res = requests.get(f"{BASE_URL}/tasks")

    assert res.status_code == 200

    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert "tasks/1" in data[0]
    assert "tasks/2" in data[1]


def test_get_single_tasks():
    res = requests.get(f"{BASE_URL}/tasks/0")

    assert res.status_code == 404

    res = requests.get(f"{BASE_URL}/tasks/1")

    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "task1"
    assert data["status"] == "open"
    assert data["created_at"] == data["updated_at"]

    res = requests.get(f"{BASE_URL}/tasks/2")

    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "task2"
    assert data["description"] == ""
    assert data["status"] == "open"
    assert data["created_at"] == data["updated_at"] 


def test_update_single_bad_then_good_title():
    res = requests.put(f"{BASE_URL}/tasks/1", json=
    {
        "title": "task1_new"*255 # longer than 255 chars
    })

    assert res.status_code == 400
    assert "error" in res.text
    assert "title" in res.text

    time.sleep(1)

    res = requests.put(f"{BASE_URL}/tasks/1", json=
    {
        "title": "task1_new"
    })

    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "task1_new"
    assert data["created_at"] != data["updated_at"]


def test_update_single_bad_then_good_status():
    res = requests.put(f"{BASE_URL}/tasks/1", json=
    {
        "title": "task1_new_with_status_change",
        "status": "bad"
    })

    assert res.status_code == 400
    assert "error" in res.text
    assert "status" in res.text

    time.sleep(1)

    res = requests.put(f"{BASE_URL}/tasks/1", json=
    {
        "title": "task1_new_with_status_change",
        "status": "done"
    })

    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "task1_new_with_status_change"
    assert data["status"] == "done"
    assert data["created_at"] != data["updated_at"]
    

def test_update_not_found():
    res = requests.put(f"{BASE_URL}/tasks/0", json=
    {
        "title": "task1_new_with_status_change",
        "status": "done"
    })

    assert res.status_code == 404
    assert "error" in res.text
    assert "not found" in res.text


def test_patch_single_bad_then_good_status():
    res = requests.patch(f"{BASE_URL}/tasks/2", data="bad")

    assert res.status_code == 400
    assert "error" in res.text
    assert "illegal text" in res.text

    time.sleep(1)

    res = requests.patch(f"{BASE_URL}/tasks/2", data="in_progress")

    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "task2"
    assert data["status"] == "in_progress"
    assert data["created_at"] != data["updated_at"]


def test_delete_tasks():
    res = requests.delete(f"{BASE_URL}/tasks/1")
    assert res.status_code == 204
    
    res = requests.delete(f"{BASE_URL}/tasks/2")
    assert res.status_code == 204

    # check really empty by getting task list
    res = requests.get(f"{BASE_URL}/tasks")

    assert res.status_code == 200

    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 0






























































