# -*- coding: utf-8 -*-

"""
@Time   : 2024/12/31 14:54
@Author : chenjingmaco@gmail.com
@File   : default_config.py
"""

# 应用默认配置项
DEFAULT_CONFIG = {

    #wtf配置
    "WTF_CSRF_ENABLED": "False",

    # SQLAlchemy数据库配置
    "SQLALCHEMY_DATABASE_URI": "",
    "SQLALCHEMY_POOL_SIZE": 30,
    "SQLALCHEMY_POOL_RECYCLE": 3600,
    "SQLALCHEMY_ECHO": "True",
}