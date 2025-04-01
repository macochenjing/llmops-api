# -*- coding: utf-8 -*-

"""
@Time   : 2024/12/27 14:18
@Author : chenjingmaco@gmail.com
@File   : test.py
"""
#
# from datetime import datetime
# import dotenv
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_deepseek import ChatDeepSeek
#
# dotenv.load_dotenv()
#
# '''
# * deepseek-chat 模型已全面升级为 DeepSeek-V3，接口不变。 通过指定 model='deepseek-chat' 即可调用 DeepSeek-V3。
# * deepseek-reasoner 是 DeepSeek 最新推出的推理模型 DeepSeek-R1。通过指定 model='deepseek-reasoner'，即可调用 DeepSeek-R1。
# DeepSeek-R1（通过 指定model="deepseek-reasoner"）不支持工具调用或结构化输出。这些功能由 DeepSeek-V3（通过 指定）支持model="deepseek-chat"。
# '''
#
# # 1.编排prompt
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是聊天机器人，请回答用户问题"),
#     ("human", "{query}"),
# ])
#
# # 2.创建大语言模型
# llm = ChatDeepSeek(
#     model="deepseek-chat",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     # other params...
# )
#
# #ai_message = llm.invoke(prompt.invoke({"query": "请你写一首乡村音乐的歌，歌词主要描述黄花风铃木盛开，春天的美好，柔情，轻松越快的心情，少女情怀，未来充满希望的歌曲"}))
# ai_message = llm.invoke(prompt.invoke(
#     {
#         "query":
#         """
#         from torch.utils.data import DataLoader 原型是怎样的
#         """
#
#     }))
#
# print(ai_message.type)
# print(ai_message.content)
# print(ai_message.response_metadata)


import os
import weaviate

client = weaviate.connect_to_local(
            host="127.0.0.1",
            port=int("8080")
        )

client.close()