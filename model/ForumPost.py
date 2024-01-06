from model import Connection

db = Connection()


class ForumPost:
    def __init__(self, id, topic_id, user_id, content, username, created_at):
        self.id = id
        self.topic_id = topic_id
        self.user_id = user_id
        self.content = content
        self.username = username
        self.created_at = created_at

    def __str__(self):
        return f"Post ID: {self.id}, Topic ID: {self.topic_id}, User ID: {self.user_id}, Content: {self.content}"

    @staticmethod
    def create_post(topic_id, user_id, content, username):
        try:
            db.insert("INSERT INTO forum_posts (topic_id, user_id, content, username) VALUES (?, ?, ?, ?)",
                      (topic_id, user_id, content, username))

            db.commit()
            print("Post created successfully.")
        except Exception as e:
            print("Error creating forum post:", str(e))

    @staticmethod
    def get_posts_for_topic(topic_id):
        try:
            result = db.select("SELECT * FROM forum_posts WHERE topic_id = ?", (topic_id,))
            return [ForumPost(*row) for row in result]
        except Exception as e:
            print("Error getting forum posts for topic:", str(e))
            return []