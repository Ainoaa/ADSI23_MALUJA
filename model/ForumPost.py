from model import Connection

db = Connection()

class ForumPost:
    def __init__(self, id, topic_id, user_id, content):
        self.id = id
        self.topic_id = topic_id
        self.user_id = user_id
        self.content = content

    def __str__(self):
        return f"Post ID: {self.id}, Topic ID: {self.topic_id}, User ID: {self.user_id}, Content: {self.content}"

    @staticmethod
    def create_post(topic_id, user_id, content):
        # Lógica para crear un nuevo mensaje en el foro en la base de datos
        db.execute("INSERT INTO forum_posts (topic_id, user_id, content) VALUES (?, ?, ?)", (topic_id, user_id, content))
        db.commit()

    @staticmethod
    def get_posts_for_topic(topic_id):
        # Lógica para obtener todos los mensajes relacionados con un tema desde la base de datos
        result = db.select("SELECT * FROM forum_posts WHERE topic_id = ?", (topic_id,))
        return [ForumPost(*row) for row in result]