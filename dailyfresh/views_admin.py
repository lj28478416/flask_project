from flask import *
from models import *
from datetime import datetime

from utils.qiniu.qiniu_yun import upload_pic

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
    admin = Userinfo.query.get(int(session['admin']))
    return render_template('admin/index.html',admin=admin)
@admin_blueprint.route('/user_count')
def user_count():
    all_count = Userinfo.query.filter(Userinfo.isAdmin!=True).count()
    now= datetime.now()
    n_mouth = datetime(now.year,now.month,1)
    n_day = datetime(now.year,now.month,now.day)
    m_new_user = Userinfo.query.filter( Userinfo.create_time>=n_mouth).count()
    d_new_user = Userinfo.query.filter( Userinfo.create_time>=n_day).count()
    now_d = '%d-%d-%d' % (now.year, now.month, now.day)
    redis_cli = current_app.click_redis
    time_list = [time.decode() for time in redis_cli.hkeys(now_d)]
    user_count = [count.decode() for count in redis_cli.hvals(now_d)]
    return render_template('admin/user_count.html',all_count=all_count,m_new_user=m_new_user, \
                           d_new_user=d_new_user,time_list=time_list,user_count=user_count)
@admin_blueprint.route('/user_list')
def user_list():
    users = Userinfo.query.order_by(Userinfo.create_time.desc())
    # 接收当前页码值，如果未传递，则显示第1页
    page = int(request.args.get('page', '1'))
    # 对数据进行分页，每页显示2条数据
    pagination = users.paginate(page, 9, False)
    # 获取当前页的数据
    users = pagination.items
    # 获取总页数
    total_page = pagination.pages
    # 显示到模板中
    return render_template('admin/user_list.html',users=users,total_page=total_page,page=page)
@admin_blueprint.route('/news_edit',methods=['POST','GET'])
def new_edit():
    page = int(request.args.get('page', '1'))
    if request.method == 'GET' and not request.args.get('page'):
        current_app.new_edit_news = News.query.order_by(News.publish_time.desc())
    elif request.method == 'POST':
        key_words = request.form.get('keys_words')
        page = 1
        if key_words:
            current_app.new_edit_news = News.query.filter(News.name.contains(key_words)).order_by(News.publish_time.desc())
        else:
            current_app.new_edit_news = News.query.order_by(News.publish_time.desc())
        # 接收当前页码值，如果未传递，则显示第1页
    # 对数据进行分页，每页显示2条数据
    pagination = current_app.new_edit_news.paginate(page, 10, False)
    # 获取当前页的数据
    news = pagination.items
    # 获取总页数
    total_page = pagination.pages
    # 显示到模板中
    return render_template('admin/news_edit.html',news=news,total_page=total_page,page=page)
@admin_blueprint.route('/news_edit_detail',methods=['POST','GET'])
def new_edit_detail():
    if request.method == 'GET':
        new_id = int(request.args.get('id'))
        new = News.query.get(new_id)
        newsclasses = NewsClasses.query.all()
        return render_template('admin/news_edit_detail.html',new=new,newsclasses=newsclasses)
    else:
        new_id = int(request.form.get('news_id'))
        news=News.query.get(new_id)
        new_name = request.form.get('news_name')
        news_class = request.form.get('news_class')
        new_abstract = request.form.get('new_abstract')
        content = request.form.get('content')
        print(new_name,news_class,new_abstract,content)
        pic = request.files.get('pic')
        if pic:
            pic = upload_pic(pic)
            news.news_pic = pic
        if not all([new_name,news_class,new_abstract,content]):
            return '不能有空'
        news.name = new_name
        news.news_classes=news_class
        news.abstract = new_abstract
        news.msg = content
        news.check_statu = 1
        db.session.commit()
        return redirect(url_for('admin.new_edit'))
@admin_blueprint.route('/news_type',methods=['POST','GET'])
def new_type():
    if request.method == 'GET':
        classes = NewsClasses.query.all()
        return render_template('admin/news_type.html',classes=classes)
    else:
        dict1 = request.form
        class_id =int(dict1.get('id'))
        if class_id == 0:
            class1 = NewsClasses()
            class1.name = dict1.get('class')
            db.session.add(class1)
            db.session.commit()
            return redirect(url_for('admin.new_type'))
        else:
            class1 = NewsClasses.query.get(class_id)
            class1.name = dict1.get('class')
            db.session.add(class1)
            db.session.commit()
            return redirect(url_for('admin.new_type'))
@admin_blueprint.route('/logout')
def logout():
    del session['admin']
    return redirect(url_for('news.admin'))
@admin_blueprint.route('/news_review',methods=['POST','GET'])
def news_review():
    page = int(request.args.get('page', '1'))
    if request.method == 'GET' and not request.args.get('page'):
        current_app.new_edit_news = News.query.filter_by(check_statu=3).order_by(News.publish_time.desc())
    elif request.method == 'POST':
        key_words = request.form.get('keys_words')
        page = 1
        if key_words:
            current_app.new_edit_news = News.query.filter(News.name.contains(key_words),News.check_statu==3).order_by(
                News.publish_time.desc())
        else:
            current_app.new_edit_news = News.query.filter_by(check_statu=3).order_by(News.publish_time.desc())
        # 接收当前页码值，如果未传递，则显示第1页
    # 对数据进行分页，每页显示2条数据
    pagination = current_app.new_edit_news.paginate(page, 10, False)
    # 获取当前页的数据
    news = pagination.items
    # 获取总页数
    total_page = pagination.pages
    # 显示到模板中
    return render_template('admin/news_review.html',news=news,total_page=total_page,page=page)
@admin_blueprint.route('/news_review_detail',methods=['POST','GET'])
def news_review_detail():
    if request.method == 'GET':
        new_id = int(request.args.get('id'))
        new = News.query.get(new_id)
        return render_template('admin/news_review_detail.html',new=new)
    else:
        dict1 = request.form
        print(dict1)
        news = News.query.get(int(dict1.get('news_id')))
        if dict1.get('action')=='accept':
            news.check_statu = 1
            db.session.add(news)
            db.session.commit()
        elif dict1.get('action')=='reject':
            news.check_statu = 2
            news.reason=dict1.get('reason')
            db.session.add(news)
            db.session.commit()
        return redirect(url_for('admin.news_review'))