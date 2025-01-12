# -*- coding: utf-8 -*-

"""
@Time   : 2024/12/27 20:49
@Author : chenjingmaco@gmail.com
@File   : llmapp.py
"""




import dotenv
from injector import Injector
from flask_migrate import Migrate

from config import LLmConfig

from internal.router import Router
from internal.server import Http
from pkg.sql import SQLAlchemy
from app.http.module import ExtensionModule

# 初始化加载.env文件中所有定义的变量到环境变量中
dotenv.load_dotenv()

conf = LLmConfig()

injector = Injector([ExtensionModule])


appserver = Http(
    __name__,
    conf=conf,
    db=injector.get(SQLAlchemy),
    migrate=injector.get(Migrate),
    router=injector.get(Router)
)

if __name__ == "__main__":
    appserver.run(debug=True)