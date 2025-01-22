from datetime import datetime
from app import app
from models import db, Message

class TestApp:
    '''Flask application in app.py'''

    def setup_method(self):
        # Set up: clear existing messages to ensure tests are isolated
        with app.app_context():
            m = Message.query.filter(
                Message.body == "Hello 👋"
            ).filter(Message.username == "Liza")

            for message in m:
                db.session.delete(message)
            db.session.commit()

    def teardown_method(self):
        # Clean up after tests
        with app.app_context():
            m = Message.query.filter(
                Message.body == "Hello 👋"
            ).filter(Message.username == "Liza")

            for message in m:
                db.session.delete(message)
            db.session.commit()

    def test_has_correct_columns(self):
        '''Test to check if message has the correct columns'''
        with app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza"
            )
            db.session.add(hello_from_liza)
            db.session.commit()

            assert(hello_from_liza.body == "Hello 👋")
            assert(hello_from_liza.username == "Liza")
            assert(type(hello_from_liza.created_at) == datetime)

            db.session.delete(hello_from_liza)
            db.session.commit()

    def test_returns_list_of_json_objects_for_all_messages_in_database(self):
        '''Returns a list of JSON objects for all messages in the database'''
        with app.app_context():
            response = app.test_client().get('/messages')
            records = Message.query.all()

            for message in response.json:
                assert(message['id'] in [record.id for record in records])
                assert(message['body'] in [record.body for record in records])

    def test_creates_new_message_in_the_database(self):
        '''Creates a new message in the database'''
        with app.app_context():
            response = app.test_client().post(
                '/messages',
                json={
                    "body": "Hello 👋",
                    "username": "Liza",
                }
            )
            # Updated to expect 201 instead of 200
            assert response.status_code == 201

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)

            db.session.delete(h)
            db.session.commit()

    def test_returns_data_for_newly_created_message_as_json(self):
        '''Returns data for the newly created message as JSON'''
        with app.app_context():
            response = app.test_client().post(
                '/messages',
                json={
                    "body": "Hello 👋",
                    "username": "Liza",
                }
            )

            assert(response.content_type == 'application/json')
            assert(response.json["body"] == "Hello 👋")
            assert(response.json["username"] == "Liza")

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)

            db.session.delete(h)
            db.session.commit()

    def test_updates_body_of_message_in_database(self):
        '''Updates the body of a message in the database'''
        with app.app_context():
            # Create a message first
            hello_from_liza = Message(
                body="Old Body",
                username="Liza"
            )
            db.session.add(hello_from_liza)
            db.session.commit()

            # Update the message's body
            m = Message.query.first()
            id = m.id
            new_body = "Goodbye 👋"
            response = app.test_client().patch(
                f'/messages/{id}',
                json={"body": new_body}
            )

            # Assert the response
            assert(response.status_code == 200)
            assert(response.json["body"] == new_body)

            db.session.delete(m)
            db.session.commit()

    def test_returns_data_for_updated_message_as_json(self):
        '''Returns data for the updated message as JSON'''
        with app.app_context():
            # Create a message first
            hello_from_liza = Message(
                body="Old Body",
                username="Liza"
            )
            db.session.add(hello_from_liza)
            db.session.commit()

            m = Message.query.first()
            id = m.id
            new_body = "Goodbye 👋"
            response = app.test_client().patch(
                f'/messages/{id}',
                json={"body": new_body}
            )

            # Assert the response
            assert(response.content_type == 'application/json')
            assert(response.json["body"] == new_body)

            db.session.delete(m)
            db.session.commit()

    def test_deletes_message_from_database(self):
        '''Deletes the message from the database'''
        with app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza"
            )
            db.session.add(hello_from_liza)
            db.session.commit()

            response = app.test_client().delete(
                f'/messages/{hello_from_liza.id}'
            )
            # Updated to expect 204 instead of 200
            assert response.status_code == 204

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(not h)
