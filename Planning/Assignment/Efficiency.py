# -*- coding: utf-8 -*-
"""
@Time    : 2023/12/21 14:46
@Author  : He Junfeng
@StudentID    : 2021113362
@File    : Efficiency.py
"""
"""
This file is to calculate the efficiency(Latora and Marchiori, 2001) of the network in Fig1(Almotahari,Yazici 2019)
Note that this so-called efficiency does not directly evaluate the criticality of one specific link
Instead, changes in efficiency when a link is removed can be considered as a criticality measure
Hence, here we consider "relative change(RC)" as the criticality of each link
We found that the results are relatively small so we mutiple the output by a constant of 1000
"""
import numpy as np
# this function is to calculate the UE flow and impedence
def calculate_UE(demand, epsilon, missinglink):
    n = 0
    flowhistory = list()
    impedencehistory = list()  # ~history is to store the impedence and flow at each iteration
    flow = np.zeros(3) if missinglink==0 else np.zeros(2)  # to initialize the flow, impedence
    impedence = update_impedence(flow, missinglink)
    flow = all_or_nothing(impedence, demand)
    flowhistory.append([flow])
    n = 1
    impedencehistory.append([update_impedence(flow, missinglink)])
    while True:
        impedence = update_impedence(flow, missinglink)
        auxiliaryflow = all_or_nothing(impedence, demand)  # using all-or-nothing method to calculate the auxiliary flow
        stepsize = bisection(flow, auxiliaryflow, missinglink)  # using bisection method to calculate the stepsize lambda
        flow = flow + stepsize*(auxiliaryflow-flow)  # update the flow and let it be the start of next iteration
        impedencehistory.append([update_impedence(flow, missinglink)])
        flowhistory.append([flow])
        flag = convergence(impedencehistory, epsilon)  # convergence judgement
        if flag == True:
            return flow,flowhistory,impedence,impedencehistory
        else:
            n+=1


# this function is to calculate the auxiliary flow using all-or-nothing method
def all_or_nothing(impedence, demand):
    flow = np.zeros(len(impedence))
    shortestpath = np.argmin(impedence)
    flow[shortestpath] = demand
    return flow


# this function is for convergence judgement
def convergence(historyimpedence, epsilon):
    shortestpath1 = np.min(historyimpedence[-1])
    shortestpath2 = np.min(historyimpedence[-2])
    numerator = abs(shortestpath2-shortestpath1)
    return True if numerator/shortestpath1<epsilon else False


# this function is to calculate the flow when the impedence is updated
def update_impedence(flow,missinglink):
    def f1(x):
        return 10 * (1 + 0.15 * (x / 2)**4)

    def f2(x):
        return 20 * (1 + 0.15 * (x / 2)**4)

    def f3(x):
        return 25 * (1 + 0.15 * (x / 2)**4)
    funlist = [0,f1,f2,f3]
    if missinglink == 0:
        impedence = [funlist[i](flow[i-1]) for i in range(1,4)]
        return np.array(impedence)
    else:
        funlist.pop(missinglink)
        impedence = [funlist[i](flow[i-1]) for i in range(1,3)]
        return np.array(impedence)


# this function is to obtain the stepsize using bisection method
def bisection(flow, auxiliaryflow, missinglink):
    def f1(x):
        return 10*(1+0.15*pow((x/2),4))
    def f2(x):
        return 20*(1+0.15*pow((x/2),4))
    def f3(x):
        return 25*(1+0.15*pow((x/2),4))
    funclist = [f1,f2,f3]
    if missinglink!=0:
        funclist.pop(missinglink-1)
    # print(len(funclist))
    def sumf(stepsize):
        sum = 0
        for i in range(len(flow)):
                sum+=(auxiliaryflow[i]-flow[i])*funclist[i](flow[i] + stepsize * (auxiliaryflow[i] - flow[i]))
        return sum
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


# this function is to calculate the Efficiency
def Efficiency_calculate():
    flowlist = list()
    impedencelist = list()
    flow,_,impedence,_ = calculate_UE(demand,epsilon,missinglink=0)
    dij = np.min(impedence)
    E = 1/(nn*(nn-1))/dij
    Efficiency = np.zeros(3)
    relative_change = np.zeros(3)
    for i in range(1,4):
        flow, _, impedence, _ = calculate_UE(demand, epsilon, missinglink=i)
        flowlist.append(flow)
        impedencelist.append(impedence)
        dij = np.min(impedence)
        Efficiency[i-1] = 1 / (nn * (nn - 1)) / dij
        relative_change[i-1] = E - Efficiency[i-1]
    return E*1000,Efficiency*1000,relative_change*1000

nn = 2  # nn:number of node
nl = 3  # nl:number of link
epsilon = 0.01
demand = 10
E,Efficiency,relative_change = Efficiency_calculate()
print("Final answer:")
print(f"Efficiency of whole network is :{E}")
print(f"Efficiency of network without link 1 is :{Efficiency[0]}")
print(f"Efficiency of network without link 2 is :{Efficiency[1]}")
print(f"Efficiency of network without link 3 is :{Efficiency[2]}")
print(f"RC of link 1 is :{relative_change[0]}")
print(f"RC of link 2 is :{relative_change[1]}")
print(f"RC of link 3 is :{relative_change[2]}")
