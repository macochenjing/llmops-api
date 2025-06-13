# -*- coding: utf-8 -*-

"""
@Time   : 2025/3/3 04:28
@Author : chenjingmaco@gmail.com
@File   : vector_database_service.py
"""

import os

import weaviate
from injector import inject
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_weaviate import WeaviateVectorStore
from weaviate import WeaviateClient
from weaviate.collections import Collection

from .embeddings_service import EmbeddingsService

# 向量数据库的集合名字
COLLECTION_NAME = "Dataset"


@inject
class VectorDatabaseService:
    """向量数据库服务"""
    client: WeaviateClient
    vector_store: WeaviateVectorStore
    embeddings_service: EmbeddingsService

    def __init__(self, embeddings_services: EmbeddingsService):
        """构造函数，完成向量数据库服务的客户端+LangChain向量数据库实例的创建"""
        # 1.赋值embeddings_service
        self.embeddings_service = embeddings_services

        # 2.创建/连接weaviate向量数据库
        self.client = weaviate.connect_to_local(
            host=os.getenv("WEAVIATE_HOST"),
            port=int(os.getenv("WEAVIATE_PORT"))
        )

        # 3.创建LangChain向量数据库
        self.vector_store = WeaviateVectorStore(
            client=self.client,
            index_name=COLLECTION_NAME,
            text_key="text",
            embedding=self.embeddings_service.cache_backed_embeddings
            # embedding=self.embeddings_service.embeddings,
        )

        # 避免警告，这里先关
        self.client.close()

    def get_retriever(self) -> VectorStoreRetriever:
        """获取检索器"""
        return self.vector_store.as_retriever()

    @property
    def collection(self) -> Collection:
        return self.client.collections.get(COLLECTION_NAME)