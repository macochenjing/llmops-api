#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/6/3 10:29
@Author : chenjingmaco@gmail.com
@File    : chat.py
"""
from langchain_ollama import ChatOllama

from internal.core.language_model.entities.model_entity import BaseLanguageModel


class Chat(ChatOllama, BaseLanguageModel):
    """Ollama聊天模型"""
    pass
