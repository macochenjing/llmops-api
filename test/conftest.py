# -*- coding: utf-8 -*-

"""
@Time   : 2024/12/30 14:13
@Author : chenjingmaco@gmail.com
@File   : conftest.py
"""

#
# import pytest
# from app.http.llmapp import appserver # 通过正式环境的app去导出其测试的client
#
# @pytest.fixture
# def client():
#     """获取Flask应用的测试应用，并返回"""
#     appserver.config["TESTING"] = True
#     with appserver.test_client() as client:
#         yield client # 不使用return的好处是：便于上下文管理，使用完会回到此处，可以继续往后执行，比如可能需要清理资源等等


import pytest
from sqlalchemy.orm import sessionmaker, scoped_session

from app.http.llmapp import appserver as _app
from internal.extension.database_extension import db as _db


@pytest.fixture
def app():
    """获取Flask应用并返回"""
    _app.config["TESTING"] = True
    return _app


@pytest.fixture
def client(app):
    """获取Flask应用的测试应用，并返回"""
    with app.test_client() as client:
        yield client


@pytest.fixture
def db(app):
    """创建一个临时的数据库会话，当测试结束的时候回滚整个事务，从而实现测试与数据实际隔离"""
    with app.app_context():
        # 1.获取数据库连接并创建事务
        connection = _db.engine.connect()
        transaction = connection.begin()

        # 2.创建一个临时数据库会话
        session_factory = sessionmaker(bind=connection)
        session = scoped_session(session_factory)
        _db.session = session

        # 3.抛出数据库实例
        yield _db

        # 4.回退数据库并关闭连接，随后清除会话
        transaction.rollback()
        connection.close()
        session.remove()