from marshmallow import Schema, fields, validate, EXCLUDE
from datetime import datetime

class TaskSchema(Schema):
    class Meta:
        unknown = EXCLUDE

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

def task_add_timestamps(json_in):
    json_out = json_in

    json_out["created_at"] = datetime.now()
    json_out["updated_at"] = json_out["created_at"]

    return json_out

def task_update_timestamps(json_in, ref_json):
    json_out = json_in

    json_out["updated_at"] = datetime.now()
    json_out["created_at"] = ref_json["created_at"]

    return json_out

def task_update_status(json_in, new_task_status):
    json_out = json_in
    
    json_out["status"] = new_task_status
    json_out["updated_at"] = datetime.now()

    return json_out