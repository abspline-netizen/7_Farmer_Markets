
import sqlite3
from review_file.review_model import ReviewManager

class ReviewController:
    def __init__(self, model):
        self.model = model

    def comment_all(self):
        return self.model.review_all()

    def comment_add(self, user_name, rating, comment):
        return self.model.review_add(user_name, rating, comment)

    def comment_delete(self, review_id):
        return self.model.delete_review(review_id)


if __name__ == "__main__":
    pass


