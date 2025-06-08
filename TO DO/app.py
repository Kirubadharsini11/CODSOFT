from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
TASK_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())

@app.route("/tasks", methods=["POST"])
def add_task():
    task_text = request.json.get("task")
    tasks = load_tasks()
    tasks.append({"task": task_text, "done": False})
    save_tasks(tasks)
    return jsonify(success=True)

@app.route("/tasks/<int:index>", methods=["PUT"])
def update_task(index):
    tasks = load_tasks()
    tasks[index]["done"] = True
    save_tasks(tasks)
    return jsonify(success=True)

@app.route("/tasks/<int:index>", methods=["DELETE"])
def delete_task(index):
    tasks = load_tasks()
    tasks.pop(index)
    save_tasks(tasks)
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
