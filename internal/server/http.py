# -*- coding: utf-8 -*-

"""
@Time   : 2024/12/27 20:43
@Author : chenjingmaco@gmail.com
@File   : http.py
"""
import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from config import LLmConfig
from internal.router import Router
from internal.extension import logging_extension,redis_extension
from internal.exception import CustomException
from pkg.response import json, Response, HttpCode
from pkg.sql import SQLAlchemy
from internal.model import App

class Http(Flask):
    """Http服务引擎"""

    def __init__(self,
                 *args,
                 conf: LLmConfig,
                 db: SQLAlchemy,
                 migrate: Migrate,
                 router: Router,
                 **kwargs
    ):

        # 1.调用父类构造函数初始化
        super().__init__(*args, **kwargs)

        # 2.初始化应用配置
        self.config.from_object(conf)

        # 3.注册绑定异常错误处理函数
        self.register_error_handler(Exception, self._register_error_handler)

        # 4.初始化flask扩展
        # 初始化数据库
        db.init_app(self)

        # 初始化数据库迁移的目录
        migrate.init_app(self, db, directory="internal/migration")

        # 初始化redis
        redis_extension.init_app(self)

        # 初始化日志记录器
        logging_extension.init_app(self)

        # # 如果表不存在，则创建；已经使用了migrate做版本管理这里全部注释
        # with self.app_context():
        #     _ = App() # 确保能够检索到这个App model, 就是说如果未使用到App这个类是不会去创建
        #     db.create_all()

        # 5.解决前后端跨域问题 方案2
        CORS(self, resources={
            r"/*":{
                "origins":'*',
                "supports_credentials":True,
                # "methods":["GET","POST"],
                # "allow_headers":["Content-Type"],
            }
        })

        # 6.注册应用路由
        router.register_router(self)

    def _register_error_handler(self, error: Exception):

        # 1.日志记录异常信息
        logging.error("An error occurred: %s", error, exc_info=True)

        # 2.判断异常信息是不是我们的自定义异常，如果是则可以提取message和code等信息
        if isinstance(error, CustomException):
            return json(Response(
                code=error.code,
                message=error.message,
                data=error.data if error.data is not None else {},
            ))

        # 3.如果不是我们自定义的异常，则有可能是程序、数据库等抛出的异常，也可以提取信息，设置为FAIL状态码
        if self.debug or os.getenv("FLASK_ENV") == "development":
            raise error
        else:
            return json(Response(
                code=HttpCode.FAIL,
                message=str(error),
                data={},
            ))

