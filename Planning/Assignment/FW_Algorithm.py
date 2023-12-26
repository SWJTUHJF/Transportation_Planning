# -*- coding: utf-8 -*-
"""
@Time    : 2023/12/17 10:54
@Author  : He Junfeng
@StudentID    :2021113362
@File    : FW_Algorithm.py
"""
# Note that this file is only for the basic FW algorithm without calculating the critical index
# As the network of Fig1 is relatively simple,hence,we decide to find the shortest path using enumeration method.


import numpy as np
def calculate_linkflow(nl):
    n = 0
    flow = np.array([0, 0, 0],dtype=float)
    perf = calculate_linkperformance(flow)
    shortest_path = perf.index(min(perf))
    flow[shortest_path] = total_demand
    n = 1
    while True:
        auxiliaryflow = np.array([0, 0, 0],dtype=float)  # initialize the auxiliary flow
        perf = calculate_linkperformance(flow)  # initialize the link performance
        shortest_path = perf.index(min(perf))  # find the shortest path for free flow
        auxiliaryflow[shortest_path] = total_demand  # based on the shortest path,obtain the auxiliary flow using allornothing method
        stepsize = Dichotomy_for_lambda(flow, auxiliaryflow, perf)  # calculate the stepsize by bisection method
        newflow = flow + stepsize * (auxiliaryflow - flow)  # obtain the new flow
        flag,precision = Convergence_Judgement(newflow, flow)  # convergence judgement
        print(f"iteration{n}:")
        print(f"stepsize = {stepsize}")
        print(f"precision =  {precision}")
        if flag==False:
            n = n+1
            flow = newflow
        else:
            print("Total iteration times:",n)
            return newflow,n


def calculate_linkperformance(xn):
    newX = [0, 0, 0]
    newX[0] = 10*(1+0.15*(xn[0]/2)**4)
    newX[1] = 20*(1+0.15*(xn[1]/2)**4)
    newX[2] = 25*(1+0.15*(xn[2]/2)**4)
    return newX


def Convergence_Judgement(newflow, flow):
    sum = 0
    for i in range(nl):
        sum+=(newflow[i]-flow[i])**2
    sum = pow(sum, 0.5)
    precision = sum/np.sum(flow)
    if precision>epsilon:
        flag = False
    if precision<=epsilon:
        flag = True
    return flag,precision


def Dichotomy_for_lambda(flow, auxiliaryflow, perf):
    def f1(x):
        return 10*(1+0.15*pow((x/2),4))
    def f2(x):
        return 20*(1+0.15*pow((x/2),4))
    def f3(x):
        return 25*(1+0.15*pow((x/2),4))
    def sumf(stepsize):
        sum = 0
        sum+=(auxiliaryflow[0]-flow[0])*f1(flow[0]+stepsize*(auxiliaryflow[0]-flow[0]))
        sum+=(auxiliaryflow[1]-flow[1])*f2(flow[1]+stepsize*(auxiliaryflow[1]-flow[1]))
        sum+=(auxiliaryflow[2]-flow[2])*f3(flow[2]+stepsize*(auxiliaryflow[2]-flow[2]))
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


epsilon = 0.01
nl = 3  # nl:number of links
nn = 2  # nn:number of nodes
total_demand = 10
o_id = 1
d_id = 2
flow,iteration = calculate_linkflow(nl)
print("Final solution:")
print(f"Flow: {flow}")