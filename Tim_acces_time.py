import pandas as pd
import numpy as np

data = pd.read_excel ('2021 Stochastic Models project - Part 1 DP - data.xlsx', sheet_name='Access times', usecols=[0,1,2],header=1)

new_people = data['Number of appointment requests'].values.tolist() #list of probabilities
p_r = data['Regular week'].values.tolist()
p_h = data['Holiday week'].values.tolist()

# stages: n = week nr., n \in {0,1,2,...,51}
# states: i = # of people on waiting list
# decision space: D = # of slots open
D = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120] # ,132,144,156,178
# Optimal value function: f_n(i) is the minimum expected cost, in week n with i people on the waiting list

holiday_weeks = {1, 8, 18, 28, 29, 30 , 31, 22, 33, 42, 52}
min_new = new_people[0]
max_new = new_people[-1]

p_n = {False: p_r,True: p_r}


def access_times(n, c_p, c_u):
    V = np.zeros(shape=(n, n*max_new+1))
    choice = np.zeros(shape=(n, n * max_new + 1))
    tot_people=0
    for i in range(n*max_new+1):
        V_all = []
        for d in D:
            summa = 0
            if d >= i:
                for ind in range(len(new_people)):
                    j = new_people[ind]
                    if j <= d - i:
                        summa += p_n[(n+1) in holiday_weeks][ind]*c_u*(d-i-j)
                        #tot_people += p_n[(n+1) in holiday_weeks][ind]*(i+j)
                    if d-i < j:
                        summa += p_n[(n+1) in holiday_weeks][ind]*c_p*(i+j-d)
                        #tot_people += p_n[(n+1) in holiday_weeks][ind]*d
            if d < i:
                for ind in range(len(new_people)):
                    j = new_people[ind]
                    summa += p_n[(n+1) in holiday_weeks][ind]*c_p*(i+j-d)
            V_all.append(summa)
        V[n-1,i] = min(V_all)
        choice[n-1,i] = D[V_all.index(min(V_all))]
    for k in range(n-2,-1,-1):
        for i in range(k*max_new+1):
            V_all = []
            for d in D:
                summa = 0
                if d >= i:
                    for ind in range(len(new_people)):
                        j = new_people[ind]
                        if j <= d - i:
                            summa += p_n[(k+1) in holiday_weeks][ind] * (c_u * (d - i - j) + V[k+1,0])
                            # tot_people += p_n[(n + 1) in holiday_weeks][ind] * (i + j)
                        if d - i < j:
                            summa += p_n[(k+1) in holiday_weeks][ind] * (c_p * (i + j - d) + V[k+1,i + j - d])
                if d < i:
                    for ind in range(len(new_people)):
                        j = new_people[ind]
                        summa += p_n[(k+1) in holiday_weeks][ind] * (c_p * (i + j - d) + V[k+1,i + j - d])
                        # tot_people += p_n[(n + 1) in holiday_weeks][ind] * d
                V_all.append(summa)
            V[k, i] = min(V_all)
            choice[k, i] = D[V_all.index(min(V_all))]
    return V, choice, tot_people


V, choices, tot = access_times(1,1,1)
print(V)
print(choices)
print(tot)