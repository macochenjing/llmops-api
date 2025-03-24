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
from typing import Dict,Any

from injector import inject
from dataclasses import dataclass
from operator import itemgetter
from internal.exception import FailException
from internal.schema.app_schema import CompletionReq
from internal.service import AppService,VectorDatabaseService
from pkg.response import success_json, validate_error_json
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.tracers import Run
from langchain_core.runnables import RunnablePassthrough,RunnableLambda,RunnableConfig
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.memory import BaseMemory
from langchain_core.output_parsers import StrOutputParser

#from internal.core.tools.builtin_tools.providers import BuiltinProviderManager

@inject
@dataclass
class AppHandler:
    """应用控制器"""

    app_service: AppService
    vector_database_service: VectorDatabaseService

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

    @classmethod
    def _load_memory_variables(cls, input: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        '''
        加载记忆变量信息
        :param input:  字典，键是字符串，值是任意值
        :return:
        '''

        # 1.从config中获取configurable
        configurable = config.get("configurable",{})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            return configurable_memory.load_memory_variables(input)

        return {"history":[]}

    @classmethod
    def _save_context(cls, run_obj:Run, config:RunnableConfig) -> None:
        """
        存储对应的上下文信息到记忆实体中
        :param run_obj:
        :param config:
        :return:
        """
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            configurable_memory.save_context(run_obj.inputs, run_obj.outputs)

    def debug(self, app_id: UUID):
        """聊天接口 简易的RAG"""
        # 1.提取从接口中获取的输入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.创建prompt与记忆
        system_prompt = "你是一个强大的聊天机器人，能根据对应的上下文和历史对话信息回复用户问题。\n\n<context>{context}</context>"
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
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

        # 4.创建链应用
        retriever = self.vector_database_service.get_retriever() | self.vector_database_service.combine_documents
        chain = (RunnablePassthrough.assign(
            history=RunnableLambda(self._load_memory_variables) | itemgetter("history"),
            context=itemgetter("query") | retriever
        ) | prompt | llm | StrOutputParser()).with_listeners(on_end=self._save_context)

        # 5.调用链生成内容
        chain_input = {"query": req.query.data}
        content = chain.invoke(chain_input, config={"configurable": {"memory": memory}})

        return success_json({"content": content})

    # def debug(self, app_id: UUID):
    #     """聊天接口 添加侦听器 钩子"""
    #
    #     # 1.提取从接口中获取的输入
    #     req = CompletionReq()
    #     if not req.validate():
    #         return validate_error_json(req.errors)
    #
    #     # 2.创建prompt与记忆
    #     prompt = ChatPromptTemplate.from_messages([
    #         ("system","你是一个强大的聊天机器人，能够根据用户的提问回复对应的问题"),
    #         MessagesPlaceholder("history"),
    #         ("human", "{query}"),
    #     ])
    #
    #     memory = ConversationBufferWindowMemory(
    #         k=3,
    #         input_key="query",
    #         output_key="output",
    #         return_messages=True,
    #         chat_memory=FileChatMessageHistory("./storage/memory/chat_history.txt"),
    #     )
    #
    #     # 3.创建llm
    #     llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
    #
    #     # 4.创建应用
    #     chain = (RunnablePassthrough.assign(
    #         history=RunnableLambda(self._load_memory_variables) | itemgetter("history")
    #     )| prompt | llm | StrOutputParser()).with_listeners(on_end=self._save_context)
    #
    #     # 5.调用链生成内容
    #     chain_input = {"query": req.query.data}
    #     content = chain.invoke(chain_input, config={"configurable":{"memory":memory}})
    #
    #     return success_json({"content": content})

    # def debug(self, app_id: UUID):
    #     """聊天接口 添加记忆"""
    #
    #     # 1.提取从接口中获取的输入
    #     req = CompletionReq()
    #     if not req.validate():
    #         return validate_error_json(req.errors)
    #
    #     # 2.创建prompt与记忆
    #     prompt = ChatPromptTemplate.from_messages([
    #         ("system","你是一个强大的聊天机器人，能够根据用户的提问回复对应的问题"),
    #         MessagesPlaceholder("history"),
    #         ("human", "{query}"),
    #     ])
    #
    #     memory = ConversationBufferWindowMemory(
    #         k=3,
    #         input_key="query",
    #         output_key="output",
    #         return_messages=True,
    #         chat_memory=FileChatMessageHistory("./storage/memory/chat_history.txt"),
    #     )
    #
    #     # 3.创建llm
    #     llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
    #
    #     # 4.创建应用
    #     chain = RunnablePassthrough.assign(
    #         history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
    #     )| prompt | llm | StrOutputParser()
    #
    #     # 5.调用链生成内容
    #     chain_input = {"query": req.query.data}
    #     content = chain.invoke(chain_input)
    #     memory.save_context(chain_input, {"output": content})
    #
    #
    #
    #     # # 版本3 langchain 链实现
    #     # # 2.构建组件
    #     # prompt = ChatPromptTemplate.from_template("{query}")
    #     # llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
    #     # parser = StrOutputParser()
    #     #
    #     # # 3.构建链
    #     # chain = prompt | llm | parser
    #     #
    #     # # 4.调用链
    #     # content = chain.invoke({"query":req.query.data})
    #
    #     return success_json({"content": content})

    # def completion(self):
    #     """聊天接口 基础与链实现"""
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

    @classmethod
    def _combine_documents(cls, documents: list[Document]) -> str:
        """将传入的文档列表合并成字符串"""
        return "\n\n".join([document.page_content for document in documents])

    def ping(self):
        raise FailException("数据未找到")
        # return {"ping":"pong"}