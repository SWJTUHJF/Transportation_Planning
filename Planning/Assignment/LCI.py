# -*- coding: utf-8 -*-
"""
@Time    : 2023/12/17 15:43
@Author  : He Junfeng
@StudentID    : 2021113362
@File    : LCI.py
"""
"""
This file is for the LCI calculation.
Similarly,as the network in Fig1 only consists 2 nodes and 3 links.
Hence,there's no need to utilize Dijkstra algorithm while enumeration method is applied.
Program Structure:
  Here are 7 functions which complement each other.
  Firstly we call function calculate_linkflow,which is the main part of this program.In it parameters are calculated 
by calling other functions such as calculate_linkperformance, Dichotomy_for_lambda and so forth.When finishing one iteration,
Convergence_Judgement is called to judge whether to end the main function.If not, set n = n+1 and continue the iteration.
  When the precision demand is satisfied,output the final results of LCI,flows for each link.
  Note that we make sure that all the parameters during each iteration will be shown for verifying the results.And it is 
nearly the same to the results in the very literature.
"""

import numpy as np


# MAIN FUNCTION
def calculate_linkflow(nl):
    LCI = np.zeros(3)
    n = 0
    gamma = 1
    u = [0, 0]  # use u to store shortest path travel time for convergence judgement
    flow = np.array([0, 0, 0],dtype=float)  # initialize parameters
    perf = calculate_linkperformance(flow)  # calculate the link performances for ite0
    mc = np.array(perf)  # mc:link marginal cost
    score = np.zeros([1,3])  # score:for further LCI calculation
    mu = mu_calculate(perf)  # mu:for further LCI calculation
    shortest_path = perf.index(min(perf))  # obtain the index of the shortest path
    u[0] = min(perf)
    print(f"iteration {n}:")
    print(f"flow = {flow}")
    print(f"perf = {perf}")
    print(f"mc = {mc}")
    print(f"mu = {mu}")
    flow[shortest_path] = total_demand
    score = score_calculate(flow, np.zeros(3), mc, perf)
    for i in range(nl):
        LCI[i] +=score[i]*mu[i]
    print("score=",score)
    n = 1
    while True:
        auxiliaryflow = np.array([0, 0, 0],dtype=float)  # initialize the auxiliary flow
        perf = calculate_linkperformance(flow)  # calculate the link performance
        u[1] = min(perf)
        mc = mc_calculate(flow,perf)
        mu = mu_calculate(perf)
        shortest_path = perf.index(min(perf))  # find the shortest path for free flow
        auxiliaryflow[shortest_path] = total_demand  # based on the shortest path,obtain the auxiliary flow using allornothing method
        stepsize = Dichotomy_for_lambda(flow, auxiliaryflow, perf)  # calculate the stepsize by bisection method
        newflow = flow + stepsize * (auxiliaryflow - flow)  # obtain the new flow
        score = score_calculate(newflow, flow, mc, perf)
        flag,precision = Convergence_Judgement(u)  # convergence judgement
        if flag==False:
            for i in range(nl):
                LCI[i] += score[i] * mu[i]
            print("----------------------------------")
            print(f"iteration {n}:")
            print(f"stepsize = {stepsize}")
            print(f"precision =  {precision}")
            print(f"flow = {flow}")
            print(f"perf = {perf}")
            print(f"mc = {mc}")
            print(f"score = {score}")
            print(f"mu = {mu}")
            n = n+1
            flow = newflow
            u[0] = u[1]
        else:
            print(f"iteration{n}:")
            print(f"precision = {precision}")
            print("Total iteration times:", n)
            return newflow, n, LCI


# this function is utilized to calculate link performance for each iteration
def calculate_linkperformance(xn):
    newX = [0, 0, 0]
    newX[0] = 10*(1+0.15*(xn[0]/2)**4)
    newX[1] = 20*(1+0.15*(xn[1]/2)**4)
    newX[2] = 25*(1+0.15*(xn[2]/2)**4)
    return newX


# this function is utilized to judge the convergence
def Convergence_Judgement(u):
    flag = False
    precision = abs(u[1]-u[0])/u[1]
    if precision<=0.01:
        flag = True
    return flag,precision


# this function is utilized to determine the parameter lambda, here we use bisection method
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
    solution_interval = [0, 1]  # initialize the preliminary solution interval
    stepsize = np.mean(solution_interval)
    precision = 0.0001
    while abs(solution_interval[0]-solution_interval[1])>precision:
        if sumf(stepsize)==0:
            break
        else:
            if sumf(solution_interval[0])*sumf(stepsize)<0:
                solution_interval[1]=stepsize  # narrow the interval
            else:
                solution_interval[0]=stepsize  # narrow the interval
            stepsize = np.mean(solution_interval)  # update the stepsize
    return stepsize


# this function is utilized to calculate mu,which will be needed for LCI calculation
def mu_calculate(perf):
    mu = np.zeros(3)
    denominator = 1/perf[0]+1/perf[1]+1/perf[2]
    for i in range(nl):
        mu[i] = 1/perf[i]/denominator
    return mu


# this function is utilized to calculate mc(marginal cost),which will be needed for LCI calculation
def mc_calculate(flow, perf):
    mc = np.zeros(3)
    mc[0] = perf[0] + flow[0]*10*0.3*(flow[0]/2)**3
    mc[1] = perf[1] + flow[1]*20*0.3*(flow[1]/2)**3
    mc[2] = perf[2] + flow[2]*25*0.3*(flow[2]/2)**3
    return mc

# this function is utilized to calculate score,which will be needed for LCI calculation
def score_calculate(newflow, flow, mc, perf):
    score = np.zeros(3)
    for i in range(nl):
        if newflow[i]-flow[i]>=1:
            score[i] = (newflow[i]-flow[i])*mc[i]/perf[i]
        else:
            score[i] = mc[i]/perf[i]
    return score


# Entry point
epsilon = 0.01  # the precision for iteration
nl = 3  # nl:number of links
nn = 2  # nn:number of nodes
total_demand = 10
o_id = 1
d_id = 2  # this network is relatively simple so these two parameters are ignored
flow, iteration, LCI = calculate_linkflow(nl)  # obtain the final results
print("----------------------------")
print("Final solution:")
print(f"Flow: {flow}")
n = 1
for i in LCI:
    print(f"LCI{n} = {i}")
    n += 1