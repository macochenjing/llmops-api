#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/6/3 10:29
@Author : chenjingmaco@gmail.com
@File    : chat.py
"""
from langchain_community.chat_models.moonshot import MoonshotChat

from internal.core.language_model.entities.model_entity import BaseLanguageModel


class Chat(MoonshotChat, BaseLanguageModel):
    """月之暗面聊天模型"""
    pass
