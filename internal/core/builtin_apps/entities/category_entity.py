# -*- coding: utf-8 -*-

"""
@Time   : 2025/5/31 07:52
@Author : chenjingmaco@gmail.com
@File   : category_entity.py
"""

from pydantic import BaseModel, Field


class CategoryEntity(BaseModel):
    """内置工具分类实体"""
    category: str = Field(default="")  # 分类唯一标识
    name: str = Field(default="")  # 分类对应的名称
