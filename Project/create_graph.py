from setup import *
import numpy as np


def create_graph(F, A, D):
    mat = np.eye(F+2)
    for i in range(F+2):
        for j in range(F+2):
            if j > i and A[j] - D[i] >= 0 :
                mat[i][j] = (A[j] - D[i])**2
            else :
                mat[i][j] = -1
    return mat

file = 'GAP4_9.txt'
G, F, T0, TM, ids, a, d, gates =read (file)
A = [T0]+a+[TM]
D = [T0]+d+[TM]

# print(create_graph(F, A, D))