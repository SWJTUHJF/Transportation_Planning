import math
import numpy as np
from sklearn.linear_model import LinearRegression

# parameter setting for gravity model
def Gravity_Model(Qij, Oi, Dj, Current_c, Future_c):
    new_qij = [[0 for i in range(num_iorj)] for j in range(num_iorj)]
    # using least square method function defined below to calculate the parameter alpha, beta, gamma
    alpha, beta, gamma = least_square_method(Qij, Oi, Dj, Current_c)
    # calculate the qij based on the Gravity Model
    for i in range(num_iorj):
        for j in range(num_iorj):
            new_qij[i][j] = alpha*((future_Oi[i]*future_Dj[j])**beta)/(future_c[i][j]**gamma)
    new_Oi,new_Dj = OD_Calculate(new_qij)
    new_FO,new_FD = Fod_Calculate(future_Oi, future_Dj, new_Oi, new_Dj)
    print("Using Gravity Model, we could obtain the qij, Oi, Dj, FO, and FD as follows:")
    print("qij:\n")
    for i in new_qij:
        print(i)
    print("\nOi:\n",new_Oi,"\nDj:\n",new_Dj,"\nFO\n",new_FO,"\nFD\n",new_FD)
    Flag = Convergence_judgement(new_FO, new_FD, epsilon)
    # if only using the gravity model we obtain the results that meet the requirements,then break the program
    # else, if it does not, continue to iterate using AGFM
    if not Flag:
        print("This OD table does not meet the constraint,continue to iterate using the method of AGFM")
        Final_Oi, Final_Dj, Final_Qij =  average_growth_factor_method(new_qij,new_Oi,new_Dj,epsilon)
        return alpha, beta, gamma, Final_Oi, Final_Dj, Final_Qij
    else:
        "We have obtain the result that meets the constraint without using AGFM"
        return alpha, beta, gamma, new_Oi, new_Dj, new_qij


# using AGFM to continue iterate
def average_growth_factor_method(Qij, Oi, Dj, error):
    new_Qij = [[0 for i in range(num_iorj)]for i in range(num_iorj)]
    new_Oi = [0, 0, 0]
    new_Dj = [0, 0, 0]
    flag = 1
    FO, FD = Fod_Calculate(future_Oi, future_Dj, Oi, Dj)
    while True:
        new_Qij = Qij_Calculate_AGFM(FO, FD, Qij)
        new_Oi,new_Dj = OD_Calculate(new_Qij)
        FO, FD = Fod_Calculate(future_Oi, future_Dj, new_Oi, new_Dj)
        # to show the results of FO,FD,Qij of each iteration
        print("iteration ",flag)
        print("FO:",FO)
        print("FD:",FD)
        print("Qij:")
        for i in new_Qij:
            print(i)
        print("----------------------------------")
        flag+=1
        # to judge whether the constraint is meeted,if not,continue to iterate,else break the iteration
        if not Convergence_judgement(FO, FD, epsilon):
            Oi = new_Oi
            Dj = new_Dj
            Qij = new_Qij
        else:
            break
    return new_Oi, new_Dj, new_Qij


# Judgement of the convergence
def Convergence_judgement(FO, FD, error):
    biggesterror = 0
    for i in FO:
        if math.fabs(i - 1) > biggesterror:
            biggesterror = math.fabs(i - 1)
    for i in FD:
        if math.fabs(i - 1) > biggesterror:
            biggesterror = math.fabs(i - 1)
    if biggesterror < error:
        return True
    else:
        return False


#using least square method to fit the parameters
def least_square_method(qij, Oi, Dj, Current_c):
    OiDj = np.zeros(shape = [3,3])
    for i in range(len(Oi)):
        for j in range(len(Oi)):
            OiDj[i][j] = Oi[i]*Dj[j]
    # calculate the Inc and InOidj
    logOiDj = np.log(OiDj)
    logc = np.log(Current_c)
    # define the input variable
    X = np.zeros(shape = [9, 2])
    flag = 0
    for i in range(num_iorj):
        for j in range(num_iorj):
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
    alpha = math.exp(intercept[0])
    beta = coefficients[0][0]
    gamma = -coefficients[0][1]
    return alpha, beta, gamma


# Calculate the Qij using the method of AGFM(Average growth factor method)
def Qij_Calculate_AGFM(FO, FD, qij):
    new_qij = [[0 for i in range(num_iorj)] for j in range(num_iorj)]  # create a blank list for further data store
    for i in range(num_iorj):
        for j in range(num_iorj):
            new_qij[i][j] = qij[i][j]*(FO[i] + FD[j])/2
    return new_qij


# Calculate the FO and FD
def Fod_Calculate(U, V, O, D):
    FO = list()
    FD = list()
    for i in range(len(U)):
        FO.append(U[i]/O[i])
    for i in range(len(V)):
        FD.append(V[i]/D[i])
    return  FO, FD


# Calculate the OiDj
def OD_Calculate(Qij):
    new_Oi = [0, 0, 0]
    new_Dj = [0, 0, 0]
    for i in range(num_iorj):
        for j in range(num_iorj):
            new_Oi[i]+=Qij[i][j]
            new_Dj[i]+=Qij[j][i]
    return new_Oi, new_Dj


# main input
current_qij = [[17.0, 7.0,4.0]
               ,[7.0, 38.0, 6.0],
               [4.0, 5.0, 17.0]]
current_Oi = [28.0, 51.0, 26.0]
current_Dj = [28.0, 50.0, 27.0]
future_Oi = [38.6, 91.9, 36.0]
future_Dj = [39.3, 90.3, 36.9]
current_c = [[7.0, 17.0, 22.0],
             [17.0, 15.0, 23.0],
             [22.0, 23.0, 7.0]]
future_c = [[4.0, 9.0, 11.0],
            [9.0, 8.0, 12.0],
            [11.0, 12.0, 4.0]]
num_iorj = 3  # This parameter means the number of origination or destination points
epsilon = 0.01


# Progarm enter
alpha, beta, gamma, Final_Oi, Final_Dj, Final_Qij = Gravity_Model(current_qij, current_Oi, current_Dj, current_c, future_c)
print("Final answer:")
print("The result of parameter fitting is:", alpha, beta, gamma)
print("The result of Qij is:")
for i in Final_Qij:
    print(i)
print("The result of Oi is:", Final_Oi)
print("The result of Dj is:", Final_Dj)
Generation = 0
for i in Final_Oi:
    Generation+=i
print("Total Trip Generation is:",Generation)