# -*- coding: utf-8 -*-

"""
@Time   : 2024/12/29 11:07
@Author : chenjingmaco@gmail.com
@File   : app_schema.py
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired,length

class CompletionReq(FlaskForm):
    """基础聊天接口请求校验"""
    # 必填、长度最大为2000
    query = StringField("query", validators=[
        DataRequired(message="用户的提问必须填写"),
        length(max=2000, message="用户的提问最大长度是2000"),
    ])

    # 这里还可以设置其它参数
