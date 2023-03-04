from flask import Flask, g, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect('./database.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    #Check if DB is there
    if not hasattr(g, 'sqlite3'):
        g.sqlite3_db = connect_db()
    return g.sqlite3_db

#close the connection to the database automatically
@app.teardown_appcontext
def close_db(error):
    #if global object has a sqlite database then close it. If u leave it open noone can access it and gets lost in memory causing leaks.
    if hasattr(g, 'sqlite_db'):
        g.sqlite3_db.close()

@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

@app.route('/users')
def viewusers():
    db = get_db()
    cursor = db.execute('select id, name, age from users')
    results = cursor.fetchall()
    return f"<h1>The Id is {results[0]['id']}.<br> The Name is {results[0]['name']}. <br> The age is {results[0]['age']}. </h1>"


#CREATE
@app.route('/users', methods=['POST'])
def create_user():
    db = get_db()
    name = request.json['name']
    age = request.json['age']
    db.execute('INSERT INTO users (name, age) VALUES (?, ?)', [name, age])
    db.commit()
    return jsonify({'message': 'User created successfully!'})


#READ
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE id = ?', [user_id])
    result = cursor.fetchone()
    if not result:
        return jsonify({'error': 'User not found'})
    return f"<h1>The Id is {result['id']}.<br> The Name is {result['name']}. <br> The age is {result['age']}. </h1>"
    #return jsonify({'id': result['id'], 'name': result['name'], 'age': result['age']})


#UPDATE
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    db = get_db()
    name = request.json['name']
    age = request.json['age']
    db.execute('UPDATE users SET name = ?, age = ? WHERE id = ?', [name, age, user_id])
    db.commit()
    return jsonify({'message': 'User updated successfully!'})


#DELETE
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = get_db()
    db.execute('DELETE FROM users WHERE id = ?', [user_id])
    db.commit()
    return jsonify({'message': 'User deleted successfully!'})


if __name__ == '__main__':
    app.run(debug = True)