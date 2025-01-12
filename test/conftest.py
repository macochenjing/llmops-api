# -*- coding: utf-8 -*-

"""
@Time   : 2024/12/30 14:13
@Author : chenjingmaco@gmail.com
@File   : conftest.py
"""

import pytest
from app.http.llmapp import appserver # 通过正式环境的app去导出其测试的client

@pytest.fixture
def client():
    """获取Flask应用的测试应用，并返回"""
    appserver.config["TESTING"] = True
    with appserver.test_client() as client:
        yield client # 不使用return的好处是：便于上下文管理，使用完会回到此处，可以继续往后执行，比如可能需要清理资源等等


