from flask import *
from models import *

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin', static_folder='static/admin/')
@admin_blueprint.before_request
def session_verify():
    if 'admin' in session and session.get('admin') == session['admin']:
        pass
    else:
        return redirect(url_for('news.admin'))
@admin_blueprint.route('/')
def index1():
    return redirect(url_for('news.admin'))
@admin_blueprint.route('/index')
def index():
    return render_template('admin/index.html')
@admin_blueprint.route('/user_count')
def user_count():
    return render_template('admin/user_count.html')
@admin_blueprint.route('/user_list')
def user_list():
    return render_template('admin/user_list.html')
@admin_blueprint.route('/news_edit')
def new_edit():
    return render_template('admin/news_edit.html')
@admin_blueprint.route('/news_edit_detail.html')
def new_edit_detail():
    return render_template('admin/news_edit_detail.html')
@admin_blueprint.route('/news_type')
def new_type():
    return render_template('admin/news_type.html')
@admin_blueprint.route('/logout')
def logout():
    del session['admin']
    return redirect(url_for('news.admin'))
@admin_blueprint.route('/news_review')
def news_review():
    return render_template('admin/news_review.html')
@admin_blueprint.route('/news_review_detail')
def news_review_detail():
    return render_template('admin/news_review_detail.html')
