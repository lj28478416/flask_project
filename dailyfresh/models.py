# 用户表: id,头像,昵称,签名,手机,密码,性别,是否为管理员
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import current_app
import pymysql

from werkzeug.security import generate_password_hash, check_password_hash

pymysql.install_as_MySQLdb()
db = SQLAlchemy()


# 基础表
class Basemodel(object):
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    publish_time = db.Column(db.DateTime, default=datetime.now)
    isdelete = db.Column(db.Boolean, default=False)


# 用户关注表
to_user_user = db.Table(
    'to_user_user',
    # 主动关注别人的用户
    db.Column('origin_user_id', db.Integer, db.ForeignKey('user_info.id'), primary_key=True),
    # 被关注用户
    db.Column('follow_user_id', db.Integer, db.ForeignKey('user_info.id'), primary_key=True)
)



# 用户表
class Userinfo(db.Model, Basemodel):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String(11))
    password_hash = db.Column(db.String(200))
    signature = db.Column(db.String(200))
    nick_name = db.Column(db.String(20))
    gender = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(50), default='FnOpFKZIe8kjEw-QuXamD28sYTXB')
    publish_news_count = db.Column(db.Integer, default=0)
    fans_count = db.Column(db.Integer, default=0)
    isAdmin = db.Column(db.Boolean, default=False)
    # 发布的新闻
    news = db.relationship('News', backref='author', lazy='dynamic')
    # 评论
    comment = db.relationship('NewsComment', backref='author', lazy='dynamic')
    # 自关联多对多
    follow_user = db.relationship(
        'Userinfo',
        secondary=to_user_user,
        lazy='dynamic',
        backref=db.backref('follow_by_user', lazy='dynamic'),
        primaryjoin= (id == to_user_user.c.origin_user_id),
        secondaryjoin= (id == to_user_user.c.follow_user_id)
    )
    #密码加密
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)
    #检查密码
    def check_pwd(self, pwd):
        return check_password_hash(self.password_hash, pwd)
    #取出头像文件名并拼接
    @property
    def avatar_get(self):
        return current_app.config.get('QINIU_URL') + self.avatar



# 新闻分类表
class NewsClasses(db.Model):
    __tablename__ = 'news_classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    news = db.relationship('News', backref='classes', lazy='dynamic')


# 审核表
class Check(db.Model):
    __tablename__ = 'check_news'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    statu = db.relationship('News', backref='check', lazy='dynamic')


# 新闻收藏表
to_news_user = db.Table(
    'to_news_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user_info.id'), primary_key=True),
    db.Column('news_id', db.Integer, db.ForeignKey('news.id'), primary_key=True)
)


# 新闻表
class News(db.Model, Basemodel):
    __tablename__ = 'news'
    name = db.Column(db.String(20))
    # 分类
    news_classes = db.Column(db.Integer, db.ForeignKey('news_classes.id'))
    # 摘要
    abstract = db.Column(db.String(50),default='无摘要')
    # 新闻图片
    news_pic = db.Column(db.String(50),default='FnOpFKZIe8kjEw-QuXamD28sYTXB')
    # 内容
    msg = db.Column(db.Text)
    # 审核状态
    check_statu = db.Column(db.Integer, db.ForeignKey('check_news.id'),default=3)
    # 未通过原因
    reason = db.Column(db.String(50),default='无')
    # 发表用户
    user = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    # 点击量
    click_count = db.Column(db.Integer, default=0)
    # 评论量
    comment_count = db.Column(db.Integer, default=0)
    # 收藏用户
    collect_user = db.relationship('Userinfo', secondary=to_news_user, backref=db.backref('collect', lazy='dynamic'), lazy='dynamic')
    # 新闻评论
    comment = db.relationship('NewsComment', backref='news_about', lazy='dynamic')

    @property
    def news_pic_get(self):
        return current_app.config.get('QINIU_URL') + self.news_pic

# 新闻评论表
class NewsComment(db.Model, Basemodel):
    __tablename__ = 'news_comment'
    # 发表用户
    user = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    # 评论的新闻
    about = db.Column(db.Integer, db.ForeignKey('news.id'))
    # 评论的内容
    msg = db.Column(db.Text)
    # 点赞数量
    like_count = db.Column(db.Integer, default=0)
    # 评论,自关联一对多
    comment_id = db.Column(db.Integer, db.ForeignKey('news_comment.id'))
    comments = db.relationship('NewsComment')
