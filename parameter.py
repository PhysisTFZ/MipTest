# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 09:45:48 2022

@author: withp
"""
import random
import numpy as np
wMax = 2
hMax = 2
def GenerateWH(M, N) :
    weight = np.zeros((M, N))
    h = np.zeros((M, N))
    for m in range(M):
        for n in range(N):
           weight[m,n] = random.randrange(1, wMax, 1) 
           h[m, n] = random.randrange(1, hMax, 1) 
    return weight, h