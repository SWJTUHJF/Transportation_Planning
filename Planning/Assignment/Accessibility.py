# -*- coding: utf-8 -*-
"""
@Time    : 2023/12/26 15:09
@Author  : He Junfeng
@StudentID    : 2021113362
@File    : Accessibility.py
"""
"""
This file is to calculate the accessibility of the specfic region
The network is from Fig3(Hansen,1959)
We manually set the employment as the attraction of one zone
"""
Region = [1, 2, 3, 4]
dist = [0,10,25,20,15,30]
employment = [0,2000, 1500, 3000, 5000]
access = [0 for i in range(5)]
access[1] = employment[2]/(dist[2]**2.2)+employment[3]/(dist[3]**2.2)+employment[4]/(dist[4]**2.2)
access[2] = employment[3]/(dist[1]**2.2)+employment[1]/(dist[2]**2.2)
access[3] = employment[2]/(dist[1]**2.2)+employment[1]/(dist[3]**2.2)+employment[4]/(dist[5]**2.2)
access[4] = employment[1]/(dist[4]**2.2)+employment[3]/(dist[5]**2.2)
for index,value in enumerate(access):
    if index!=0:
        print(f"Accessibility of Zone {index}:",value)


