#!/usr/bin/python
# the following command will remove all the .txt files
# find . -name "*.txt" -type f -delete
import timeit
import sys
import random
import math
from copy import deepcopy


def kk(A):
    while len(A) > 1:
        largest = max(A)
        A.remove(largest)
        second_largest = max(A)
        A.remove(second_largest)
        A.append(largest - second_largest)
    return A[0]


def random_sol_standard(n):
    S = []
    for i in range(n):
        S.append(random.choice([-1, 1]))
    return S


def random_neighbor_standard(S):
    Sp = deepcopy(S)
    i = random.randrange(0, len(S))
    j = random.randrange(0, len(S))
    while i == j:
        i = random.randrange(0, len(S))
        j = random.randrange(0, len(S))
    Sp[i] = -S[i]
    if random.random() > 0.5:
        Sp[j] = -Sp[j]
    return Sp


def random_sol_prepart(n):
    P = []
    for i in range(n):
        P.append(random.randrange(1, n + 1))
    return P


def random_neighbor_prepart(P):
    Pp = deepcopy(P)
    i = random.randrange(0, len(P))
    j = random.randrange(1, len(P))
    while Pp[i] == j:
        i = random.randrange(0, len(P))
        j = random.randrange(0, len(P))
    Pp[i] = j
    return Pp


def residue_standard(A, S):
    multiplied = [a * b for a, b in zip(A, S)]
    u = abs(sum(multiplied))
    return u


def residue_prepart(A, P):
    A_2 = []
    for i in range(len(A)):
        A_2.append(0)
    for j in range(len(A)):
        A_2[P[j] - 1] = A_2[P[j] - 1] + A[j]
    r = kk(A_2)
    return r


max_iter = 25000


def standard_repeated_random(A, S):
    for i in range(max_iter):
        S_2 = random_sol_standard(len(A))
        if residue_standard(A, S_2) < residue_standard(A, S):
            S = S_2
    return residue_standard(A, S)


def pre_part_repeated_random(A, P):
    for i in range(max_iter):
        P_2 = random_sol_prepart(len(A))
        if residue_prepart(A, P_2) < residue_prepart(A, P):
            P = P_2
    return residue_prepart(A, P)


def standard_hill_climbing(A, S):
    SR = residue_standard(A, S)
    for i in range(max_iter):
        S_2 = random_neighbor_standard(S)
        S_2R = residue_standard(A, S_2)
        if S_2R < SR:
            S = S_2
            SR = S_2R
    return SR


def pre_part_hill_climbing(A, S):
    SR = residue_prepart(A, S)
    for i in range(max_iter):
        S_2 = random_neighbor_prepart(S)
        S_2R = residue_prepart(A, S_2)
        if S_2R < SR:
            S = S_2
            SR = S_2R
    return SR


def T(i):
    return (10 ** 10) * (0.8 ** (math.floor(i / 300)))


def standard_sim_ann(A, S):
    SR = residue_standard(A, S)
    S_3 = deepcopy(S)
    S_3R = deepcopy(SR)

    for i in range(max_iter):
        S_2 = random_neighbor_standard(S)
        S_2R = residue_standard(A, S_2)
        if S_2R < SR:
            S = S_2
            SR = S_2R
        else:
            if random.random() < math.exp(-(S_2R - SR) / T(i)):
                S = S_2
                SR = S_2R
        if SR < S_3R:
            S_3 = S
            S_3R = SR
    return S_3R


def pre_part_sim_ann(A,S):
    SR = residue_prepart(A, S)
    S_3 = deepcopy(S)
    S_3R = deepcopy(SR)

    for i in range(max_iter):
        S_2 = random_neighbor_prepart(S)
        S_2R = residue_prepart(A, S_2)
        if S_2R < SR:
            S = S_2
            SR = S_2R
        else:
            if random.random() < math.exp(-(S_2R - SR) / T(i)):
                S = S_2
                SR = S_2R
        if SR < S_3R:
            S_3 = S
            S_3R = SR
    return S_3R


def tostringlist(lst):
    string = ""
    for item in lst[:len(lst) - 1]:
        string += str(item)
        string += ", "
    string += str(lst[len(lst) - 1])
    string += "\n"
    return string


# create the csv file
with open('results_final%d.csv' % sys.argv[1], 'wb') as f:
    f.write(tostringlist(['kk_res', 'kk_time', 'srr_res', 'srr_time', 'pprr_res', 'pprr_time', 'shc_res', 'shc_time', 'pphc_res', 'pphc_time', 'ssa_res', 'ssa_time', 'ppsa_res', 'ppsa_time']))
    for i in range(1, 101):

        num_set = random.sample(xrange(1, 10**12), 100)
        S = random_sol_standard(len(num_set))
        P = random_sol_prepart(len(num_set))

        row = []

        start = timeit.default_timer()
        output = kk(deepcopy(num_set))
        row.append(output)
        # print "kk output: %s" % output
        end = timeit.default_timer()
        time = end - start
        row.append(time)

        start = timeit.default_timer()
        output = standard_repeated_random(deepcopy(num_set), deepcopy(S))
        row.append(output)
        end = timeit.default_timer()
        time = end - start
        row.append(time)

        start = timeit.default_timer()
        output = pre_part_repeated_random(deepcopy(num_set), deepcopy(P))
        row.append(output)
        end = timeit.default_timer()
        time = end - start
        row.append(time)

        start = timeit.default_timer()
        output = standard_hill_climbing(deepcopy(num_set), deepcopy(S))
        row.append(output)
        end = timeit.default_timer()
        time = end - start
        row.append(time)

        start = timeit.default_timer()
        output = pre_part_hill_climbing(deepcopy(num_set), deepcopy(P))
        row.append(output)
        end = timeit.default_timer()
        time = end - start
        row.append(time)

        start = timeit.default_timer()
        output = standard_sim_ann(deepcopy(num_set), deepcopy(S))
        row.append(output)
        end = timeit.default_timer()
        time = end - start
        row.append(time)

        start = timeit.default_timer()
        output = pre_part_sim_ann(deepcopy(num_set), deepcopy(P))
        row.append(output)
        end = timeit.default_timer()
        time = end - start
        row.append(time)

        f.write(tostringlist(row))
