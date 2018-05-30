from flask import *
from models import *
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
        return render_template('news/user_pic_info.html')
    else:

@user_blueprint.route('/user_follow')
def user_follow():
    userinfos = g.userinfo.follow_user.all()
    return render_template('news/user_follow.html',userinfos=userinfos)
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
    collections = g.userinfo.collect
    return render_template('news/user_collection.html',collections=collections)
@user_blueprint.route('/user_news_release')
def user_news_release():
    return render_template('news/user_news_release.html')
@user_blueprint.route('/user_news_list')
def user_news_list():
    user_news = g.userinfo.news
    return render_template('news/user_news_list.html',user_news=user_news)