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
            topics = ForumTopic.get_all_topics()
            print("Forum Topics:", topics)
            return topics
        except Exception as e:
            print("Error getting forum topics:", str(e))
            return None

    def create_forum_topic(self, user_id, username, title, content):
        try:
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

    def create_reply(self, user_id, topic_id, content):
        try:
            username = request.user.name
            ForumPost.create_post(topic_id, user_id, content, username)
            posts = ForumPost.get_posts_for_topic(topic_id)
            return posts
        except Exception as e:
            print("Error creating forum reply:", str(e))
            return None

    def get_forum_topics_with_posts(self):
        try:
            topics = ForumTopic.get_all_topics()
            for topic in topics:
                posts = ForumPost.get_posts_for_topic(topic.id)
                topic.posts = posts

            return topics
        except Exception as e:
            print("Error getting forum topics:", str(e))
            return None
