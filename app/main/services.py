import random
from flask import (render_template, request, redirect, url_for, jsonify, flash, session)
from app.models import Flashcard
from flask_login import current_user, login_required, logout_user
from app.main.repositories import FlashcardRepository

class MainService:
    def __init__(self, flashcard_repo: FlashcardRepository):
        self.flashcard_repo = flashcard_repo

    def index(self):
        flashcards = self.flashcard_repo.get_all()
        if current_user.is_authenticated:
            return render_template('main/index.html',
                                   username=current_user.username,
                                   flashcards=flashcards)
        else:
            return render_template('main/index.html', 
                                   username=None,
                                   flashcards=flashcards)

    @login_required
    def add_word(self):
        if request.method == 'POST':
            question = request.form['question']
            answer = request.form['answer']
            flashcard = Flashcard(question=question, answer=answer)
            self.flashcard_repo.add(flashcard)
            return redirect(url_for('main.index'))
        return render_template('main/add_word.html')

    def study(self):
        all_words = self.flashcard_repo.get_all()
        total_words = len(all_words)
        session['total_words'] = total_words

        current_index = session.get('current_index', 0)
        if current_index >= total_words:
            return redirect(url_for('main.finish'))

        flashcard = all_words[current_index]
        question = flashcard.question
        correct_answer = flashcard.answer

        all_answers = [word.answer for word in self.flashcard_repo.get_all_except(question)]
        wrong_answers = random.sample(all_answers, 2)
        answer_options = [correct_answer] + wrong_answers
        random.shuffle(answer_options)

        session['current_index'] = current_index + 1
        return render_template('study/study.html', question=question, options=answer_options,
                               correct_answer=correct_answer, total_words=total_words,
                               total_correct=session.get('total_correct', 0),
                               current_index=current_index + 1)

    def check_answer(self):
        selected_answer = request.form['answer']
        correct_answer = request.form['correct_answer']

        if selected_answer == correct_answer:
            session['total_correct'] = session.get('total_correct', 0) + 1
            flash('Correct!', 'success')
        else:
            flash('Incorrect!', 'danger')

        return redirect(url_for('main.study'))

    def finish(self):
        total_words = session.get('total_words', 0)
        total_correct = session.get('total_correct', 0)

        if total_words > 0:
            percentage = round((total_correct / total_words) * 100)
            message = f'{percentage}% of correct answers ({total_correct}/{total_words})'
        else:
            message = "No words to evaluate"

        session['finish_message'] = message
        return render_template('study/finish.html', message=message)

    def reset_session(self):
        session.pop('current_index', None)
        session.pop('total_correct', None)
        return redirect(url_for('main.index'))

    def check_word(self, word):
        if self.flashcard_repo.get_by_question(word) or self.flashcard_repo.get_by_answer(word):
            return jsonify({'exists': True})
        else:
            return jsonify({'exists': False})
        
    def study_reverse(self):
        all_words = self.flashcard_repo.get_all()
        total_words = len(all_words)
        session['total_words'] = total_words

        current_index = session.get('current_index', 0)
        if current_index >= total_words:
            return redirect(url_for('main.finish'))

        flashcard = all_words[current_index]

        # Swap the question and answer
        question = flashcard.answer
        correct_answer = flashcard.question

        all_answers = [word.question for word in self.flashcard_repo.get_all_except(correct_answer)]
        wrong_answers = random.sample(all_answers, 2)

        answer_options = [correct_answer] + wrong_answers
        random.shuffle(answer_options)

        session['current_index'] = current_index + 1

        return render_template('study/study.html', question=question, options=answer_options,
                            correct_answer=correct_answer, total_words=total_words,
                            total_correct=session.get('total_correct', 0),
                            current_index=current_index + 1)
