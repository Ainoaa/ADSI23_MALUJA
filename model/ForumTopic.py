from model import Connection

db = Connection()

class ForumTopic:
    def __init__(self, id, title, user_id):
        self.id = id
        self.title = title
        self.user_id = user_id

    def __str__(self):
        return f"Topic ID: {self.id}, Title: {self.title}, User ID: {self.user_id}"

    @staticmethod
    def create_topic(user_id, title):
        # Lógica para crear un nuevo tema en la base de datos
        db.execute("INSERT INTO forum_topics (user_id, title) VALUES (?, ?)", (user_id, title))
        db.commit()

    @staticmethod
    def get_all_topics():
        # Lógica para obtener todos los temas desde la base de datos
        result = db.select("SELECT * FROM forum_topics")
        return [ForumTopic(*row) for row in result]