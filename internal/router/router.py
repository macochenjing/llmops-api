# -*- coding: utf-8 -*-

"""
@Time   : 2024/12/27 16:35
@Author : chenjingmaco@gmail.com
@File   : router.py
"""

from injector import inject
from dataclasses import dataclass

from flask import Flask, Blueprint
from internal.handler import AppHandler


@inject
@dataclass #简化注入的代码逻辑, 无需构造函数__init__(), 它会默认生成构造函数
class Router:
    """路由"""
    app_handler: AppHandler

    def register_router(self, app: Flask):
        """注册路由"""
        # 1.创建一个蓝图
        bp = Blueprint("llmops", __name__, url_prefix="")

        # 2.将url与对应的控制器方法做绑定
        # bp.add_url_rule("/ping", view_func=self.app_handler.ping)

        bp.add_url_rule("/apps/<uuid:app_id>/debug", methods=["POST"], view_func=self.app_handler.debug)

        # bp.add_url_rule("/app", methods=["POST"], view_func=self.app_handler.create_app)
        #
        # # <uuid:id> uuid是类型, 绑定了id
        # bp.add_url_rule("/app/<uuid:id>", view_func=self.app_handler.get_app)
        #
        # # <uuid:id> uuid是类型, 绑定了id
        # bp.add_url_rule("/app/<uuid:id>", methods=["POST"], view_func=self.app_handler.update_app)
        #
        # # <uuid:id> uuid是类型, 绑定了id
        # bp.add_url_rule("/app/<uuid:id>/delete", methods=["POST"], view_func=self.app_handler.delete_app)

        # 3.在应用上去注册蓝图
        app.register_blueprint(bp)
