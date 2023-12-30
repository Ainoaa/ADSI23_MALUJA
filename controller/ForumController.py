from model import Connection, ForumTopic

db = Connection()


class ForumController:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ForumController, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def get_forum_topics(self):
        try:
            # Llama al método estático directamente
            topics = ForumTopic.get_all_topics()
            print("Forum Topics:", topics)
            return topics
        except Exception as e:
            print("Error getting forum topics:", str(e))
            return None

    def get_forum_topic_by_id(self, topic_id):
        # Implementa la lógica para obtener un tema específico por su ID
        pass

    def create_forum_topic(self, user_id, title, content):
        try:
            # Utiliza directamente la conexión para interactuar con la base de datos
            db.insert("INSERT INTO ForumTopic (user_id, title, content) VALUES (?, ?, ?)", (user_id, title, content))
            print("Topic created successfully.")
        except Exception as e:
            print("Error creating forum topic:", str(e))

    def get_forum_posts_for_topic(self, topic_id):
        # Implementa la lógica para obtener mensajes relacionados con un tema específico
        pass

    def create_forum_post(self, user_id, topic_id, content):
        # Implementa la lógica para crear un nuevo mensaje en el foro y guardarlo en la base de datos
        pass
