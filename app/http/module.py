# -*- coding: utf-8 -*-

"""
@Time   : 2024/12/31 15:20
@Author : chenjingmaco@gmail.com
@File   : module.py
"""

from pkg.sql import SQLAlchemy
from injector import Binder, Module
from internal.extension.database_extension import db
from flask_migrate import Migrate
from internal.extension.migrate_extension import migrate

class ExtensionModule(Module):
    """扩展模块的依赖注入"""
    def configure(self, binder: Binder) -> None:
        binder.bind(SQLAlchemy, to=db)
        binder.bind(Migrate, to=migrate)

