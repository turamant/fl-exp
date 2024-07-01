FLASK_APP - указывает на файл, который является точкой входа в ваше Flask-приложение.

FLASK_ENV - устанавливает режим работы Flask-приложения (например, development, production, testing).

FLASK_DEBUG - включает или отключает режим отладки для вашего приложения (обычно True для разработки).

SECRET_KEY - секретный ключ, который используется для защиты сессий и других данных в Flask.

DATABASE_URL - URL базы данных, который указывает Flask на используемую базу данных.

export FLASK_APP=manage.py
export FLASK_ENV=development
export FLASK_DEBUG=1
export SECRET_KEY=your_secret_key
export DATABASE_URL=sqlite:///your_database.db
