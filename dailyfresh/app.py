import redis
from flask import *
from config import Config
import logging
from logging.handlers import RotatingFileHandler
from flask_session import Session
import os
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Session(app)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 设置日志的记录等级
    logging.basicConfig(level=logging.DEBUG)  # 调试debug级
    log_dir = os.path.join(BASE_DIR, "logs/t1.log")
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler(log_dir, maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式：日志等级、输入日志信息的文件名、行数、日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象添加日记录器
    logging.getLogger().addHandler(file_log_handler)
    app.click_redis = redis.StrictRedis(host=app.config.get('REDIS_HOST'), port=app.config.get('REDIS_PORT'), db=app.config.get('REDIS_DB'))
    app.logger_xjzx = logging
    return app
