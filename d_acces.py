import pandas as pd
import numpy as np


data = pd.read_excel ('2021 Stochastic Models project - Part 1 DP - data.xlsx', sheet_name='Access times', usecols=[0,1,2],header=1)
# print(data)
# print(data.columns.ravel()) #Column headers

regular = pd.DataFrame(data, columns= ['Regular week'])
holiday = pd.DataFrame(data, columns= ['Holiday week'])
appointments = pd.DataFrame(data, columns= ['Number of appointment requests'])

NrAppointments_List = data['Number of appointment requests'].values.tolist() #list of probabilities
Regular_List = data['Regular week'].values.tolist()
Holiday_List = data['Holiday week'].values.tolist()


E_Reg = 0
E_Hol = 0
for i in range(len(NrAppointments_List)):
    E_Reg += NrAppointments_List[i]*Regular_List[i] #the expected number of appointment requests in Regular week
    E_Hol += NrAppointments_List[i]*Holiday_List[i] #the expected number of appointment requests in Holiday week
# print(E_Reg)
# print(E_Hol)
Cu=0.1
Cp=0.1
E=np.zeros(shape=(31,11))
for i in range(31):
    for j in range(11):
        E[i,j] = (sum(NrAppointments_List[k-24]*Regular_List[k-24]*Cu*(12*j-i-k) for k in range(max(0,24),min(12*j-i+1,76)))
            +sum(NrAppointments_List[k-24]*Regular_List[k-24]*Cp*(i+k-12*j) for k in range(max(24,12*j-i),min(120-i,76))))



def valuefunction(n):
    V=np.zeros(shape=(n+1,1000))
    holidayweeks=[1]
    for i in range(31):
        V[n, i] = np.amin(E[i,])
        # print(n,i,V[n,i])
    for m in range(n - 1, 0, -1):
        # if m not in holidayweeks:
           for i in range(29,-1,-1):
                V[m,i] = min(E[i,j]
                    +sum(NrAppointments_List[k-24]*Regular_List[k-24]*V[m+1,0] for k in range(24,min(12*j-i,76)))
                    +sum(NrAppointments_List[k-24]*Regular_List[k-24]*V[m+1,i+k-12*j] for k in range(max(24,12*j-i),min(76,120-i)))
                        for j in range(11))
                # print(m,i,V[m,i])
        # else:
        #     for i in range(29, -1, -1):
        #         V[m, i] = min(E[i, j]
        #                       + sum(NrAppointments_List[k - 24] * Holiday_List[k - 24] * V[m + 1, 0] for k in
        #                             range(24, min(12 * j - i, 76)))
        #                       + sum(
        #             NrAppointments_List[k - 24] * Holiday_List[k - 24] * V[m + 1, i + k - 12 * j] for k in
        #             range(max(24, 12 * j - i), min(76, 120 - i)))
        #                       for j in range(11))
    return V[1,0]

print(valuefunction(4))
