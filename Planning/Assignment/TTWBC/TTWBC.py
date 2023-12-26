# -*- coding: utf-8 -*-
"""
@Time    : 2023/12/25 21:08
@Author  : He Junfeng
@StudentID    : 2021113362
@File    : TTWBC.py
"""
import random

# -*- coding: utf-8 -*-
"""
For simplicity's sake, we only choose one OD pair 1-20 to calculate the TTWBC
"""
import numpy as np
class Node:
    def __init__(self, node_id, l_in_empty, l_out_empty):
        self.node_id = node_id
        self.l_in = l_in_empty
        self.l_out = l_out_empty

    def set_l_in(self, l_in):
        self.l_in.append(l_in)

    def set_l_out(self, l_out):
        self.l_out.append(l_out)

    def set_SPP_u(self, u):
        self.u = u

    def set_SPP_p(self, p):
        self.p = p

class Link:
    def __init__(self, link_id, tail_node, head_node, length):
        self.link_id = link_id
        self.tail_node = tail_node
        self.head_node = head_node
        self.length = length


def Obtain_LinkandNode(path):
    with open(path, 'r') as f1:
        l1 = f1.readlines()
    length=len(l1)
    x=0
    while x < length:
        if l1[x] == '\n':
            del l1[x]
            x -= 1
            length -= 1
        x += 1
    for i in range(len(l1)):
        if '~' in l1[i]:
            l1_START_LINE = i+1
            break
    for i in range(2):
        l1[i] = l1[i].split(' ')
    NODE_COUNT = eval(l1[0][-1])
    LINK_COUNT = eval(l1[1][-1])
    for i in range(l1_START_LINE, len(l1)):
        l1[i] = l1[i].strip('\n')
        l1[i] = l1[i].rstrip('\t')
        l1[i] = l1[i].lstrip('\t')
        l1[i] = l1[i].split(' ')
    readlist = l1[l1_START_LINE:]
    LINK = [Link(i+1,eval(readlist[i][0]),eval(readlist[i][1]),link_length[i]) for i in range(LINK_COUNT)]
    LINK.insert(0, 0)#in order to avoid different meanings between index and id
    NODE = [Node(i+1,[],[]) for i in range(NODE_COUNT)]
    NODE.insert(0, 0)
    for i in range (1, LINK_COUNT+1):
        NODE[LINK[i].tail_node].set_l_out(LINK[i])
        NODE[LINK[i].head_node].set_l_in(LINK[i])
    return (LINK, NODE, NODE_COUNT, LINK_COUNT)


shortestpath = np.array([[1,2,3,4,5,6,7,8,9,19],
                         [1,2,3,4,5,6,7,8,18,28],
                         [1,2,3,4,5,6,7,17,27,28],
                         [1,2,3,4,5,6,16,26,27,28],
                         [1,2,3,4,5,15,25,26,27,28],
                         [1,2,3,4,14,24,25,26,27,28],
                         [1,2,3,13,23,24,25,26,27,28],
                         [1,2,12,22,23,24,25,26,27,28],
                         [1,11,21,22,23,24,25,26,27,28],
                         [10,20,21,22,23,24,25,26,27,28]])


link_length = [1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1]
path = "Nagurney.txt"
LINK, NODE, NODE_COUNT, LINK_COUNT = Obtain_LinkandNode(path)
TNSP = len(shortestpath)  # TNSP:Total number of shortest paths between the OD pair
TTWBC = list()
for i in range(1, LINK_COUNT+1):
    sum = 0
    for j in shortestpath:
        if i in j:
            sum+=1
    TTWBC.append(int(sum/TNSP*LINK[i].length))
TTWBC = np.array(TTWBC)
link_rank = np.argsort(-TTWBC)+1
link_rank = link_rank[:10]
rank = TTWBC[link_rank-1]
for i in range(10):
    print("LINK:", link_rank[i]," Rank:",rank[i])
