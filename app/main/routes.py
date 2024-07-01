from app.main import bp
from app.main.services import MainService
from app.main.repositories import FlashcardRepository

main_service = MainService(FlashcardRepository())

@bp.route('/')
def index():
    return main_service.index()

@bp.route('/study')
def study():
    return main_service.study()

@bp.route('/check_answer', methods=['POST'])
def check_answer():
    return main_service.check_answer()

@bp.route('/finish')
def finish():
    return main_service.finish()

@bp.route('/reset_session')
def reset_session():
    return main_service.reset_session()

@bp.route('/study_reverse')
def study_reverse():
    return main_service.study_reverse()

@bp.route('/add_word', methods=['GET', 'POST'])
def add_word():
    return main_service.add_word()

@bp.route('/check-word', methods=['GET'])
def check_word():
    return main_service.check_word()
