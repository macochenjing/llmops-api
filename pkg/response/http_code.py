# -*- coding: utf-8 -*-

"""
@Time   : 2024/12/29 15:43
@Author : chenjingmaco@gmail.com
@File   : http_code.py
"""

from enum import Enum


class HttpCode(str, Enum): # 表示它的枚举值是字符串类型，可以拥有与字符串所有的属性和方法, 就是说它可与字符直接比较，也可以直接序列化等等
    """HTTP基础业务状态码"""
    SUCCESS        = "success"                  # 成功状态码
    FAIL           = "fail"                     # 失败状态码
    NOT_FOUND      = "not_found"                # 未找到
    UNAUTHORIZED   = "unautorized"              # 未授权
    FORBIDDEN      = "forbidden"                # 无权限
    VALIDATE_ERROR = "validate_error"           # 数据验证错误