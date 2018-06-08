from flask import *
from models import *
import re
import random
from datetime import datetime
from utils.ytx_sdk import sms_yzm
from utils.captcha.captcha import captcha

news_blueprint = Blueprint('news', __name__, url_prefix='/news',static_folder='static/news/')

@news_blueprint.before_request
def before_request():
    if session.get('id') != None and session.get('id') == session['id']:
        print('have_session')
        g.userinfo = Userinfo.query.filter(Userinfo.id == session['id']).first()
        g.logined = 'true'
        g.nick_name = g.userinfo.nick_name
        g.avatar_get = g.userinfo.avatar_get
    else:
        print('no_session')
        g.logined = 'false'
        g.nick_name = 'null'
        g.avatar_get = 'none'
@news_blueprint.route('/index')
def index():
    new_classes = NewsClasses.query.all()
    hot_news = News.query.filter_by(check_statu=1).order_by(News.click_count.desc())[0:6]
    return render_template('news/index.html',hot_news=hot_news,new_classes=new_classes,logined=g.logined, nick_name=g.nick_name,avatar_get = g.avatar_get)

@news_blueprint.route('/newslist')
def newslist():
    class_id= int(request.args.get('class_id'))
    page = int(request.args.get('page'))
    if class_id==0:
        news_list = News.query.filter_by(check_statu=1).order_by(News.publish_time.desc()).paginate(page,4,False)
        news = news_list.items
        totle_page = news_list.pages
        newslist1=[]
        for new in news:
            new_dict={
                'id':new.id,
                'news_pic_get':new.news_pic_get,
                'name':new.name,
                'abstract':new.abstract,
                'avatar_get':new.author.avatar_get,
                'author_id':new.author.id,
                'nick_name':new.author.nick_name,
                'publish_time': new.publish_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            newslist1.append(new_dict)
        return jsonify(news=newslist1,totle_page=totle_page)
    else:
        news_list = News.query.filter_by(check_statu=1).filter_by(news_classes=class_id).order_by(News.publish_time.desc()).paginate(page,4,False)
        news = news_list.items
        totle_page = news_list.pages
        newslist1=[]
        for new in news:
            new_dict={
                'id':new.id,
                'news_pic_get':new.news_pic_get,
                'name':new.name,
                'abstract':new.abstract,
                'avatar_get':new.author.avatar_get,
                'author_id':new.author.id,
                'nick_name':new.author.nick_name,
                'publish_time':new.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            newslist1.append(new_dict)
        return jsonify(news=newslist1,totle_page=totle_page)
@news_blueprint.route('/notfind',methods = ['POST','GET'])
def not_find():
    return render_template('news/404.html', logined=g.logined, nick_name=g.nick_name,avatar_get = g.avatar_get)
@news_blueprint.route('/user')
def user():
    if g.logined == 'true':
        return render_template('news/user.html',logined = g.logined,nick_name = g.nick_name,avatar_get = g.avatar_get)
    else:
        return redirect(url_for('news.index'))
@news_blueprint.route('/detail')
def detail():
    news_id = request.args.get('new_id')
    news_id = int(news_id)
    news = News.query.get(news_id)
    author = news.author
    hot_news = News.query.filter_by(check_statu=1).order_by(News.click_count.desc())[0:6]
    if g.logined=='true':
        if news not in g.userinfo.collect:
            collect = 1
        else:
            collect = 2
        if author in g.userinfo.follow_user:
            follow = 1
        else:
            follow = 2
    else:
        collect = 3
        follow = 2
    return render_template('news/detail.html', collect=collect, hot_news=hot_news,logined=g.logined, nick_name=g.nick_name,avatar_get = g.avatar_get,news=news, \
                            follow=follow)
@news_blueprint.route('/collect')
def collect():
    if g.logined == 'true':
        news_id = int(request.args.get('news_id'))
        news = News.query.get(news_id)
        if news not in g.userinfo.collect:
            g.userinfo.collect.append(news)
            db.session.commit()
            return jsonify(result=1)
        else:
            return jsonify(result=2)
    else:
        return jsonify(result=3)
@news_blueprint.route('/collected')
def collected():
    if g.logined == 'true':
        news_id = int(request.args.get('news_id'))
        news = News.query.get(news_id)
        if news not in g.userinfo.collect:
            return jsonify(result=2)
        else:
            g.userinfo.collect.remove(news)
            db.session.commit()
            return jsonify(result=1)
    else:
        return jsonify(result=3)
@news_blueprint.route('/comment',methods=['POST'])
def comment():
    if g.logined == 'true':
        news_id = int(request.form.get('news_id'))
        news = News.query.get(news_id)
        news.comment_count += 1
        newscomment = NewsComment()
        newscomment.user = g.userinfo.id
        newscomment.about = news_id
        newscomment.msg = request.form.get('comment')
        db.session.add(newscomment)
        db.session.commit()
        return jsonify(result=1)
    else:
        return jsonify(result=2)
@news_blueprint.route('/comment_list')
def comment_list():
    news_id = int(request.args.get('news_id'))
    news = News.query.get(news_id)
    list1 = news.comment.order_by(NewsComment.publish_time.desc())
    comment_list2 = []
    for com in list1:
        if com.comment_id == None:
            liked = 0
            like_click_list = [int(x) for x in current_app.click_redis.lrange('comment%d' % com.id, 0, -1)]
            if g.logined == 'true':
                if g.userinfo.id in like_click_list:
                    liked = 1
            comment_list = NewsComment.query.filter(NewsComment.comment_id==com.id)
            comment_list1 = []
            for com2 in comment_list:
                dict2={
                    'author':com2.author.nick_name,
                    'msg':com2.msg
                }
                comment_list1.append(dict2)
            dict1 = {
                'avartar':com.author.avatar_get,
                'nick_name':com.author.nick_name,
                'msg':com.msg,
                'publish_time':com.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
                'like_count':com.like_count,
                'liked':liked,
                'id':com.id,
                'comment_list':comment_list1
            }
            comment_list2.append(dict1)
        else:
            pass
    return jsonify(comment_list=comment_list2)
@news_blueprint.route('/follow',methods=['GET','POST'])
def follow():
    if request.method == 'POST':
        action = int(request.form.get('action'))
        author_id = int(request.form.get('author'))
        if g.logined == 'true':
            if action == 1:
                userinfo = Userinfo.query.get(author_id)
                userinfo.fans_count += 1
                g.userinfo.follow_user.append(userinfo)
                db.session.commit()
                return jsonify(result=2)
            else:
                userinfo = Userinfo.query.get(author_id)
                userinfo.fans_count -= 1
                g.userinfo.follow_user.remove(userinfo)
                db.session.commit()
                return jsonify(result=2)
        else:
            return jsonify(result=1)
@news_blueprint.route('/click_like',methods=['POST'])
def click_like():
    if g.logined == 'true':
        if request.form.get('action')=='1':
            comment_id = int(request.form.get('commentid'))
            comment = NewsComment.query.get(comment_id)
            like_click_list = [int(x) for x in current_app.click_redis.lrange('comment%d' % comment_id, 0, -1)]
            if g.userinfo.id not in like_click_list:
                current_app.click_redis.rpush('comment%d'%comment_id,g.userinfo.id)
                comment.like_count += 1
                db.session.commit()
                return jsonify(like_cout=comment.like_count)
            else:
                return jsonify(like_cout = '你个小几把,不按套路来')
        elif request.form.get('action')=='0':
            comment_id = int(request.form.get('commentid'))
            comment = NewsComment.query.get(comment_id)
            like_click_list = [int(x) for x in current_app.click_redis.lrange('comment%d' % comment_id, 0, -1)]
            if g.userinfo.id in like_click_list:
                current_app.click_redis.lrem('comment%d' % comment_id,0,g.userinfo.id)
                comment.like_count -= 1
                db.session.commit()
                return jsonify(like_cout=comment.like_count)
            else:
                return jsonify(like_cout='你个小几把,不按套路来')
        else:
            return jsonify(like_cout='你个小几把,不按套路来')
    else:
        return jsonify(like_cout = '你个小几把,不按套路来')
@news_blueprint.route('/comment_comment',methods=['POST'])
def comment_comment():
    if g.logined == 'true':
        msg = request.form.get('msg')
        comment_id = request.form.get('comment_id')
        news_id = request.form.get('news_id')
        if not all([msg,comment_id,news_id]):
            return jsonify(result = 2)
        news = News.query.get(int(news_id))
        news.comment_count += 1
        comment = NewsComment()
        comment.comment_id = int(comment_id)
        comment.msg = msg
        comment.about = int(news_id)
        comment.user = g.userinfo.id
        db.session.add(comment)
        db.session.commit()
        return jsonify(result=1)
    else:
        return jsonify(result=2)
@news_blueprint.route('/other')
def other():
    user_id = int(request.args.get('id'))
    userinfo = Userinfo.query.get(user_id)
    news = userinfo.news.order_by(News.publish_time.desc())
    # 接收当前页码值，如果未传递，则显示第1页
    page = int(request.args.get('page', '1'))
    # 对数据进行分页，每页显示2条数据
    pagination = news.paginate(page, 6, False)
    # 获取当前页的数据
    news = pagination.items
    # 获取总页数
    total_page = pagination.pages
    # 显示到模板中
    if g.logined == 'true':
        if userinfo in g.userinfo.follow_user:
            follow = 1
        else:
            follow = 2
    else:
        follow = 2
    return render_template('news/other.html', userinfo=userinfo,logined=g.logined, \
                           nick_name=g.nick_name,avatar_get = g.avatar_get,news=news,page=page,total_page=total_page,\
                           user_id=user_id,follow=follow)
@news_blueprint.route('/login',methods=['POST'])
def login():
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    userinfo = Userinfo.query.filter(Userinfo.mobile == mobile).first()
    if userinfo != None and userinfo.check_pwd(password):
        userinfo.publish_time = datetime.now()
        db.session.commit()
        session['id'] = '%s' % userinfo.id
        now = datetime.now()
        now_d = '%d-%d-%d' % (now.year,now.month,now.day)
        redis_cli = current_app.click_redis
        time_list = ["08:15", "09:15", "10:15", "11:15", "12:15", "13:15",
                     "14:15", "15:15", "16:15", "17:15", "18:15","19:15"]
        for index,time in enumerate(time_list):
            if now.hour < (index + 8) or (now.hour==(index + 8) and now.minute <= 15):
                redis_cli.hincrby(now_d, time, 1)
                break
        else:
            redis_cli.hincrby(now_d, "19:15", 1)
        db.session.commit()
        return jsonify(state='success',nick_name=userinfo.nick_name,avatar_get=userinfo.avatar_get)
    else:
        return jsonify(state='failure')
@news_blueprint.route('/pic_verify')
def pic_verify():
    """图片验证码"""
    verify = captcha.generate_captcha()
    session['pic_verify'] = verify[1]
    response = make_response(verify[2])
    # 默认浏览器将数据作为text/html解析
    # 需要告诉浏览器当前数据的类型为image/png
    response.mimetype = 'image/png'
    return response
@news_blueprint.route('/sms_verify',methods=['POST'])
def sms_verify():
    """短信验证码"""
    dict1=request.form
    session['mobile']=dict1.get('mobile')
    pic_code = dict1.get('pic_code').upper()
    #随机生成一个4位的验证码
    yzm=random.randint(1000,9999)
    #将短信验证码进行保存，用于验证
    session['sms_yzm']=yzm
    if pic_code == session['pic_verify']:
        if session['mobile'].isnumeric() and len(session['mobile']) == 11:
            return jsonify(result=2,code = yzm)
        else:
            return jsonify(result=3)
    else:
        return jsonify(result=1)
    #发送短信
    # mobile为发送短信的手机号,yzm2为验证码,5为验证码有效时间5分钟,1为模板id
    # sms_yzm.sendTemplateSMS(mobile,{yzm,5},1)
@news_blueprint.route('/register',methods =['POST'])
def register():
    """验证注册"""
    dict1 = request.form
    print(dict1)
    mobile = dict1.get('mobile')
    sms_code = int(dict1.get('sms_code'))
    pic_code = dict1.get('pic_code').upper()
    pwd = dict1.get('pwd')
    #判断是否为空
    if not all([mobile, pic_code, sms_code, pwd]):
        return jsonify(result = 1)
    #判断手机号码是否存在
    if Userinfo.query.filter(Userinfo.mobile==mobile==session['mobile']).first():
        return jsonify(result = 2)
    #判断验证码是否正确
    if pic_code != session['pic_verify']:
        return jsonify(result = 3)
    #判断手机验证码是否正确
    if sms_code != session['sms_yzm']:
        return jsonify(result = 4)
    #判断密码是否符合规则
    if not re.match(r'[a-z0-9A-Z.+*/]{6,20}',pwd):
        return jsonify(result = 5)
    if Userinfo.query.filter(Userinfo.mobile==mobile==session['mobile']).first() is None and \
            pic_code == session['pic_verify'] and\
            sms_code == session['sms_yzm'] and\
            re.match(r'^[a-z0-9A-Z.+*/]{6,20}$',pwd):
        userinfo = Userinfo()
        userinfo.mobile = mobile
        userinfo.nick_name = mobile
        userinfo.password(pwd)
        db.session.add(userinfo)
        db.session.commit()
        session['id'] = userinfo.id
        return jsonify(result=6)
@news_blueprint.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('admin/login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        super_commend = Userinfo.query.filter(Userinfo.mobile==username).first()
        if super_commend != None and super_commend.check_pwd(password) and super_commend.isAdmin==True:
            session['admin'] = '%s' % super_commend.id
            return redirect(url_for('admin.index'))
        else:
            return render_template('admin/login.html')
@news_blueprint.route('/logout')
def logout():
    if request.args.get('logout') == 'true':
        if session.get('id'):
            del session['id']
            return jsonify(result='success')