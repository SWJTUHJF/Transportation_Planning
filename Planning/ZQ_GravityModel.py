import math
import numpy as np
from sklearn.linear_model import LinearRegression
def Convergence_judgement(FO, FD):
    F = FO + FD
    maxF = max(F)
    minF = min(F)
    if maxF-1<0.01 and 1-minF<0.01:
        return True
    else:
        return False
def least_square_method(qij, Oi, Dj, Current_c):
    OiDj = np.zeros(shape = [3,3])
    for i in range(len(Oi)):
        for j in range(len(Oi)):
            OiDj[i][j] = Oi[i]*Dj[j]
    logOiDj = np.log(OiDj)
    logc = np.log(Current_c)
    X = np.zeros(shape = [9, 2])
    flag = 0
    for i in range(3):
        for j in range(3):
            X[flag][0] = logOiDj[i][j]
            X[flag][1] = logc[i][j]
            flag+=1
            if flag ==9:
                break
    Y = np.log(qij)
    Y = np.reshape(Y,(9,1))
    model = LinearRegression()
    model.fit(X, Y)
    coefficients = model.coef_
    intercept = model.intercept_
    return math.exp(intercept[0]),coefficients[0][0], -coefficients[0][1]
def Qij_Calculate_AGFM(FO, FD, qij):
    new_qij = [[0 for i in range(3)] for j in range(3)]
    for i in range(3):
        for j in range(3):
            new_qij[i][j] = qij[i][j]*(FO[i] + FD[j])/2
    return new_qij
def Fod_Calculate(U, V, O, D):
    FO = list()
    FD = list()
    for i in range(3):
        FO.append(U[i]/O[i])
    for i in range(3):
        FD.append(V[i]/D[i])
    return  FO, FD
def OD_Calculate(Qij):
    new_O = [0, 0, 0]
    new_D = [0, 0, 0]
    for i in range(3):
        for j in range(3):
            new_O[i]+=Qij[i][j]
            new_D[i]+=Qij[j][i]
    return new_O, new_D
def Gravity_Model(cq, cO, cD, cc):
    new_q = [[0,0,0],[0,0,0],[0,0,0]]
    a0,a1,a2 = least_square_method(cq, cO, cD, cc)
    for i in range(3):
        for j in range(3):
            new_q[i][j] = a0*((fO[i]*fD[j])**a1)/(fc[i][j]**a2)
    new_O,new_D = OD_Calculate(new_q)
    new_FO,new_FD = Fod_Calculate(fO, fD, new_O, new_D)
    if not Convergence_judgement(new_FO, new_FD):
        finalo, finald, finalq = AGFM(new_q,new_O,new_D)
        return a0, a1, a2, finalo, finald, finalq
    else:
        return a0, a1, a2, new_O, new_D, new_q
def AGFM(Qij, Oi, Dj):
    new_Q = [[0,0,0],[0,0,0],[0,0,0]]
    new_O = [0, 0, 0]
    new_D = [0, 0, 0]
    flag = 1
    while True:
        FO, FD = Fod_Calculate(fO, fD, Oi, Dj)
        new_Q = Qij_Calculate_AGFM(FO, FD, Qij)
        new_O,new_D = OD_Calculate(new_Q)
        if not Convergence_judgement(FO, FD):
            Oi = new_O
            Dj = new_D
            Qij = new_Q
        else:
            break
    return new_O, new_D, new_Q
cq = [[17.0, 7.0,4.0],[7.0, 38.0, 6.0],[4.0, 5.0, 17.0]]
cO = [28.0, 51.0, 26.0]
cD = [28.0, 50.0, 27.0]
fO = [38.6, 91.9, 36.0]
fD = [39.3, 90.3, 36.9]
cc = [[7.0, 17.0, 22.0],[17.0, 15.0, 23.0],[22.0, 23.0, 7.0]]
fc = [[4.0, 9.0, 11.0],[9.0, 8.0, 12.0],[11.0, 12.0, 4.0]]
alpha,beta,gamma, Final_Oi, Final_Dj, Final_Qij = Gravity_Model(cq, cO, cD, cc)
finaltable = np.zeros(shape=[4,4])
for i in range(3):
    for j in range(3):
        finaltable[i][j] = round(Final_Qij[i][j],3)
for i in range(3):
    finaltable[i][3] = round(Final_Oi[i],3)
    finaltable[3][i] = round(Final_Dj[i],3)
for i in range(3):
    finaltable[3][3]+=finaltable[i][3]
print("The result of is:\n", finaltable)
