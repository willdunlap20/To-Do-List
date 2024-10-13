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
    title = db.Column(db.String(100), nullable=False)  # New title field
    notes = db.Column(db.String(255), nullable=True)    # New notes field
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, default=1)
    order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "notes": self.notes,
            "completed": self.completed,
            "priority": self.priority,
            "order": self.order
        }

# Route to serve the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Get all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.order_by(Todo.order).all()
    return jsonify([todo.to_dict() for todo in todos])

# Add a new todo
@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_todo = Todo(
        title=data['title'],    # Now capturing the title
        notes=data.get('notes', ''),  # Optional notes field
        completed=False,
        priority=data.get('priority', 1),
        order=data.get('order', 0)
    )
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

# Update an existing todo
@app.route('/todos/<int:todo_id>', methods=['PATCH'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json()
    todo.title = data.get('title', todo.title)  # Allow updating title
    todo.notes = data.get('notes', todo.notes)  # Allow updating notes
    todo.completed = data.get('completed', todo.completed)
    todo.priority = data.get('priority', todo.priority)
    todo.order = data.get('order', todo.order)
    db.session.commit()
    return jsonify(todo.to_dict())

# Delete a todo
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted'}), 200

# Update task order
@app.route('/update_task_order', methods=['POST'])
def update_task_order():
    data = request.get_json()
    for index, todo_id in enumerate(data['order']):
        todo = Todo.query.get(todo_id)
        if todo:
            todo.order = index
    db.session.commit()
    return jsonify({'message': 'Order updated'}), 200

if __name__ == '__main__':
    app.run(debug=True)
