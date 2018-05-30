from models import *
super_command = Userinfo()
super_command.mobile = input('用户名')
super_command.password_hash = input('密码')
super_command.isAdmin = True
db.session.add(super_command)