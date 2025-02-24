# -*- coding: utf-8 -*-

"""
@Time   : 2024/12/27 14:18
@Author : chenjingmaco@gmail.com
@File   : test.py
"""

#
# from injector import Injector,inject
#
# class A:
#     name: str = "hello llmops"
#
# @inject
# class B:
#
#     #@inject
#     def __init__(self, a: A):
#         self.a = a
#     def print(self):
#         print(f"class A's name: {self.a.name}")
#
# injecobj = Injector()
# b_instance = injecobj.get(B)
# b_instance.print()
#
# for i in range(1,10):
#     print(i)

from typing import List,Optional

class Solution:

    maxlist = []
    maxlen = 0

    def copy_to_max(self, curlist: List[int]):
        self.maxlist = [num for num in curlist]

    def compare_best(self, curlist: List[int]):

        if len(curlist) < len(self.maxlist):
            return

        if len(curlist) > len(self.maxlist):
            self.copy_to_max(curlist)

        for i in range(0, len(curlist)):

            if curlist[i] < self.maxlist[i]:
                return
            if curlist[i] == self.maxlist[i]:
                continue
            self.copy_to_max(curlist)

            return


    def input_next_position(self, leftsourcelist: List[int], flagdict: dict, curlist: List[int], nextpos: int) -> Optional[int]:

        # 如果maxlist达到了最大长度2n-1，则每次递归前可以判断curlist前缀是否有可能大于maxlist,如果不能则直接放弃递归
        if len(self.maxlist) >= self.maxlen:
            for i in range(0, len(curlist)):
                # 等位相同的继续比较
                # 等位小于maxlist的curlist不可能出现最优，直接返回
                if curlist[i] < self.maxlist[i]:
                    print("curlist:",curlist)
                    print("maxlist:",self.maxlist)
                    return i
                # 等位大于maxlist的curlist可能会比maxlist优，则跳出循环，继续往下执行
                if curlist[i] > self.maxlist[i]:
                    break


        # 1. 每一次递归，开始循环前,先判断当前位置是否被之前的数字限定(数字i要出现两
        #    次，并且距离为i,通过flagdict标记判断),如果倍限定,则使用限定数字填充,然
        #    后直到当前位置未被限定

        while nextpos > 0 and flagdict.get(nextpos):
            curlist.append(flagdict[nextpos])
            nextpos += 1

        # 2. 当leftsourcelist中无数字，与maxlist比较哪个最优，然后回溯
        if len(leftsourcelist) <= 0:
            self.compare_best(curlist)
            return

        com = None
        # 3. 使用leftsourcelist中的数字填充, 并且使用flagdict标记限定位置(数字1不能限定),然后继续下一个位置的递归
        for i in range(0, len(leftsourcelist)):

            if com is not None and com == nextpos:
                # 当前位置不能比maxlist对应的com位置大是没希望最优的
                if leftsourcelist[i] < self.maxlist[com]:
                    continue

                # 有希望是最优的，则重置com, 然后下一个递归中可以与maxlist继续比较
                com = None

            # 1不能限定
            if leftsourcelist[i] != 1:
                # 先判断是否有冲突，限定的数字不能被占用，如果被占用则是有冲突的，跳过当前数字
                newpos = len(curlist)
                newlimitindex = newpos + leftsourcelist[i]
                if flagdict.get(newlimitindex):
                    continue
                # 标记
                flagdict[newlimitindex] = leftsourcelist[i]

            # 将未被限定数字添加到当前序列后面
            curlist.append(leftsourcelist[i])

            newpos = len(curlist)
            # 计算剩余列表
            newleft = leftsourcelist[0:i] + leftsourcelist[i+1:]

            # 下一次递归
            com = self.input_next_position(newleft, flagdict, curlist, newpos)

            # 回溯回来需要修正flagdict与curlist
            # 去掉当前数字限定的标记
            if leftsourcelist[i] != 1:
                del flagdict[newlimitindex]

            #截取curlist
            curlist = curlist[0:newpos-1]

            # 没希望比当前maxlist更好，则继续回退到com位置
            if com is not None:
                if com < nextpos:
                    return com


    def constructDistancedSequence(self, n: int) -> List[int]:
        # 1. 定义初始化全局变量--当前最长有效序列:maxlist,初始化[1,n]的未被使用或填充到序
        #    列的数字列表: leftsourcelist,标记位字典:flagdict,
        #    当前列表:curlist,下个位置nextpos
        #    (0开始)
        # 2. 编写递归函数，将leftsourcelist,flagdict,curlist,nextpos传递给递
        #    归函数

        if n < 1 or n > 20:
            return None

        tl = [i for i in range(1, n + 1)]
        leftsourcelist = tl[::-1]
        flagdict = {}
        curlist = []
        nextpos = 0
        self.maxlen = 2*n-1

        self.input_next_position(leftsourcelist, flagdict, curlist, nextpos)

        return self.maxlist


ts = Solution()

print(ts.constructDistancedSequence(12))