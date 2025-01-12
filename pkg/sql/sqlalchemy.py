# -*- coding: utf-8 -*-

"""
@Time   : 2025/1/8 14:59
@Author : chenjingmaco@gmail.com
@File   : sqlalchemy.py
"""

from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

class SQLAlchemy(_SQLAlchemy):
    """重写Flask-SQLAlchemy中的核心类，实现自动提交"""

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e