from flask import Flask, request, jsonify, render_template_string
from flask_mysqldb import MySQL
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

app = Flask(__name__)

app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        try:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            print("Database connection successful")
        except Exception as e:
            print("Database connection failed: ", e)

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO tasks (name, description) VALUES (%s, %s)", (name, description))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Task added'}), 201
    else:
        form = '''
        <h1>Task List</h1>
        <h2>Add new task</h2>
        <form method="post" action="/">
            <label for="name">Task Name:</label>
            <input type="text" id="name" name="name">
            <label for="description">Description:</label> 
            <input type="text" id="description" name="description"> 
            <input type="submit" value="Add new task">
        </form>
        '''
        return render_template_string(form)

# Route to create a new task
@app.route('/task', methods=['POST'])
def add_task():
    name = request.json['name']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO tasks (name) VALUES (%s)", (name,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'New task added'}), 201

# Route to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    return jsonify(tasks)

# Route to get a single task
@app.route('/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    cursor.close()
    return jsonify(task)

# Route to update a task
@app.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    name = request.json['name']
    description = request.json['description']  
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE tasks SET name = %s, description = %s WHERE id = %s", (name, description, task_id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Task updated'})

# Route to delete an task
@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

