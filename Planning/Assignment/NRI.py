# -*- coding: utf-8 -*-
"""
@Time    : 2023/12/20 6:08
@Author  : He Junfeng
@StudentID    : 2021113362
@File    : NRI.py
"""
# this file is to calculate the NRI of Fig1(Almotahari,Yazici 2019)


import numpy as np
# this function is to calculate the UE flow and impedence
def calculate_UE(demand, epsilon, missinglink):
    if missinglink == 0:
        print("This is the total minutes of travel on the whole network.")
    else:
        print(f"This is calculating the NRI of link {missinglink}")
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
        print("******************")
        print(f"iteration{n}:")
        print(f"flow = {flow}")
        impedence = update_impedence(flow, missinglink)
        auxiliaryflow = all_or_nothing(impedence, demand)  # using all-or-nothing method to calculate the auxiliary flow
        stepsize = bisection(flow, auxiliaryflow, missinglink)  # using bisection method to calculate the stepsize lambda
        flow = flow + stepsize*(auxiliaryflow-flow)  # update the flow and let it be the start of next iteration
        impedencehistory.append([update_impedence(flow, missinglink)])
        flowhistory.append([flow])
        flag = convergence(impedencehistory, epsilon)  # convergence judgement
        print(f"stepsize = {stepsize}")
        print(f"impedence = {impedence}")
        if flag == True:
            print("******************")
            print(f"iteration{n+1}:")
            print(f"flow = {flow}")
            print(f"impedence = {update_impedence(flow, missinglink)}")
            print("******************")
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


# this function is to calculate the NRI
def NRI_calculate():
    flowlist = list()
    impedencelist = list()
    flow,_,impedence,_ = calculate_UE(demand,epsilon,missinglink=0)
    c = np.sum(flow*impedence)
    NRI = [0,0,0]
    for i in range(1,4):
        flow, _, impedence, _ = calculate_UE(demand, epsilon, missinglink=i)
        flowlist.append(flow)
        impedencelist.append(impedence)
        NRI[i-1] = np.sum(flow*impedence) - c
    return NRI,flowlist,impedencelist

nl = 3
epsilon = 0.01
demand = 10
NRI,UE_FLOW,UE_INPEDENCE = NRI_calculate()
print("Final answer:")
print(f"NRI of link 1 is :{NRI[0]}")
print(f"NRI of link 2 is :{NRI[1]}")
print(f"NRI of link 3 is :{NRI[2]}")
