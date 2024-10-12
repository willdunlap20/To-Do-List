from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up the database and migration tools
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "task": self.task,
            "completed": self.completed
        }

# Route to serve the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Get all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

# Add a new todo
@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({"error": "Task is required"}), 400
    new_todo = Todo(
        task=data['task'],
        completed=False
    )
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

# Update an existing todo
@app.route('/todos/<int:todo_id>', methods=['PATCH'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json()
    todo.completed = data.get('completed', todo.completed)
    db.session.commit()
    return jsonify(todo.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
