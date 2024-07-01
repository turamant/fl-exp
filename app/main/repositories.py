from app.models import Flashcard, db

class FlashcardRepository:
    def get_all(self):
        return Flashcard.query.all()

    def get_by_question(self, question):
        return Flashcard.query.filter_by(question=question).first()

    def get_by_answer(self, answer):
        return Flashcard.query.filter_by(answer=answer).first()

    def get_all_except(self, question):
        return Flashcard.query.filter(Flashcard.question != question).all()

    def add(self, flashcard):
        db.session.add(flashcard)
        db.session.commit()