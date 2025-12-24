from flask import Flask, request
from flask_cors import CORS

from task_format import TaskSchema, task_add_timestamps, task_update_timestamps, task_update_status

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "http://localhost:5173"]}})

# in-memory tasks
tasks = {}

# schema for marshmellow versication
schema = TaskSchema()

task_uuid_increment = 1

@app.get("/tasks")
def list_tasks():
    return ["tasks/" + str(key) for key in tasks.keys()], 200


@app.post("/tasks")
def create_new_single_task():
    global task_uuid_increment

    task_data = request.get_json()

    # verify structure - 400 for validation errors 
    try:
        task_json = schema.load(task_data)
        # adds same now timestamps to updated_at and created_at
        task_json = task_add_timestamps(task_json)
    except Exception as exp:
        return {"error": f"Validation error, {exp}"}, 400

    tasks[task_uuid_increment] = task_json

    ret_location_header = f"tasks/{task_uuid_increment}"

    # increment only after the header is store for return
    task_uuid_increment = task_uuid_increment + 1

    # 
    return ret_location_header, 201


@app.get("/tasks/<int:task_uuid>")
def read_single_task(task_uuid):
    if task_uuid in tasks:
        return tasks[task_uuid], 200
    else:
        return {"error": f"Task ID {task_uuid} not found"}, 404


@app.put("/tasks/<int:task_uuid>")
def update_single_task(task_uuid):
    if task_uuid not in tasks:
        return {"error": f"Task ID {task_uuid} not found"}, 404
    
    new_task_data = request.get_json()
    
    # verify structure - 400 for validation errors
    try:
        new_task_json = schema.load(new_task_data)
        # updates now timestamp to updated_at only
        new_task_json = task_update_timestamps(new_task_json, tasks[task_uuid])
    except Exception as exp:
        return {"error": f"Validation error, {exp}"}, 400

    tasks[task_uuid] = new_task_json

    return tasks[task_uuid], 200


@app.patch("/tasks/<int:task_uuid>")
def update_single_task_status(task_uuid):
    if task_uuid not in tasks:
        return {"error": f"Task ID {task_uuid} not found"}, 404
    
    new_task_status = request.get_data(as_text=True)
    
    # verify status - 400 for validation errors
    if new_task_status in ["open", "in_progress", "done"]:
        # also updates status and now timestamp to updated_at only
        tasks[task_uuid] = task_update_status(tasks[task_uuid], new_task_status)
    else:
        return {"error": f"Validation error, '{new_task_status}' is an illegal text to patch to status"}, 400

    return tasks[task_uuid], 200
    

@app.delete("/tasks/<int:task_uuid>")
def delete_new_task(task_uuid):
    if task_uuid not in tasks:
        return {"error": f"Task ID {task_uuid} not found"}, 404
    
    del tasks[task_uuid]
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)