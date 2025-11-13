from .db import SessionLocal
from .models import Texts

class TextsInterface:
    def __init__(self):
        self.session = SessionLocal()

    def get(self, user_id: int):
        return self.session.query(Texts).get(user_id)

    def get_all_texts(self):
        return self.session.query(Texts).all()

