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


def standard_sol(n):
    S = []
    for i in range(n):
        S.append(random.choice([-1, 1]))
    return S


def standard_random_move(S):
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


def pre_part(n):
    P = []
    for i in range(n):
        P.append(random.randrange(1, n + 1))
    return P


def pre_part_random_move(P):
    Pp = deepcopy(P)
    i = random.randrange(0, len(P))
    j = random.randrange(1, len(P))
    while Pp[i] == j:
        i = random.randrange(0, len(P))
        j = random.randrange(0, len(P))
    Pp[i] = j
    return Pp


def standard_residue(A, S):
    multiplied = [a * b for a, b in zip(A, S)]
    u = abs(sum(multiplied))
    return u


def pre_part_residue(A, P):
    A_2 = []
    # print "pre part residue: %s" % A
    # print P
    for i in range(len(A)):
        A_2.append(0)
    for j in range(len(A)):
        # print A
        A_2[P[j] - 1] = A_2[P[j] - 1] + A[j]
    r = kk(A_2)
    return r


max_iter = 25000


def standard_repeated_random(A, S):
    for i in range(max_iter):
        S_2 = standard_sol(len(A))
        if standard_residue(A, S_2) < standard_residue(A, S):
            S = S_2
    return standard_residue(A, S)


def pre_part_repeated_random(A, P):
    for i in range(max_iter):
        P_2 = pre_part(len(A))
        if pre_part_residue(A, P_2) < pre_part_residue(A, P):
            P = P_2
    return pre_part_residue(A, P)


def standard_hill_climbing(A, S):
    SR = standard_residue(A, S)
    for i in range(max_iter):
        S_2 = standard_random_move(S)
        S_2R = standard_residue(A, S_2)
        if S_2R < SR:
            S = S_2 
            SR = S_2R
    return SR 


def pre_part_hill_climbing(A, S):
    SR = pre_part_residue(A, S)
    for i in range(max_iter):
        S_2 = pre_part_random_move(S)
        S_2R = pre_part_residue(A, S_2)
        if S_2R < SR:
            S = S_2
            SR = S_2R
    return SR 


def T(i):
    return (10 ** 10) * (0.8 ** (math.floor(i / 300)))


def standard_sim_ann(A, S): 
    SR = standard_residue(A, S)
    S_3 = deepcopy(S)
    S_3R = deepcopy(SR)

    for i in range(max_iter):
        S_2 = standard_random_move(S)
        S_2R = standard_residue(A, S_2)
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
    SR = pre_part_residue(A, S)
    S_3 = deepcopy(S)
    S_3R = deepcopy(SR)

    for i in range(max_iter):
        S_2 = pre_part_random_move(S)
        S_2R = pre_part_residue(A, S)
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
with open('results.csv', 'wb') as f:
    f.write(tostringlist(['kk_res', 'kk_time', 'srr_res', 'srr_time', 'pprr_res', 'pprr_time', 'shc_res', 'shc_time', 'pphc_res', 'pphc_time', 'ssa_res', 'ssa_time', 'ppsa_res', 'ppsa_time']))
    for i in range(1, 11):

        # generate file of 100 random ints
        num_set = random.sample(xrange(1, 10**12), 100)
        # print num_set
        S = standard_sol(len(num_set))
        # print S
        P = pre_part(len(num_set))
        # print P

        row = []

        # num_set = []
        # input_file = open(sys.argv[1], 'r')
        # for line in input_file:
        #   e = int(line)
        #   num_set.append(e)

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
        # print "srr output: %s" % output
        end = timeit.default_timer()
        time = end - start
        row.append(time)

        start = timeit.default_timer()
        output = pre_part_repeated_random(deepcopy(num_set), deepcopy(P))
        row.append(output)
        # print "pprm output: %s" % output
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
