# -*- coding: utf-8 -*-

"""
@Time   : 2025/1/7 17:52
@Author : chenjingmaco@gmail.com
@File   : app_service.py
"""
import uuid

from injector import inject
from dataclasses import dataclass

from pkg.sql import SQLAlchemy
from internal.model import App

@inject
@dataclass
class AppService:
    """应用服务器逻辑"""
    db: SQLAlchemy

    def create_app(self) -> App:

        # 版本1
        # # 1.创建模型的视图类
        # appobj = App(name="测试机器人", account_id=uuid.uuid4(), icon="", description="这是一个简单的聊天机器人")
        #
        # # appobj.name =  "测试机器人"
        # # appobj.description = "这是一个简单的聊天机器人"
        #
        # # 2.将实体类添加到session会话中
        # self.db.session.add(appobj)
        #
        # # 3.提交session会话
        # self.db.session.commit()
        #
        # return appobj

        # 版本2
        with self.db.auto_commit():
            # 1.创建模型的视图类
            appobj = App(name="测试机器人", account_id=uuid.uuid4(), icon="", description="这是一个简单的聊天机器人")
            self.db.session.add(appobj)
        return appobj

    def get_app(self, id: uuid.UUID) -> App:
        appobj = self.db.session.query(App).get(id)
        return appobj

    def update_app(self, id: uuid.UUID) -> App:

        with self.db.auto_commit():
            appobj = self.get_app(id)
            appobj.name = "测试聊天机器人"
        return appobj

    def delete_app(self, id: uuid.UUID) -> App:

        with self.db.auto_commit():
            appobj = self.get_app(id)
            self.db.session.delete(appobj)
        return appobj

