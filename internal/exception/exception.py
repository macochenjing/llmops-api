# -*- coding: utf-8 -*-

"""
@Time   : 2024/12/29 17:38
@Author : chenjingmaco@gmail.com
@File   : exception.py
"""

from dataclasses import field
from typing import Any
from pkg.response import HttpCode

class CustomException(Exception):
    """基础自定义异常信息"""

    code: HttpCode = HttpCode.FAIL
    message: str = ""
    data: Any = field(default_factory=dict)

    def __init__(self, message: str = None, data: Any = None):
        super().__init__()
        self.message = message
        self.data = data

class FailException(CustomException):
    """通用失败异常"""
    pass

class NotFoundException(CustomException):
    """未找到异常"""
    code = HttpCode.NOT_FOUND

class UnauthorizedException(CustomException):
    """未授权异常"""
    code = HttpCode.UNAUTHORIZED

class ForbiddenException(CustomException):
    """无权限异常"""
    code = HttpCode.FORBIDDEN

class ValidateErrorException(CustomException):
    """验证异常"""
    code = HttpCode.VALIDATE_ERROR

# e1 = UnauthorizedException(message="e1", data={"e1":1})
# e2 = ValidateErrorException(message="e2", data={"e2":1})
#
# print(e1.code, e1.message, e1.data)
# print(e2.code, e2.message, e2.data)

# ex1 = CustomException(message="Custom message")
# ex2 = CustomException()
#
# print(ex1.message)  # "Custom message" (实例属性覆盖类属性)
# print(ex2.message)  # "Default message" (引用了类属性)