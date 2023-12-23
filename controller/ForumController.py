from model import Connection, ForumTopic, ForumPost

db = Connection()

class ForumController:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ForumController, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def get_forum_topics(self):
        # Lógica para obtener temas del foro desde la base de datos
        topics = []  # Agrega la lógica para recuperar temas
        print("Forum Topics:", topics)
        return topics

    def get_forum_topic_by_id(self, topic_id):
        # Lógica para obtener un tema específico del foro por su ID desde la base de datos
        pass

    def create_forum_topic(self, user_id, title, content):
        try:
            new_topic = ForumTopic(user_id=user_id, title=title, content=content)
            db.session.add(new_topic)
            db.session.commit()
            print("Result of topic creation:", new_topic)
            return new_topic
        except Exception as e:
            print("Error creating forum topic:", str(e))
            return None

    def get_forum_posts_for_topic(self, topic_id):
        # Lógica para obtener mensajes relacionados con un tema específico desde la base de datos
        pass

    def create_forum_post(self, user_id, topic_id, content):
        # Lógica para crear un nuevo mensaje en el foro y guardarlo en la base de datos
        pass
