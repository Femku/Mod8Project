# pip install pandas ++
# pip install openpyxl ++
# pip install xlrd --
# pip install wheel --

import pandas as pd


data = pd.read_excel (r'C:\Users\femke\PycharmProjects\ProjectMod8Part1\2021 Stochastic Models project - Part 1 DP - data.xlsx', sheet_name='Access times', usecols=[0,1,2],header=1)
print(data)
print(data.columns.ravel()) #Column headers

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
print(E_Reg)
print(E_Hol)


