import redis
import os
class Config():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.102.136:3306/flask_project'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # redis配置
    REDIS_HOST = "192.168.102.136"
    REDIS_PORT = 6379
    REDIS_DB = 10
    # session
    SECRET_KEY = "flask_project"
    # flask_session的配置信息
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)  # 使用 redis 的实例
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 14  # session 的有效期，单位是秒

    # 表示项目的根目录
    # __file__==>当前文件名config.py
    # os.path.abspath()==>获取文件的绝对路径，/home/python/Desktop/sz10_flask/xjzx/config.py
    # os.path.dirname()==>获取路径的目录名，/home/python/Desktop/sz10_flask/xjzx
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 七牛云配置
    QINIU_AK = 'KbRsuh4zNcrFbm9coAy5EQd6TIygquYndiJvtpFa'
    QINIU_SK = 'FjDPu0WO2SMUg_k7sTnMwDhzOiPIL_-0_EI9FTIJ'
    QINIU_BUCKET = 'zikobe'
    QINIU_URL = 'http://o80vsdrfw.bkt.clouddn.com/'
