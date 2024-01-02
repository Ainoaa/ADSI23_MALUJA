from model import Connection
from model.ForumPost import ForumPost

db = Connection()

class ForumTopic:
    def __init__(self, id, user_id, username, title, content, created_at):
        self.id = id
        self.user_id = user_id
        self.username = username
        self.title = title
        self.content = content
        self.created_at = created_at
        self.posts = []

    def __str__(self):
        return f"Title: {self.title}, User ID: {self.user_id}"

    @staticmethod
    def create_topic(user_id, username, title):
        try:
            # Lógica para crear un nuevo tema en la base de datos
            db.insert("INSERT INTO ForumTopic (user_id,username, title) VALUES (?, ?)", (user_id, username, title))
            print("Topic created successfully.")
        except Exception as e:
            print(f"Error creating forum topic: {str(e)}")

    @staticmethod
    def get_all_topics():
        try:
            # Lógica para obtener todos los temas desde la base de datos
            result = db.select("SELECT * FROM ForumTopic")
            return [ForumTopic(*row) for row in result]
        except Exception as e:
            print(f"Error al obtener temas del foro: {str(e)}")
            return []

    def get_posts(self):
        try:
            result = db.select("SELECT * FROM forum_posts WHERE topic_id = ?", (self.id,))
            return [ForumPost(*row) for row in result]
        except Exception as e:
            print("Error getting forum posts for topic:", str(e))
            return []

    def add_post(self, post):
        self.posts.append(post)
