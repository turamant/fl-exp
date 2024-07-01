import random
from flask import (render_template, request,
                   redirect, url_for, jsonify, flash, session)
from app.main import bp
from app.models import Flashcard
from flask_login import current_user, login_required, logout_user
from app.models import db


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Flashcard.query.paginate(page=page, per_page=per_page)
    flashcards = pagination.items

    if current_user.is_authenticated:
        return render_template('main/index.html',
                               username=current_user.username,
                               flashcards=flashcards,
                               pagination=pagination)
    else:
        return render_template('main/index.html', 
                               username=None,
                               flashcards=flashcards,
                               pagination=pagination)
    

@bp.route('/add_word', methods=['GET', 'POST'])
@login_required
def add_word():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        flashcard = Flashcard(question=question, answer=answer)
        db.session.add(flashcard)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('main/add_word.html', username=current_user.username)


@bp.route('/study', methods=['GET'])
def study():
    all_words = Flashcard.query.all()
    total_words = len(all_words)
    
    # Сохраняем общее количество слов в сессии
    session['total_words'] = total_words
    
    # Получаем текущий индекс слова из сессии
    current_index = session.get('current_index', 0)
    
    if current_index >= total_words:
        return redirect(url_for('main.finish'))
    
    # Получаем текущее слово по индексу
    flashcard = all_words[current_index]
    
    question = flashcard.question
    correct_answer = flashcard.answer
    
    all_answers = [word.answer for word in Flashcard.query.filter(Flashcard.question != question).all()]
    wrong_answers = random.sample(all_answers, 2)
    
    answer_options = [correct_answer] + wrong_answers
    random.shuffle(answer_options)
    
    # Сохраняем текущий индекс в сессии
    session['current_index'] = current_index + 1
    
    return render_template('study/study.html', question=question, options=answer_options, 
                           correct_answer=correct_answer, total_words=total_words,
                           total_correct=session.get('total_correct', 0), 
                           current_index=current_index + 1, username=current_user.username)

    
@bp.route('/check_answer', methods=['POST'])
def check_answer():
    selected_answer = request.form['answer']
    correct_answer = request.form['correct_answer']
    
    if selected_answer == correct_answer:
        session['total_correct'] = session.get('total_correct', 0) + 1
        flash('Correct!', 'success')
    else:
        flash('Incorrect!', 'danger')
    
    return redirect(url_for('main.study'))
    
@bp.route('/finish', methods=['GET'])
def finish():
    total_words = session.get('total_words', 0)
    total_correct = session.get('total_correct', 0)

    if total_words > 0:
        percentage = round((total_correct / total_words) * 100)
        message = f'{percentage}% of correct answers ({total_correct}/{total_words})'
    else:
        message = "No words to evaluate"

    # Сохраняем результаты в сессии
    session['finish_message'] = message

    return render_template('study/finish.html',
                           message=message,
                           username=current_user.username)


@bp.route('/reset_session', methods=['GET'])
def reset_session():
    # Сбрасываем данные из сессии, кроме информации о пользователе
    session.pop('current_index', None)
    session.pop('total_correct', None)
    
    # Перенаправляем пользователя на главную страницу
    return redirect(url_for('main.index'))


@bp.route('/check-word', methods=['GET'])
def check_word():
    word = request.args.get('word')
    if Flashcard.query.filter_by(question=word).first() or Flashcard.query.filter_by(answer=word).first():
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})
    
    
@bp.route('/study_reverse', methods=['GET'])
def study_reverse():
    all_words = Flashcard.query.all()
    total_words = len(all_words)
    
    session['total_words'] = total_words
    current_index = session.get('current_index', 0)
    
    if current_index >= total_words:
        return redirect(url_for('main.finish'))
    
    flashcard = all_words[current_index]
    
    # Меняем местами question и answer
    question = flashcard.answer
    correct_answer = flashcard.question
    
    all_answers = [word.question for word in Flashcard.query.filter(Flashcard.answer != correct_answer).all()]
    wrong_answers = random.sample(all_answers, 2)
    
    answer_options = [correct_answer] + wrong_answers
    random.shuffle(answer_options)
    
    session['current_index'] = current_index + 1
    
    return render_template('study/study.html',
                           question=question,
                           options=answer_options,
                           correct_answer=correct_answer,
                           total_words=total_words,
                           total_correct=session.get('total_correct', 0), 
                           current_index=current_index + 1,
                           username=current_user.username)