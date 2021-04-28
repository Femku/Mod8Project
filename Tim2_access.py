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


def access_times(n, c_p, c_u, c_e):
    V = np.zeros(shape=(n, n*max_new+1))#create array for the costs, with size weeks x waitingpeople
    choice = np.zeros(shape=(n, n * max_new + 1)) #create array for the choices, with size weeks x waitingpeople
    for i in range(n*max_new+1): #for all the possible number of people waiting do..
        V_all = [] #create empty array, to store all the costs for all the possibile decisions
        for d in D: #for all the decisions:
            summa = 0 #costs start on zero
            if d >= i: #if the number of open appointments is more than people on the waitinglist
                for ind in range(len(new_people)): #for all the possible new people calling:
                    j = new_people[ind]
                    if j <= d - i: #if there are unused appointments:
                        summa += p_n[(n+1) in holiday_weeks][ind]*(c_u*(d-i-j))#+c_e*(i+j)) #check whether it's a holidayweek or not and compute the corresponding expected costs
                    if d-i < j: #if there are people put on the waiting list:
                        summa += p_n[(n+1) in holiday_weeks][ind]*(c_p*(i+j-d))#+c_e*d)
            if d < i: #if there are less open appointments than the people on the waiting list
                for ind in range(len(new_people)):
                    j = new_people[ind]
                    summa += p_n[(n+1) in holiday_weeks][ind]*(c_p*(i+j-d))#+c_e*d)
            V_all.append(summa)
        V[n-1,i] = min(V_all)
        choice[n-1,i] = D[V_all.index(min(V_all))]
    for k in range(n-2,-1,-1): #now for the weeks n-1 till 0
        for i in range(k*max_new+1): #possible amount of people waiting
            V_all = []
            for d in D:
                summa = 0
                if d >= i:
                    for ind in range(len(new_people)):
                        j = new_people[ind]
                        if j <= d - i: #if there are unused appointments:
                            summa += p_n[(k+1) in holiday_weeks][ind] * (c_u * (d - i - j) + c_e*(i+j) + V[k+1, 0])
                        if d - i < j: #if there are too little appointments
                            summa += p_n[(k+1) in holiday_weeks][ind] * (c_p * (i + j - d) + c_e*d + V[k+1, i + j - d])
                if d < i:
                    for ind in range(len(new_people)):
                        j = new_people[ind]
                        summa += p_n[(k+1) in holiday_weeks][ind] * (c_p * (i + j - d) + c_e*d + V[k+1, i + j - d])
                V_all.append(summa)
            V[k, i] = min(V_all)
            choice[k, i] = D[V_all.index(min(V_all))]
    return V, choice


def access_times2(n, c_p, c_u, c_e,b,max_ins):
    V = np.zeros(shape=(n, n*max_new+1, n*max_new+1)) #create array to store the costs and threated persons
    choice = np.zeros(shape=(n, n * max_new + 1, n*max_new+1)) #create array for the choices and threated perons
    for i in range(n*max_new+1):
        for t in range(n*max_new): #for the amount of people treated
            if t < max_ins: #if the tot amount of people is less than the limit
                c_eb = c_e - b #shouldn't this be -b?
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
            for t in range(k*max_new+1):
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
                                summa += p_n[(k+1) in holiday_weeks][ind] * (c_u * (d - i - j) + c_eb*(i+j) + V[k+1, 0,t + i + j])
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


V, choices = access_times2(4, 1, 1, 0.5, 3,210)
print(f'Policy table: {V}')
# print(f'Choices: {choices[2,10,:]}')
print(f' zerosarray(2,2,3): {np.zeros(shape = (2,2,3))}')
### To convert the data to excel; the data should be 2d
# df = pd.DataFrame(V, columns = ['week', 'waiting'])
# df.to_excel(r'C:\Users\femke\PycharmProjects\Mod8Project\Access Time Output.xlsx', index = False) #sheet_name='Your sheet name'