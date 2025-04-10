# -*- coding: utf-8 -*-

"""
@Time   : 2025/4/10 17:01
@Author : chenjingmaco@gmail.com
@File   : demo_task.py
"""

import logging
import time
from uuid import UUID

from celery import shared_task
from flask import current_app


# 使用这个装饰器，直接将函数变成异步任务
@shared_task
def demo_task(id: UUID) -> str:
    """测试异步任务"""
    logging.info("睡眠5秒")
    time.sleep(5)
    logging.info(f"id的值:{id}")
    logging.info(f"配置信息:{current_app.config}")
    return "慕小课"
