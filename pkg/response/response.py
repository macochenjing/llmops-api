# -*- coding: utf-8 -*-

"""
@Time   : 2024/12/29 15:49
@Author : chenjingmaco@gmail.com
@File   : response.py
"""


from dataclasses import field, dataclass
from typing import Any, Union, Generator

from flask import jsonify, stream_with_context, Response as FlaskResponse

from .http_code import HttpCode

@dataclass   # 默认生成构造函数
class Response:
    """基础HTTP接口响应格式"""
    code: HttpCode = HttpCode.SUCCESS
    message: str = ""

    # Any表示可以是任何类型，这里默认设置为一个空字典
    data: Any = field(default_factory=dict)


def json(data: Response = None):
    """基础的响应接口"""

    response = jsonify(data)

    # 解决跨域

    # 方案1 直接在响应头添加相关字段

    # # 添加跨域响应头
    # response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5173'
    # response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    # response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    # response.headers['Access-Control-Allow-Credentials'] = 'true'
    #
    # return response, 200

    return response, 200

def success_json(data: Any = None):
    """成功数据响应"""
    return json(Response(code=HttpCode.SUCCESS, message="", data=data))


def fail_json(data: Any = None):
    """失败数据响应"""
    return json(Response(code=HttpCode.FAIL, message="", data=data))


def validate_error_json(errors: dict = None):
    """数据验证错误响应"""
    first_key = next(iter(errors))
    if first_key is not None:
        msg = errors.get(first_key)[0]
    else:
        msg = ""
    return json(Response(code=HttpCode.VALIDATE_ERROR, message=msg, data=errors))


def message(code: HttpCode = None, msg: str = ""):
    """基础的消息响应，固定返回消息提示，数据固定为空字典"""
    return json(Response(code=code, message=msg, data={}))


def success_message(msg: str = ""):
    """成功的消息响应"""
    return message(code=HttpCode.SUCCESS, msg=msg)


def fail_message(msg: str = ""):
    """失败的消息响应"""
    return message(code=HttpCode.FAIL, msg=msg)


def not_found_message(msg: str = ""):
    """未找到消息响应"""
    return message(code=HttpCode.NOT_FOUND, msg=msg)


def unauthorized_message(msg: str = ""):
    """未授权消息响应"""
    return message(code=HttpCode.UNAUTHORIZED, msg=msg)


def forbidden_message(msg: str = ""):
    """无权限消息响应"""
    return message(code=HttpCode.FORBIDDEN, msg=msg)

def compact_generate_response(response: Union[Response, Generator]) -> FlaskResponse:
    """统一合并处理块输出以及流式事件输出"""
    # 1.检测下是否为块输出(Response)
    if isinstance(response, Response):
        return json(response)
    else:
        # 2.response格式为生成器，代表本次响应需要执行流式事件输出
        def generate() -> Generator:
            """构建generate函数，流式从response中获取数据"""

            '''
            yield from response
            将当前生成器的执行权 临时转移 给另一个生成器（response），并直接 逐项 从该生成器中获取数据，
            再通过当前生成器向外传递.
            相当于以下代码的简写：
                for item in response:  # 遍历 response 生成器的每一项
                    yield item         # 将 item 传递给外层生成器
            '''
            yield from response

        # 3.返回携带上下文的流式事件输出
        return FlaskResponse(
            stream_with_context(generate()),
            status=200,
            mimetype="text/event-stream",
        )