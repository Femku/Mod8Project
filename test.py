import pandas as pd
import numpy as np


data = pd.read_excel (r'C:\Users\femke\PycharmProjects\ProjectMod8Part1\2021 Stochastic Models project - Part 1 DP - data.xlsx', sheet_name='Access times', usecols=[0,1,2],header=1)
print(data)
# print(data.columns.ravel()) #Column headers

# regular = pd.DataFrame(data, columns= ['Regular week'])
# holiday = pd.DataFrame(data, columns= ['Holiday week'])
# appointments = pd.DataFrame(data, columns= ['Number of appointment requests'])

NrAppointments_List = data['Number of appointment requests'].values.tolist() #list of probabilities
Regular_List = data['Regular week'].values.tolist()
Holiday_List = data['Holiday week'].values.tolist()

E_Reg = 0
E_Hol = 0
for i in range(len(NrAppointments_List)):
    E_Reg += NrAppointments_List[i]*Regular_List[i] #the expected number of appointment requests in Regular week
    E_Hol += NrAppointments_List[i]*Holiday_List[i] #the expected number of appointment requests in Holiday week
print(f'expected number of patients in regular week: {E_Reg}')
print(f'expected number of patients in holiday week: {E_Hol}')
Cu=1
Cp=1

#week 1: zero on waiting list
def slots_to_open(n):
    HWeeks_list = [1] # 8, 18, 28, 29, 30, 31, 32, 33, 42, 52]
    tot_tpeople=0
    if n not in HWeeks_list:
       costsd= dict()
       waitingpersonsd=dict()
       for d in range(0,121,12):
           costs=0
           waitingpersons=0
           for x in range(len(Regular_List)):
               t= Regular_List[x]*(d - NrAppointments_List[x])
               if t>0:
                   cost= t*Cu
                   waiting=0
                   tot_tpeople
               else:
                   cost= -t*Cp
                   waiting=-t
               costs += cost
               waitingpersons += waiting
           costsd[d]=costs
           waitingpersonsd[d]=waitingpersons
    else:
        costsd = dict()
        waitingpersonsd = dict()
        for d in range(0, 121, 12):
            costs = 0
            waitingpersons = 0
            for x in range(len(Holiday_List)):
                t = Holiday_List[x] * (d - NrAppointments_List[x])
                if t > 0:
                    cost = t * Cu
                    waiting = 0
                else:
                    cost = -t * Cp
                    waiting = -t
                costs += cost
                waitingpersons += waiting
            costsd[d] = costs
            waitingpersonsd[d]= waitingpersons
    slots= min(costsd, key = costsd.get)
    mincost= costsd[slots]

    return slots, mincost, waitingpersonsd

#week 2: possible on waiting list from week 1 + patients
def slots_to_open_2(n):
    HWeeks_list = [1]  # 8, 18, 28, 29, 30, 31, 32, 33, 42, 52]
    if n not in HWeeks_list:
        costsd = dict()
        waitingpersonsd = dict()
        for d in range(0, 121, 12):
            costs = 0
            waitingpersons = 0
            (x, wait) = slots_to_open_2(n-1)
            for x in range(len(Regular_List)):
                t = Regular_List[x] * (d - NrAppointments_List[x] - wait[d])
                if t > 0:
                    cost = t * Cu
                    waiting = 0
                else:
                    cost = -t * Cp
                    waiting = -t
                costs += cost
                waitingpersons += waiting
            costsd[d] = costs
            waitingpersonsd[d] = waitingpersons
    else:
        costsd = dict()
        waitingpersonsd = dict()
        for d in range(0, 121, 12):
            costs = 0
            waitingpersons = 0
            x,wait= slots_to_open(n-1)
            for x in range(len(Holiday_List)):
                t = Holiday_List[x] * (d - NrAppointments_List[x]- wait[d])
                if t > 0:
                    cost = t * Cu
                    waiting = 0
                else:
                    cost = -t * Cp
                    waiting = -t
                costs += cost
                waitingpersons += waiting
            costsd[d] = costs
            waitingpersonsd[d] = waitingpersons
    slots = min(costsd, key=costsd.get)

    return slots, waitingpersonsd

#start with week 4: minimize the costs and don't take into account the future costs (for waiting persons)
def week4(i,n):
    HWeeks_list = [1]  # 8, 18, 28, 29, 30, 31, 32, 33, 42, 52]
    if n not in HWeeks_list:
        costsd = dict()
        E = np.zeros(shape=(225, 11)) #11 decisions(0,12,...120)
        for i in range(225):
            for j in range(11):
                E[i,j]=(sum(NrAppointments_List[k-24]*Regular_List[k-24]*Cu*(12*j-i-k) for k in range(max(0,24),min(12*j-i+1,76)))
            +sum(NrAppointments_List[k-24]*Regular_List[k-24]*Cp*(i+k-12*j) for k in range(max(24,12*j-i),min(120-i,76))))

        for d in range(0, 121, 12):
            costs = 0

            for x in range(len(Regular_List)):
                t = Regular_List[x] * (d - NrAppointments_List[x])
                if t > 0:
                    cost = t * Cu
                else:
                    cost = -t * Cp
                costs += cost

            costsd[d] = costs

    else:
        costsd = dict()
        waitingpersonsd = dict()
        for d in range(0, 121, 12):
            costs = 0
            waitingpersons = 0
            x, wait = slots_to_open(n - 1)
            for x in range(len(Holiday_List)):
                t = Holiday_List[x] * (d - NrAppointments_List[x] - wait[d])
                if t > 0:
                    cost = t * Cu
                    waiting = 0
                else:
                    cost = -t * Cp
                    waiting = -t
                costs += cost
                waitingpersons += waiting
            costsd[d] = costs
            waitingpersonsd[d] = waitingpersons
    slots = min(costsd, key=costsd.get)



# (x,y) = slots_to_open(2)
print(slots_to_open(1))
print(slots_to_open_2(2))
print(slots_to_open_2(3))
print(slots_to_open_2(4))




