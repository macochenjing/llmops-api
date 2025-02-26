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

from typing import List, Tuple


class Solution:

    # 将二维矩阵存储到类属性，避免到处传递
    inputgrid = None

    # 当前最长有效序列的下标
    maxseq = []

    # 行数与列数
    ROWS = 0
    COLS = 0

    # 保留当前的最大有效序列长度
    maxlength = 0

    # 定义四个方向
    LEFT_TOP     = 1
    RIGHT_TOP    = 2
    RIGHT_BOTTOM = 3
    LEFT_BOTTOM  = 4

    def condition_required(self, row, col, nextrow, nextcol):

        if nextrow < 0 or nextrow >= self.ROWS or nextcol < 0 or nextcol >= self.COLS:
            return False

        curnum = self.inputgrid[row][col]
        nextnum = self.inputgrid[nextrow][nextcol]

        if (curnum == 1 or curnum == 0) and nextnum == 2:
            return True
        if curnum == 2 and nextnum == 0:
            return True
        return False


    def left_top_search(self, row: int, col: int, turncount: int, depth: int) -> Tuple[int, List[Tuple[int,int]]]:
        nextrow = row-1
        nextcol = col-1
        if not self.condition_required(row, col, nextrow, nextcol):
            return 0, None
        next_directions = [self.LEFT_TOP, self.RIGHT_TOP]
        return self.deep_search(nextrow, nextcol, turncount, self.LEFT_TOP, depth+1, next_directions)

    def left_bottom_search(self, row: int, col: int, turncount: int, depth: int) -> Tuple[int, List[Tuple[int,int]]]:
        nextrow = row + 1
        nextcol = col - 1

        if not self.condition_required(row, col, nextrow, nextcol):
            return 0,None

        next_directions = [self.LEFT_BOTTOM, self.LEFT_TOP]
        return self.deep_search(nextrow, nextcol, turncount, self.LEFT_BOTTOM, depth+1, next_directions)

    def right_top_search(self, row: int, col: int, turncount: int, depth: int) -> Tuple[int, List[Tuple[int,int]]]:
        nextrow = row - 1
        nextcol = col + 1
        if not self.condition_required(row, col, nextrow, nextcol):
            return 0,None
        next_directions = [self.RIGHT_TOP, self.RIGHT_BOTTOM]
        return self.deep_search(nextrow, nextcol, turncount, self.RIGHT_TOP, depth+1, next_directions)

    def right_bottom_search(self, row: int, col: int, turncount: int, depth: int) -> Tuple[int, List[Tuple[int,int]]]:
        nextrow = row + 1
        nextcol = col + 1
        if not self.condition_required(row, col, nextrow, nextcol):
            return 0,None
        next_directions = [self.RIGHT_BOTTOM, self.LEFT_BOTTOM]
        return self.deep_search(nextrow, nextcol, turncount, self.RIGHT_BOTTOM, depth+1, next_directions)

    def deep_search(self, row: int, col: int, turncount: int, curdirect: int, depth: int, directions: List[int]) -> Tuple[int, List[Tuple[int,int]]]:

        curnum = self.inputgrid[row][col]
        # print("deep_search: ", "row:", row, "col:", col, "curnum:", curnum, "directions:", directions)
        maxlen = 0
        maxseq = []
        for direct in directions:
            curlen = 0
            curseq = None
            tmpcount = turncount
            if direct != curdirect: #方向不同就是要旋转
                tmpcount += 1

            print("tmpcount:", tmpcount)
            # 仅仅旋转一次
            if tmpcount <= 1:
                if direct == self.LEFT_TOP:
                    step = row if row < col else col
                    if tmpcount == 0 or (tmpcount == 1 and depth + step > self.maxlength):
                        curlen, curseq = self.left_top_search(row, col, tmpcount, depth)
                elif direct == self.RIGHT_TOP:
                    step = row if row < self.COLS-col-1 else self.COLS-col-1
                    if tmpcount == 0 or (tmpcount == 1 and depth + step > self.maxlength):
                        curlen, curseq = self.right_top_search(row, col, tmpcount, depth)
                elif direct == self.LEFT_BOTTOM:
                    step = col if col < self.ROWS-row-1 else self.ROWS-row-1
                    if tmpcount == 0 or (tmpcount == 1 and depth + step > self.maxlength):
                        curlen, curseq = self.left_bottom_search(row, col, tmpcount, depth)
                else:
                    step = self.ROWS-row-1 if self.ROWS-row-1 < self.COLS-col-1 else self.COLS-col-1
                    if tmpcount == 0 or (tmpcount == 1 and depth + step > self.maxlength):
                        curlen, curseq = self.right_bottom_search(row, col, tmpcount, depth)

            curlen += 1
            if curlen > maxlen:
                maxlen = curlen
                if not curseq:
                    curseq = []
                curseq.insert(0, (row, col))
                maxseq = curseq

        # print("deep_search: ", "row:", row, "col:", col, "curnum:", curnum, "directions:", directions, "maxlen:", maxlen)
        return maxlen,maxseq


    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:

        self.inputgrid = grid
        self.ROWS = len(self.inputgrid)
        self.COLS = len(self.inputgrid[0])
        for row in range(0, self.ROWS):
            for col in range(0, self.COLS):
                # 遍历，每个序列必须从1开始
                if self.inputgrid[row][col] != 1:
                    continue
                # 每次从1递归开始，并且是四个方向
                seqlength, curseq = self.deep_search(row, col, -1, 0, 1, [self.LEFT_TOP, self.RIGHT_TOP, self.RIGHT_BOTTOM, self.LEFT_BOTTOM])
                #每次递归结束，保留最大的长度
                if seqlength > self.maxlength:
                    self.maxlength = seqlength
                    self.maxseq = curseq

        #return self.maxlength, self.maxseq
        return self.maxlength


sobj = Solution()
print(sobj.lenOfVDiagonal([[2,2,1,2,2],[2,0,2,2,0],[2,0,1,1,0],[1,0,2,2,2],[2,0,0,2,2]]))
