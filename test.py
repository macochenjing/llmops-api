# -*- coding: utf-8 -*-

"""
@Time   : 2024/12/27 14:18
@Author : chenjingmaco@gmail.com
@File   : test.py
"""

from injector import Injector,inject

class A:
    name: str = "hello llmops"

@inject
class B:

    #@inject
    def __init__(self, a: A):
        self.a = a
    def print(self):
        print(f"class A's name: {self.a.name}")

injecobj = Injector()
b_instance = injecobj.get(B)
b_instance.print()