#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/6/4 18:51
@Author  : thezehui@gmail.com
@File    : 1.bind函数使用技巧.py
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("human", "{query}")
])

# 停止词传递-1
# llm = ChatOpenAI(model="gpt-4o", model_kwargs={"stop":"world"}) # 注意这里的停止词有随机性 因为输出是一个token一个token输出，同一个词在不同语义下解析的token数不一样，所以就可能检测不到world

# 停止词传递-2
# chain = prompt | llm.bind(stop="世界") | StrOutputParser()

llm = ChatOpenAI(model="gpt-3.5-turbo")

chain = prompt | llm.bind(model="gpt-4o") | StrOutputParser()

content = chain.invoke({"query": "你是什么模型呢？"})

print(content)
