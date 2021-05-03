# pip install pandas ++
# pip install openpyxl ++

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

p_n = {False: p_r,True: p_h}


def access_times(n, c_p, c_u, c_e, b, max_ins):
    """
       Computes the optimal decision for deciding how many slots to open. By minimizing the expected costs.
       Returning the decisions and costs in a matrix
       :param n: number of weeks (n in {0,1,2,...,51})
       :param c_p: cost for putting a patient on the waiting list for one week
       :param c_u: cost for an unused appointment
       :param c_e: cost for a treatment
       :param b: reimbursement for a treatment
       :param max_ins: maximal number of patients that the outpatient clinic gets a reimbursument

       :return: results of the optimal value function
       :return: The optimal decisions
       """
    V = np.full(shape=(n, n*max_new+1, n*max_new+1), fill_value= np.inf)
    choice = np.full(shape=(n, n * max_new + 1, n*max_new+1), fill_value= np.inf)
    for i in range(n*max_new+1):
        for t in range(n*max_new+1-i):
            if t < max_ins:
                c_eb = c_e - b
            if t >= max_ins:
                c_eb = c_e
            V_all = []
            for d in D:
                summa = 0
                if d >= i:
                    for ind in range(len(new_people)):
                        j = new_people[ind]
                        if j <= d - i:
                            summa += p_n[(n+1) in holiday_weeks][ind]*(c_u*(d-i-j)+c_eb*(i+j))
                        if d-i < j:
                            summa += p_n[(n+1) in holiday_weeks][ind]*(c_p*(i+j-d)+c_eb*d)
                if d < i:
                    for ind in range(len(new_people)):
                        j = new_people[ind]
                        summa += p_n[(n+1) in holiday_weeks][ind]*(c_p*(i+j-d)+c_eb*d)
                V_all.append(summa)
            V[n-1,i,t] = min(V_all)
            choice[n-1,i,t] = D[V_all.index(min(V_all))]
    for k in range(n-2,-1,-1):
        for i in range(k*max_new+1):
            for t in range(k*max_new+1-i):
                if t < max_ins:
                    c_eb = c_e - b
                if t >= max_ins:
                    c_eb = c_e
                V_all = []
                for d in D:
                    summa = 0
                    if d >= i:
                        for ind in range(len(new_people)):
                            j = new_people[ind]
                            if j <= d - i:
                                summa += p_n[(k+1) in holiday_weeks][ind] * (c_u * (d - i - j) + c_eb*(i+j) + V[k+1, 0, t + i + j])
                            if d - i < j:
                                summa += p_n[(k+1) in holiday_weeks][ind] * (c_p * (i + j - d) + c_eb*d + V[k+1, i + j - d, t + d])
                    if d < i:
                        for ind in range(len(new_people)):
                            j = new_people[ind]
                            summa += p_n[(k+1) in holiday_weeks][ind] * (c_p * (i + j - d) + c_eb*d + V[k+1, i + j - d, t + d])
                    V_all.append(summa)
                V[k, i, t] = min(V_all)
                choice[k, i, t] = D[V_all.index(min(V_all))]
    return V, choice


n = 4
c_p = 1
c_u = 1
c_e = 0.5
d = 1
max_ins = 100
V, choices = access_times(n, c_p, c_u, c_e, d, max_ins)
print(V)
with pd.ExcelWriter("output.xlsx") as writer:
    for i in range(n):
        df1 = pd.DataFrame(V[i,:,:])
        df2 = pd.DataFrame(choices[i,:,:])
        df1.to_excel(excel_writer=writer, sheet_name=f'n={i} E(c)')
        df2.to_excel(excel_writer=writer, sheet_name=f'n={i} choices')
