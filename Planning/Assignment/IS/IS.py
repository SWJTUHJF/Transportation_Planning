# -*- coding: utf-8 -*-
"""
@Time    : 2023/12/21 15:08
@Author  : He Junfeng
@StudentID    : 2021113362
@File    : IS.py
"""


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
    def __init__(self, link_id, tail_node, head_node, length=0):
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
    LINK = [Link(i+1,eval(readlist[i][0]),eval(readlist[i][1])) for i in range(LINK_COUNT)]
    LINK.insert(0, 0)#in order to avoid different meanings between index and id
    NODE = [Node(i+1,[],[]) for i in range(NODE_COUNT)]
    NODE.insert(0, 0)
    for i in range (1, LINK_COUNT+1):
        NODE[LINK[i].tail_node].set_l_out(LINK[i])
        NODE[LINK[i].head_node].set_l_in(LINK[i])
    return (LINK, NODE, NODE_COUNT, LINK_COUNT)


def SPP_LC(o_id, d_id, node, link, impedence):
    for i in range(len(impedence)):
        link[i+1].length = impedence[i]
    node[o_id].set_SPP_u(0)
    for t in node[1:]:
        t.set_SPP_p(-1)
        if t.node_id != o_id:
            t.set_SPP_u(float('inf'))  #初始化条件
    Q = [node[o_id]]  #Q作为SEL使用
    while len(Q) != 0:  #关键循环
        i = Q[0]
        del Q[0]
        for ij in i.l_out:
            j = node[ij.head_node]
            if j.u > (i.u + ij.length):
                j.u = (i.u + ij.length)
                j.p = i
                if j not in Q:
                    Q.append(j)
    shortestpath_p_list = [0]  #记录最短路
    for t in node[1:]:
        shortestpath_p_list.append(t.p)
    Lc_node = [] # store node list between o_id and d_id
    shortestpath_link = []  # store link list between o_id and d_id
    head_n = node[d_id]
    Lc_node.append(d_id)
    tail_n = shortestpath_p_list[d_id] #get the predecessor
    while tail_n != -1:
        for l in head_n.l_in:
            if l.tail_node == tail_n.node_id:#get the exact link by predecessor
                shortestpath_link.insert(0,l)
        head_n = tail_n
        Lc_node.append(tail_n.node_id)
        tail_n = shortestpath_p_list[head_n.node_id] #get the predecessor
    Lc_node.reverse()
    return Lc_node, shortestpath_link

