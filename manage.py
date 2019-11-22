from flask_script import Manager
from flask_migrate import migrate,MigrateCommand
from app_demo import app
from exts import db


manager = Manager(app)
#使用Migrate绑定app和db
migrate = migrate(app,db)
#添加迁移脚本的命令到manager中
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()