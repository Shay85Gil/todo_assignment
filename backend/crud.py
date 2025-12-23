from flask import Flask, request, jsonify
from marshmallow import Schema, fields, validate
from datetime import datetime


class TaskSchema(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(max=255)
    )
    description = fields.Str(load_default="", required=False)
    status = fields.Str(
        load_default="open",
        validate=validate.OneOf(["open", "in_progress", "done"]),
        required=False
    )
    created_at = fields.DateTime(load_default=lambda: datetime.now())
    updated_at = fields.DateTime(load_default=lambda: datetime.now())


app = Flask(__name__)

tasks = {}
task_uuid_increment = 1


@app.get("/tasks")
def list_tasks():
    return ["tasks/" + str(key) for key in tasks.keys()], 200


@app.post("/tasks")
def create_new_single_task():
    global task_uuid_increment

    task_data = request.get_json()
    task_json = jsonify(task_data)

    # verify structure - 400 for validation errors
    schema = TaskSchema()
    try:
        task_json = schema.load(task_data)
    except Exception as exp:
        return {"error": f"Validation error, {exp}"}, 400

    tasks[task_uuid_increment] = task_json

    ret_location_header = f"tasks/{task_uuid_increment}"

    task_uuid_increment = task_uuid_increment + 1

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
    schema = TaskSchema()
    try:
        new_task_json = schema.load(new_task_data)
    except Exception as exp:
        return {"error": f"Validation error, {exp}"}, 400
    
    new_task_json["created_at"] = tasks[task_uuid]["created_at"]

    tasks[task_uuid] = new_task_json

    return tasks[task_uuid], 200


@app.patch("/tasks/<int:task_uuid>")
def update_single_task_status(task_uuid):
    if task_uuid not in tasks:
        return {"error": f"Task ID {task_uuid} not found"}, 404
    
    new_task_status = request.get_data(as_text=True)
    
    # verify status - 400 for validation errors
    if new_task_status in ["open", "in_progress", "done"]:
        tasks[task_uuid]["status"] = new_task_status
        tasks[task_uuid]["updated_at"] = datetime.now()
    else:
        return {"error": f"Validation error, '{new_task_status}' is an illegal text tp patch to status"}, 400

    return tasks[task_uuid], 200
    

@app.delete("/tasks/<int:task_uuid>")
def delete_new_task(task_uuid):
    if task_uuid not in tasks:
        return {"error": f"Task ID {task_uuid} not found"}, 404
    
    del tasks[task_uuid]
    return {"message": f"Task ID {task_uuid} deleted"}, 204


if __name__ == "__main__":
    app.run(debug=True)