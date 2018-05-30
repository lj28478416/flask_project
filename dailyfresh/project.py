from app import create_app
from flask import *
from views_admin import admin_blueprint
from views_news import news_blueprint
from views_user import user_blueprint
from models import *
from flask_migrate import MigrateCommand,Migrate
from flask_script import Manager
from flask_wtf import CSRFProtect
app = create_app()
db.init_app(app)
CSRFProtect(app)
app.register_blueprint(admin_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(news_blueprint)
@app.route('/')
def index():
    return redirect(url_for('news.index'))
@app.errorhandler(404)
def error_404(status):
    return redirect(url_for('news.not_find'))
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()