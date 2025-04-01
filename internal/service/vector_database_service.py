# -*- coding: utf-8 -*-

"""
@Time   : 2025/3/3 04:28
@Author : chenjingmaco@gmail.com
@File   : vector_database_service.py
"""
import os

import weaviate
from injector import inject
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore
from weaviate import WeaviateClient


@inject
class VectorDatabaseService:
    """向量数据库服务"""
    client: WeaviateClient
    vector_store: WeaviateVectorStore

    def __init__(self):
        """构造函数，完成向量数据库服务的客户端+LangChain向量数据库实例的创建"""
        # 1.创建/连接weaviate向量数据库
        self.client = weaviate.connect_to_local(
            host=os.getenv("WEAVIATE_HOST"),
            port=int(os.getenv("WEAVIATE_PORT"))
        )

        # 2.创建LangChain向量数据库
        self.vector_store = WeaviateVectorStore(
            client=self.client,
            index_name="Dataset",
            text_key="text",
            embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        )

        # to do close client 要通过包装管理器才行，这里为避免警告提示，直接关闭
        self.client.close()

    def get_retriever(self) -> VectorStoreRetriever:
        """获取检索器"""
        return self.vector_store.as_retriever()

    @classmethod
    def combine_documents(cls, documents: list[Document]) -> str:
        """将对应的文档列表使用换行符进行合并"""
        return "\n\n".join([document.page_content for document in documents])

    def close(self):
        """显式关闭连接"""
        if self.client:
            self.client.close()

