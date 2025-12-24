# todo_assignment
A simple web application for creating and managing a list of tasks

# Setup Instructions
1. Run "docker-compose build --no-cache" (sudo)
2. Run "docker-compose up" (sudo)

# API Usage examples
1. Create Task:
    curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" \
  -d '{
    "title": "Buy milk",
    "description": "2 liters"
  }'
2. List all tasks:
    curl http://localhost:5000/tasks
3. Get a listed task:
    curl http://localhost:5000/tasks/{task_uuid}
4. Updated task:
    curl -X PUT http://localhost:5000/tasks/{task_uuid} -H "Content-Type: application/json" \
  -d '{
    "title": "Buy milk",
    "description": "3 liters",
    "status": "in_progress"
  }'
5. patch task status only:
    curl -X PATCH http://localhost:5000/tasks/{task_uuid} -H "Content-Type: application/text" -d "done"
6. Delete task:
    curl -X DELETE http://localhost:5000/tasks/{task_uuid}

# Architecture Notes
1. Used Flask as a lean and stright-forward REST API package.
2. Used marshmallow to help enforce validation errors.
3. Used Docker to avoid many instalations. and also as a part to run pytest test suit, that fails the docker build.
4. Added GitHub Actions CI on push and PR that fails in docker build fails because of errors/tests.

# Assumptions Made
1. In task create, the POST endpoint would get a workload with legal title at least, to avoid "zombie" task that are not as defined
2. This is a single person or small group app, that assumes hard page refresh when more than one local user for sync.
3. Also, assumes users won't edit task that are not theirs.

# Possible Improvements
1. This implementation uses in-memory records as the app runs. Database usage for such a POC assignment assumed to be an overhead.
2. Prettier GUI.

# AI Used
1. ChatGPT 5.2 - to select frameworks (as I didn't came from Full Stack).
2. ChatGPT 5.2 - to understand syntax and get some code refs and snipets.
3. ChatGPT 5.2 - for docker-compose and github actions and understand basic vue bring-up.