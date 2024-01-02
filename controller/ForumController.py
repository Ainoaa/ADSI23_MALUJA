from flask import request

from model import Connection, ForumTopic, ForumPost
from model.ForumTopic import ForumTopic
from model.ForumPost import ForumPost

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

    def create_forum_topic(self, user_id, username, title, content):
        try:
            # Utiliza directamente la conexión para interactuar con la base de datos
            db.insert("INSERT INTO ForumTopic (user_id, username, title, content) VALUES (?, ?, ?, ?)",
                      (user_id, username, title, content))
            print("Topic created successfully.")
        except Exception as e:
            print("Error creating forum topic:", str(e))

    def get_forum_posts_for_topic(self, topic_id):
        try:
            posts = ForumPost.get_posts_for_topic(topic_id)
            print("Forum Posts:", posts)
            return posts
        except Exception as e:
            print("Error getting forum posts:", str(e))
            return None

    def create_forum_post(self, user_id, topic_id, content):
        try:
            ForumPost.create_post(topic_id, user_id, content)
            print("Post created successfully.")
        except Exception as e:
            print("Error creating forum post:", str(e))

    def create_reply(self, user_id, topic_id, content):
        try:
            # Obtiene el nombre de usuario del objeto de usuario en la solicitud
            username = request.user.name
            # Implementa la lógica para crear un nuevo mensaje en el foro y guardarlo en la base de datos
            ForumPost.create_post(topic_id, user_id, content, username)
            # Después de insertar el nuevo mensaje, obtener los mensajes actualizados del tema
            posts = ForumPost.get_posts_for_topic(topic_id)
            # Redirigir a la página del foro con los mensajes actualizados
            return posts
        except Exception as e:
            print("Error creating forum reply:", str(e))
            return None

    def get_forum_topics_with_posts(self):
        try:
            topics = ForumTopic.get_all_topics()
            # Obtén las respuestas para cada tema y agrúpalas
            for topic in topics:
                posts = ForumPost.get_posts_for_topic(topic.id)
                topic.posts = posts

            return topics
        except Exception as e:
            print("Error getting forum topics:", str(e))
            return None
