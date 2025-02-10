# -*- coding: utf-8 -*-

"""
@Time   : 2024/12/27 16:31
@Author : chenjingmaco@gmail.com
@File   : app_hander.py
"""

import uuid
from uuid import UUID
import os
from openai import OpenAI

from injector import inject
from dataclasses import dataclass
from operator import itemgetter


from internal.exception import FailException
from internal.schema.app_schema import CompletionReq
from internal.service import AppService
from pkg.response import success_json, validate_error_json

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.output_parsers import StrOutputParser


@inject
@dataclass
class AppHandler:
    """应用控制器"""

    app_service: AppService

    def create_app(self):
        """调用服务创建新的APP记录"""
        appobj = self.app_service.create_app()
        return success_json(f"应用已经创建成功，id是: {appobj.id}")

    def get_app(self, id: uuid.UUID):
        appobj = self.app_service.get_app(id)
        return success_json(f"应用已经成功获取，名字是: {appobj.name}")

    def update_app(self, id: uuid.UUID):
        appobj = self.app_service.update_app(id)
        return success_json(f"应用已经成功修改，修改的名字是: {appobj.name}")

    def delete_app(self, id: uuid.UUID):
        appobj = self.app_service.delete_app(id)
        return success_json(f"应用已经成功被删除，id为: {appobj.id}")

    def debug(self, app_id: UUID):
        """聊天接口"""

        # 1.提取从接口中获取的输入
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.创建prompt与记忆
        prompt = ChatPromptTemplate.from_messages([
            ("system","你是一个强大的聊天机器人，能够根据用户的提问回复对应的问题"),
            MessagesPlaceholder("history"),
            ("human", "{query}"),
        ])

        memory = ConversationBufferWindowMemory(
            k=3,
            input_key="query",
            output_key="output",
            return_messages=True,
            chat_memory=FileChatMessageHistory("./storage/memory/chat_history.txt"),
        )

        # 3.创建llm
        llm = ChatOpenAI(model="gpt-3.5-turbo-16k")

        # 4.创建应用
        chain = RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )| prompt | llm | StrOutputParser()

        # 5.调用链生成内容
        chain_input = {"query": req.query.data}
        content = chain.invoke(chain_input)
        memory.save_context(chain_input, {"output": content})



        # # 版本3 langchain 链实现
        # # 2.构建组件
        # prompt = ChatPromptTemplate.from_template("{query}")
        # llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
        # parser = StrOutputParser()
        #
        # # 3.构建链
        # chain = prompt | llm | parser
        #
        # # 4.调用链
        # content = chain.invoke({"query":req.query.data})

        return success_json({"content": content})

    # def completion(self):
    #     """聊天接口"""
    #
    #     # 1.提取从接口中获取的输入
    #     req = CompletionReq()
    #     if not req.validate():
    #         return validate_error_json(req.errors)
    #
    #     # # 版本1 原生的openai实现
    #     # # 2.构建OpenAI客户端，并发起请求
    #     # client = OpenAI(base_url=os.getenv("OPENAI_API_BASE"))
    #     #
    #     # completion = client.chat.completions.create(
    #     #     model="gpt-3.5-turbo-16k",
    #     #     messages=[
    #     #         {"role": "system", "content": "你是OpenAI开发的聊天机器人，请根据用户的输入回复对应的信息"},
    #     #         {"role":"user", "content": req.query.data},
    #     #     ]
    #     # )
    #     #
    #     # # 3.得到请求响应，然后将响应返回给到前端
    #     # content = completion.choices[0].message.content
    #     #
    #     # return success_json({"content": content})
    #
    #     # # 版本2 langchain实现
    #     # # 2.构建prompt
    #     # prompt = ChatPromptTemplate.from_template("{query}")
    #     #
    #     # # 3.实例化OpenAI客户端，并发起请求
    #     # llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
    #     # ai_message = llm.invoke(prompt.invoke({"query":req.query.data}))
    #     # parser = StrOutputParser()
    #     #
    #     # # 4.解析响应内容
    #     # content = parser.invoke(ai_message)
    #
    #     # 版本3 langchain 链实现
    #     # 2.构建组件
    #     prompt = ChatPromptTemplate.from_template("{query}")
    #     llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
    #     parser = StrOutputParser()
    #
    #     # 3.构建链
    #     chain = prompt | llm | parser
    #
    #     # 4.调用链
    #     content = chain.invoke({"query":req.query.data})
    #
    #     return success_json({"content": content})

    def ping(self):
        raise FailException("数据未找到")
        # return {"ping":"pong"}