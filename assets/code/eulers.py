#!/usr/bin/env python3
import numpy as np

TRUE_VALUE = np.e - 2

def yPrime(t, y):
    return t + y

def eulersMethod(yPrime, N, a, b, alpha):
    h = (b-a) / N
    w = alpha
    for i in range(N):
        time = a + i * h
        w = w + h * yPrime(time, w)
    return w

def printResults(eulers_res):
    for i in range(len(eulers_res)):
        if i != 0:
            print('{} & ${:0.7e}$ & ${:0.5f}$ \\\\ '.format(2**(i+2), eulers_res[i], eulers_res[i-1]/eulers_res[i]))
        else:
            print('4 & ${:0.7e}$ &  \\\\ '.format(eulers_res[i]))

if __name__ == "__main__":
    errors = []
    for i in range(2,18):
        N = np.power(2, i)
        result = eulersMethod(yPrime, N, a=0, b=1, alpha=0)
        errors.append(result - TRUE_VALUE) 
    printResults(errors)   