# -*- coding: utf-8 -*-
"""
@Time    : 2023/12/23 22:45
@Author  : He Junfeng
@StudentID    : 2021113362
@File    : IS_run.py
"""
"""
This file is to calculate the IS(Link importance).
Note that here we utilize the network example in Figure4 (Nagurney and Qiang, 2007).
For simplicity's sake, we only choose one OD pair 1-20.
Results are sorted to help us better grasp the criticality of each link.
The calculation of EI is similar to that of IS,hence,we do not annotate in that file.
"""
import numpy as np
from Assignment.IS.IS import *


# this function is used to calculate the UE
def calculate_UE(demand, epsilon, missinglink, node, link):
    if missinglink == 0:
        miss_link = link.copy()
        miss_node = node.copy()
    else:
        miss_link = link.copy()
        miss_link.pop(missinglink)
        miss_node = node.copy()
        miss_node[link[missinglink].tail_node].l_out.remove(link[missinglink])
        miss_node[link[missinglink].head_node].l_in.remove(link[missinglink])
    n = 0
    flowhistory = list()
    impedencehistory = list()  # ~history is to store the impedence and flow at each iteration
    flow = np.zeros(28) if missinglink==0 else np.zeros(27)  # to initialize the flow, impedence
    impedence = calculate_impedence(flow, missinglink)
    flow, forcon = all_or_nothing(impedence, demand, miss_node, miss_link, missinglink)
    flowhistory.append([flow])
    n = 1
    shortimp0 = list()
    impedence_insert = impedence.copy()
    if missinglink!=0:
        impedence_insert = np.insert(impedence_insert, missinglink-1,0)
    for i in forcon:
        shortimp0.append(impedence_insert[i-1])
    impedencehistory.append([shortimp0])
    while True:
        impedence = calculate_impedence(flow, missinglink)
        auxiliaryflow, forcon = all_or_nothing(impedence, demand, miss_node, miss_link, missinglink)  # using all-or-nothing method to calculate the auxiliary flow
        shortimp0 = list()
        impedence_insert = impedence.copy()
        if missinglink!=0:
            impedence_insert = np.insert(impedence_insert, missinglink - 1, 0)
        for i in forcon:
                shortimp0.append(impedence_insert[i-1])
        impedencehistory.append([shortimp0])
        stepsize = bisection(flow, auxiliaryflow, missinglink)  # using bisection method to calculate the stepsize lambda
        flow = flow + stepsize*(auxiliaryflow-flow)  # update the flow and let it be the start of next iteration
        flowhistory.append([flow])
        flag = convergence(impedencehistory, epsilon)  # convergence judgement
        if flag == True:
            impedence = calculate_impedence(flow, missinglink)
            return np.array(flow),flowhistory,np.array(impedence),impedencehistory
        else:
            n+=1


# this function is used to conduct all-or-nothing method
def all_or_nothing(impedence, demand, node, link, missinglink):
    _, shortestpath_link = SPP_LC(o_id, d_id, node, link, impedence)
    forcon = [i.link_id for i in shortestpath_link]
    flow = [0 for i in range(28)]
    for i in forcon:
        flow[i-1] = demand
    if missinglink!=0:
        flow.pop(missinglink-1)
    flow = np.array(flow)
    return flow,forcon


# this function is for the convergence judgement
def convergence(historyimpedence, epsilon):
    shortestpath1 = np.sum(historyimpedence[-1])
    shortestpath2 = np.sum(historyimpedence[-2])
    numerator = abs(shortestpath2-shortestpath1)
    return True if numerator/shortestpath1<epsilon else False


# this function is used to obtain the parameter lambda by bisection method
def bisection(flow, auxiliaryflow, missinglink):
    def sumf(stepsize):
        variables = [flow[i]+stepsize*(auxiliaryflow[i]-flow[i]) for i in range(len(flow))]
        impedence = calculate_impedence(variables, missinglink)
        sum = np.array([(auxiliaryflow[i]-flow[i])*impedence[i] for i in range(len(flow))])
        return np.sum(sum)
    solution_interval = [0, 1]
    stepsize = np.mean(solution_interval)
    precision = 0.0001
    while abs(solution_interval[0]-solution_interval[1])>precision:
        if sumf(stepsize)==0:
            break
        else:
            if sumf(solution_interval[0])*sumf(stepsize)<0:
                solution_interval[1]=stepsize
            else:
                solution_interval[0]=stepsize
            stepsize = np.mean(solution_interval)
    return stepsize


# this function is to calculate the impedence under a certain traffic flow
def calculate_impedence(flow, missinglink):
    def f1(x):
        return 0.00005 * x ** 4 + 5 * x + 500

    def f2(x):
        return 0.00003 * x ** 4 + 4 * x + 200

    def f3(x):
        return 0.00005 * x ** 4 + 3 * x + 350

    def f4(x):
        return 0.00003 * x ** 4 + 6 * x + 400

    def f5(x):
        return 0.00006 * x ** 4 + 6 * x + 600

    def f6(x):
        return 6 * x + 500

    def f7(x):
        return 0.00008 * x ** 4 + 8 * x + 400

    def f8(x):
        return 0.00004 * x ** 4 + 5 * x + 650

    def f9(x):
        return 0.00001 * x ** 4 + 6 * x + 700

    def f10(x):
        return 4 * x + 800

    def f11(x):
        return 0.00007 * x ** 4 + 7 * x + 650

    def f12(x):
        return 8 * x + 700

    def f13(x):
        return 0.00001 * x ** 4 + 7 * x + 600

    def f14(x):
        return 8 * x + 500

    def f15(x):
        return 0.00003 * x ** 4 + 9 * x + 200

    def f16(x):
        return 8 * x + 300

    def f17(x):
        return 0.00003 * x ** 4 + 7 * x + 450

    def f18(x):
        return 5 * x + 300

    def f19(x):
        return 8 * x + 600

    def f20(x):
        return 0.00003 * x ** 4 + 6 * x + 300

    def f21(x):
        return 0.00004 * x ** 4 + 4 * x + 400

    def f22(x):
        return 0.00002 * x ** 4 + 6 * x + 500

    def f23(x):
        return 0.00003 * x ** 4 + 9 * x + 350

    def f24(x):
        return 0.00002 * x ** 4 + 8 * x + 400

    def f25(x):
        return 0.00003 * x ** 4 + 9 * x + 450

    def f26(x):
        return 0.00006 * x ** 4 + 7 * x + 300

    def f27(x):
        return 0.00003 * x ** 4 + 8 * x + 500

    def f28(x):
        return 0.00003 * x ** 4 + 7 * x + 560

    funlist = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14,
               f15, f16, f17, f18, f19, f20, f21, f22, f23, f24, f25, f26, f27, f28]
    if missinglink == 0:
        impedence = [funlist[i](flow[i]) for i in range(28)]
        return np.array(impedence)
    else:
        funlist.pop(missinglink-1)
        impedence = [funlist[i](flow[i]) for i in range(27)]
        return np.array(impedence)


# this function is used to calculate the IS
def calculate_IS():
    LINK, NODE, NODE_COUNT, LINK_COUNT = Obtain_LinkandNode(PATH)
    flow, _, impedence, _ = calculate_UE(demand, epsilon, 0, NODE, LINK)
    system_travel_time = np.sum(flow*impedence)
    STTWL = list()  #STTWL: system travel time without specific link
    for i in range(1,29):
        LINK, NODE, NODE_COUNT, LINK_COUNT = Obtain_LinkandNode("Nagurney.txt")
        flowwl, _, impedencewl, _ = calculate_UE(demand, epsilon, i, NODE, LINK)
        STTWL.append(np.sum(flowwl*impedencewl))
    IS = [(STTWL[i]-system_travel_time)/demand for i in range(28)]
    return IS


PATH = "Nagurney.txt"
o_id = 1
d_id = 20
demand = 100
epsilon = 0.005
IS = calculate_IS()
IS.insert(0,0)
IS = np.array(IS)
tosort = np.argsort(-IS)
for i in range(len(tosort)):
    print(tosort[i], IS[tosort[i]])