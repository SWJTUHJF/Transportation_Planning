import math
# 指定计算方法
method = int(input("Choose AvgIncreaseFun for 1,DetroitFun for 2,FratarFun for 3,UniqueGrowthFun for 4 and FurnessFun for 5:"))
if method ==1:
    print("平均增长系数法求解")
if method ==2:
    print("底特律法求解")
if method ==3:
    print("福莱特法求解")
if method ==5:
    print("Furness法求解")

#input for current trip distribution
PA_Table = [[4,2,2],[2,8,4],[2,4,4]]  #Qij
Update_PA_Table = [[0,0,0],[0,0,0],[0,0,0]]
O = [8,14,10]  #Oi
D = [8,14,10]  #Dj
Update_O = [0,0,0]
Update_D = [0,0,0]
T = 32  #total_generation

#input for future trips
U = [16,28,40]  #futureOi
V = [16,28,40]  #futureDj
X = 84  #future_total_generation

##平均增长率法
def AvgIncreaseFunc(FO,FD,i,j):
    f = (FO[i]+FD[j])/2
    return f

## 底特律法
def DetroitFun(FO,FD,T,X,i,j):
    f = FO[i]*FD[j]*T/X
    return f

## 福莱特法
def FratarFun(FO,FD,PA_Table,O,D,i,j,m):
    sumqFi = 0
    sumqFj = 0
    num = 0
    for q in PA_Table[i]:
        sumqFi += q*FD[num]
        num+=1
    num = 0
    for q in PA_Table:
        sumqFj += q[j]*FO[num]
        num+=1
    Li = O[i]/sumqFi
    Lj = D[j]/sumqFj
    f = FO[i]*FD[j]*(Lj+Li)/2
    return f

# 常增长系数法
def UniqueGrowth(O,U,i):
    f = U[i]/O[i]
    return f

def FurnessMethod():
    pass
tool = True

## Convergence gap
def ConvergenceTest(FO,FD):
    gap = 0.03
    biggestgap = 0
    for i in FO:
        if math.fabs(i-1) > biggestgap:
            biggestgap = math.fabs(i-1)
    for i in FD:
        if math.fabs(i-1) > biggestgap:
            biggestgap = math.fabs(i-1)
    if biggestgap<gap:
        return True
    else:
        return False


#Initialize
m = 0
numofZones = len(O)
maxiter = 10
FO = [0,0,0]  #FO:growth rate of production
FD = [0,0,0]  #FD:growth rate of attraction
if method != 5:
    print("第一次求解Fo和Fd")
    for i in range(0, numofZones):
        FO[i] = U[i] / O[i]
        print("FO%d=%.4f" % (i + 1, FO[i]))

    for j in range(0, numofZones):
        FD[j] = V[j] / D[j]
        print("FD%d=%.4f" % (j + 1, FD[j]))

#Main loop

if method!=5:
    for m in range(0, maxiter):
        if method == 4:
            print("采用常增长系数法求解")
            print("求各个小区的发生增长数：")
            for i in range(0, numofZones):
                for j in range(0, numofZones):
                    Update_PA_Table[i][j] = PA_Table[i][j] * UniqueGrowth(O, U, i)
                print("Fo%d=%.4f" % (i + 1, UniqueGrowth(O, U, i)))
            PA_Table = Update_PA_Table
            print("常增长系数法计算得到的OD表：")
            break
        # Update PA table according to different function
        print(f"第{m + 1}次迭代")
        # 更新OD表
        for i in range(0, numofZones):
            for j in range(0, numofZones):
                if (method == 1):
                    Update_PA_Table[i][j] = PA_Table[i][j] * AvgIncreaseFunc(FO, FD, i, j)
                    print("q%d%d=%.3f" % (i + 1, j + 1, Update_PA_Table[i][j]))
                elif method == 2:
                    Update_PA_Table[i][j] = PA_Table[i][j] * DetroitFun(FO, FD, T, X, i, j)
                    print("q%d%d=%.3f" % (i + 1, j + 1, Update_PA_Table[i][j]))
                elif method == 3:
                    Update_PA_Table[i][j] = PA_Table[i][j] * FratarFun(FO, FD, PA_Table, O, D, i, j, m)
                    print("q%d%d=%.3f" % (i + 1, j + 1, Update_PA_Table[i][j]))

        print(f"第{m + 1}次迭代计算OD表")
        for i in Update_PA_Table:
            print(i)
        # Update trips production and trip attraction
        Update_O = [0, 0, 0]
        Update_D = [0, 0, 0]
        for i in range(0, numofZones):
            for j in range(0, numofZones):
                Update_O[i] = Update_PA_Table[i][j] + Update_O[i]
        for i in range(0, numofZones):
            for j in range(0, numofZones):
                Update_D[i] = Update_PA_Table[j][i] + Update_D[i]
        O = Update_O
        D = Update_D
        # Update FO and FD according to updated production and attraction
        print(f"第{m + 2}次求解FO,FD：")
        for i in range(0, numofZones):
            FO[i] = U[i] / Update_O[i]
            FD[i] = V[i] / Update_D[i]
            print(f"FO{i + 1}={FO[i]},FD{i}={FD[i]}")

        # used for Detriot method
        if method == 2:
            T = 0
            for i in Update_O:
                T = T + i
        # Conduct convergence test
        if ConvergenceTest(FO, FD):
            print("FO和FD各项系数误差均小于3%，不需继续迭代")
            PA_Table = Update_PA_Table
            break
        else:
            print("FO和FD部分系数大于3%的误差，需要重新迭代")
            PA_Table = Update_PA_Table
# Structure of Furness method differs from other method
if method == 5:
    # First iteration:FD = 0
    print("Let all the element of FD be 0")
    print("第1次迭代：")
    for i in range(0,numofZones):
        FD[i] = 1
    for i in range(0,numofZones):
        FO[i] = U[i]/O[i]
        print("FO%.d=%.4f"%(i+1,FO[i]))  # 初始化FO FD
    for i in range(0,numofZones):  # 得到第一次的迭代计算OD表
        for j in range(0,numofZones):
            PA_Table[i][j]*=FO[i]
    print("第一次迭代计算OD表")
    for i in PA_Table:
        print(i)
    if ConvergenceTest(FO, FD):  # 进行第一次的收敛判断
        print("FO和FD各项系数误差均小于3%，不需继续迭代")
        maxiter = 0
    else:
        print("FO和FD部分系数大于3%的误差，需要重新迭代")
    # 更新O,D
    Update_O = [0, 0, 0]
    Update_D = [0, 0, 0]
    for i in range(0, numofZones):
        for j in range(0, numofZones):
            Update_O[i] = PA_Table[i][j] + Update_O[i]
    for i in range(0, numofZones):
        for j in range(0, numofZones):
            Update_D[i] = PA_Table[j][i] + Update_D[i]
    O = Update_O
    D = Update_D

    for time in range(0,maxiter):
        print(f"第{time+2}次迭代：")
        # 计算吸引增长系数
        print("先求吸引增长系数:")
        for i in range(0,numofZones):
            FD[i] = V[i]/D[i]
            print("FD%.d=%.4f"%(i+1,V[i]/D[i]))
        print(f"将分布交通量乘以吸引增长系数，得新的分布交通量.下表为第{time+2}次迭代计算中间OD表")
        # 更新OD表
        for i in range(0, numofZones):
            for j in range(0, numofZones):
                PA_Table[i][j] *= FD[j]
        # 更新O,D
        Update_O = [0, 0, 0]
        Update_D = [0, 0, 0]
        for i in range(0, numofZones):
            for j in range(0, numofZones):
                Update_O[i] = PA_Table[i][j] + Update_O[i]
        for i in range(0, numofZones):
            for j in range(0, numofZones):
                Update_D[i] = PA_Table[j][i] + Update_D[i]
        O = Update_O
        D = Update_D
        # 计算发生增长系数
        for i in PA_Table:
            print(i)
        print("接着求发生增长系数：")
        for i in range(0,numofZones):
            FO[i] = U[i]/O[i]
            print("FO%.d=%.4f"%(i+1,FO[i]))
        if ConvergenceTest(FO, FD):
            print("FO和FD各项系数误差均小于3%，不需继续迭代")
            break
        else:
            print("FO和FD部分系数大于3%的误差，需要重新迭代")
        # 更新OD表
        for i in range(0, numofZones):
            for j in range(0, numofZones):
                PA_Table[i][j] *= FO[i]
        # 更新O,D
        Update_O = [0, 0, 0]
        Update_D = [0, 0, 0]
        for i in range(0, numofZones):
            for j in range(0, numofZones):
                Update_O[i] = PA_Table[i][j] + Update_O[i]
        for i in range(0, numofZones):
            for j in range(0, numofZones):
                Update_D[i] = PA_Table[j][i] + Update_D[i]
        O = Update_O
        D = Update_D
        print(f"第{time+2}次迭代计算OD表为：")
        for i in PA_Table:
            print(i)


# Utilized to trim the number
finallist = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
for i in range(0,numofZones):
    for j in range(0,numofZones):
        finallist[i][j]=PA_Table[i][j]
        finallist[i][-1]+=PA_Table[i][j]
        finallist[-1][i]+=PA_Table[j][i]
for i in range(0,numofZones):
    finallist[-1][-1]+= finallist[i][-1]
for i in finallist:
    for j in range(0, numofZones+1):
        i[j] = "%.3f" % i[j]
print("将来分布交通量表为：")
for i in finallist:
    print(i)
