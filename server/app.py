from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# Route to get all messages
@app.route('/messages', methods=['GET'])
def messages():
    # Fetch all messages from the database, ordered by created_at
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages])

# Route to get a single message by ID
@app.route('/messages/<int:id>', methods=['GET'])
def messages_by_id(id):
    # Fetch the message by ID, return 404 if not found
    message = Message.query.get_or_404(id)
    return jsonify(message.to_dict())

# Route to create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    body = request.json.get('body')
    username = request.json.get('username')
    
    if not body or not username:
        return jsonify({"error": "Missing required fields"}), 400

    new_message = Message(body=body, username=username)
    db.session.add(new_message)
    db.session.commit()

    return jsonify(new_message.to_dict()), 201

# Route to update a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    
    body = request.json.get('body')
    
    if body:
        message.body = body
        db.session.commit()

    return jsonify(message.to_dict())

# Route to delete a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    
    return '', 204

if __name__ == '__main__':
    app.run(port=5555)
