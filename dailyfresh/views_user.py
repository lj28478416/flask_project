from flask import *
from models import *
from utils.qiniu.qiniu_yun import upload_pic
import re

user_blueprint = Blueprint('user', __name__, url_prefix='/user',static_folder='static/news/')

@user_blueprint.before_request
def before_request():
    if session.get('id') != None and session.get('id') == session['id']:
        g.userinfo = Userinfo.query.filter(Userinfo.id == session['id']).first()
    else:
        return redirect(url_for('news.not_find'))
@user_blueprint.route('/user_base_info',methods=['POST','GET'])
def user_base_info():
    if request.method == 'GET':
        return render_template('news/user_base_info.html',userinfo=g.userinfo)
    else:
        dict1 = request.form
        signature = dict1.get('signature')
        nick_name = dict1.get('nick_name')
        gender = dict1.get('gender')
        g.userinfo.signature = signature
        g.userinfo.nick_name = nick_name
        g.userinfo.gender = int(gender)
        db.session.add(g.userinfo)
        db.session.commit()
        return jsonify(result=nick_name)
@user_blueprint.route('/user_pic_info',methods=['GET','POST'])
def user_pic_info():
    if request.method == 'GET':
        return render_template('news/user_pic_info.html',userinfo=g.userinfo)
    else:
        avater = request.files.get('portrait')
        avater_name = upload_pic(avater)
        g.userinfo.avatar = avater_name
        db.session.add(g.userinfo)
        db.session.commit()
        return jsonify(result = g.userinfo.avatar_get)
@user_blueprint.route('/user_follow')
def user_follow():
    # 接收当前页码值，如果未传递，则显示第1页
    page = int(request.args.get('page', '1'))
    # 对数据进行分页，每页显示2条数据
    pagination = g.userinfo.follow_user.paginate(page, 4, False)
    # 获取当前页的数据
    userinfos = pagination.items
    # 获取总页数
    total_page = pagination.pages
    # 显示到模板中
    return render_template('news/user_follow.html',userinfos=userinfos,total_page=total_page,page=page)
# @user_blueprint.route('/del_follow')
# def del_follow():
#     userid = request.args.get('id')
#     userinfos = g.userinfo.follow_user.all()
#     # g.userinfo.follow_user.get(userid).fans_count -= 1
#     print(userinfos)
#     for userinfo in userinfos:
#         if userinfo.id == int(userid):
#             userinfos.remove(userinfo)
#     print(userinfos)
#     # db.session.add(g.userinfo)
#     db.session.commit()
#     return render_template('news/user_follow.html',userinfos=userinfos)
@user_blueprint.route('/user_pass_info',methods=["POST",'GET'])
def user_pass_info():
    if request.method == 'GET':
        return render_template('news/user_pass_info.html')
    else:
        dict1 = request.form
        old_pwd = dict1.get('old_pwd')
        new_pwd = dict1.get('new_pwd')
        if g.userinfo.check_pwd(old_pwd):
            if re.match(r'^[a-z0-9A-Z.+*/]{6,20}$',new_pwd):
                g.userinfo.password(new_pwd)
                db.session.add(g.userinfo)
                db.session.commit()
                return jsonify(result=1)
            else:
                return jsonify(result=3)
        else:
            return jsonify(result=2)
@user_blueprint.route('/user_collection')
def user_collection():
    # 接收当前页码值，如果未传递，则显示第1页
    page = int(request.args.get('page', '1'))
    # 对数据进行分页，每页显示2条数据
    pagination = g.userinfo.collect.order_by(News.publish_time.desc()).paginate(page, 6, False)
    # 获取当前页的数据
    collections = pagination.items
    # 获取总页数
    total_page = pagination.pages
    # 显示到模板中
    return render_template('news/user_collection.html',collections=collections, page = page ,total_page=total_page)
@user_blueprint.route('/user_news_release',methods=['GET','POST'])
def user_news_release():
    newsclasses = NewsClasses.query.all()
    if request.method == 'GET':
        return render_template('news/user_news_release.html',newsclasses =newsclasses)
    else:
        news_pic = request.files.get('news_pic')
        dict1 = request.form
        news = News()
        news.name = dict1.get('name')
        news.news_classes=int(dict1.get('news_classes'))
        news.abstract = dict1.get('abstract')
        news.msg = dict1.get('content')
        news.check_statu = 3
        news.user = g.userinfo.id
        print(news.name, news.abstract, news.msg,news_pic)
        if not all([news.name, news.abstract, news.msg,news_pic]):
            return jsonify(result='error')
        pic_name = upload_pic(news_pic)
        news.news_pic = pic_name
        db.session.add(news)
        db.session.commit()
        return jsonify(result='success')
@user_blueprint.route('/user_news_list')
def user_news_list():
    # 接收当前页码值，如果未传递，则显示第1页
    page = int(request.args.get('page', '1'))
    # 对数据进行分页，每页显示2条数据
    pagination = g.userinfo.news.order_by(News.publish_time.desc()).paginate(page, 6, False)
    # 获取当前页的数据
    user_news = pagination.items
    # 获取总页数
    total_page = pagination.pages
    # 显示到模板中
    return render_template('news/user_news_list.html',user_news=user_news,total_page=total_page,page=page)
@user_blueprint.route('/user_news_change',methods=['GET','POST'])
def user_news_change():
    newsclasses = NewsClasses.query.all()
    news_id = int(request.args.get('id'))
    news = News.query.get(news_id)
    if request.method == 'GET':
        return render_template('news/user_news_change.html',news =news,newsclasses=newsclasses)
    else:
        news_pic = request.files.get('news_pic')
        dict1 = request.form
        news = News()
        news.name = dict1.get('name')
        news.news_classes = int(dict1.get('news_classes'))
        news.abstract = dict1.get('abstract')
        news.msg = dict1.get('content')
        news.check_statu = 3
        news.user = g.userinfo.id
        if not all([news.name, news.abstract, news.msg, news_pic]):
            print('error')
            return jsonify(result='error')
        pic_name = upload_pic(news_pic)
        print('success')
        news.news_pic = pic_name
        db.session.add(news)
        db.session.commit()
        return jsonify(result='success')