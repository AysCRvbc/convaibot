import os
import sqlite3
import json


class BotDatabase:
    def __init__(self, path):
        self.path = path
        if not os.path.exists("data"):
            os.mkdir("data")
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY,
                bind_id INTEGER,
                bind_name TEXT,
                description TEXT
            );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                conversation_id INTEGER,
                message_json TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            );
        ''')
        self.connection.commit()

    def add_conversation(self, id, bind_id, bind_name, description):
        self.cursor.execute('''
            INSERT INTO conversations (id, bind_id, bind_name, description)
            VALUES (?, ?, ?, ?)
        ''', (id, bind_id, bind_name, description))
        self.connection.commit()

    def get_conversations(self):
        self.cursor.execute('''
            SELECT *
            FROM conversations
        ''')
        return self.cursor.fetchall()

    def get_conversation_by_id(self, id):
        self.cursor.execute('''
            SELECT *
            FROM conversations
            WHERE id = ?
        ''', (id,))
        return self.cursor.fetchone()

    def exists_conversation_by_id(self, id):
        self.cursor.execute('''
            SELECT EXISTS (
                SELECT 1
                FROM conversations
                WHERE id = ?
            )
        ''', (id,))
        return self.cursor.fetchone()[0]

    def get_conversations_by_bind_id(self, bind_id):
        self.cursor.execute('''
            SELECT *
            FROM conversations
            WHERE bind_id = ?
        ''', (bind_id,))
        return self.cursor.fetchall()

    def insert_json_message(self, conversation_id, json_message):
        self.cursor.execute('''
            INSERT INTO messages (conversation_id, message_json)
            VALUES (?, ?);
        ''', (conversation_id, json.dumps(json_message)))
        self.connection.commit()

    def get_all_messages_for_conversation(self, conversation_id):
        self.cursor.execute('''
            SELECT message_json FROM messages
            WHERE conversation_id = ?;
        ''', (conversation_id,))
        messages_data = self.cursor.fetchall()
        return [json.loads(message[0]) for message in messages_data]

    def close(self):
        self.connection.close()
