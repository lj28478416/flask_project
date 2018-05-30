from flask import *
from models import *
import re
import random
from utils.ytx_sdk import sms_yzm
from utils.captcha.captcha import captcha

news_blueprint = Blueprint('news', __name__, url_prefix='/news',static_folder='static/news/')

@news_blueprint.before_request
def before_request():
    if request.args.get('logout') == 'true':
        if session.get('id'):
            del session['id']
    if session.get('id') != None and session.get('id') == session['id']:
        userinfo = Userinfo.query.filter(Userinfo.id == session['id']).first()
        g.logined = 'true'
        g.nick_name = userinfo.nick_name
    else:
        g.logined = 'false'
        g.nick_name = 'null'
@news_blueprint.route('/index')
def index():
    news = News.query.all()
    return render_template('news/index.html',logined=g.logined,nick_name=g.nick_name,news=news)
@news_blueprint.route('/notfind',methods = ['POST','GET'])
def not_find():
    return render_template('news/404.html', logined=g.logined, nick_name=g.nick_name)
@news_blueprint.route('/user')
def user():
    if g.logined == 'true':
        return render_template('news/user.html',logined = g.logined,nick_name = g.nick_name)
    else:
        return redirect(url_for('news.index'))
@news_blueprint.route('/detail')
def detail():
    return render_template('news/detail.html', logined=g.logined, nick_name=g.nick_name)
@news_blueprint.route('/other')
def other():
    return render_template('news/other.html', logined=g.logined, nick_name=g.nick_name)
@news_blueprint.route('/login',methods=['POST'])
def login():
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    userinfo = Userinfo.query.filter(Userinfo.mobile == mobile).first()
    if userinfo != None and userinfo.check_pwd(password):
        session['id'] = '%s' % userinfo.id
        return jsonify(state='success',nick_name=userinfo.nick_name)
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
            session['admin'] = '%s' % password
            return redirect(url_for('admin.index'))
        else:
            return render_template('admin/login.html')