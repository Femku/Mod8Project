# pip install pandas
# pip install openpyxl

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
print(E_Reg)
print(E_Hol)
Cu=1
Cp=1
def e0(j,n):
    exp=0
    HolWeeks_list = [1, 8, 18, 28, 29, 30, 31, 32, 33, 42, 52]
    if n not in HolWeeks_list:
        for k in range(0,j+1):
                   exp += Regular_List[k]*Cu*(j-k)
        for k in range(j+1,NrAppointments_List[-1]+1):
                   exp += Regular_List[k]*Cp*(k-j)
    else:
        for k in range(0,j+1):
                   exp += Holiday_List[k]*Cu*(j-k)
        for k in range(j+1,NrAppointments_List[-1]+1):
                   exp += Holiday_List[k]*Cp*(k-j)
    return exp

def ei(i,j,n):
    expi=0
    HolWeeks_list=[1,8,18,28,29,30,31,32,33,42,52]
    if n not in HolWeeks_list:
        for k in range(0,j-i+1):
            if k<52:
               expi += Regular_List[k]*Cu*(j-i-k)
            else:
                continue
        for k in range(j-i+1,52):
            if j-i+1>0:
               expi += Regular_List[k]*Cp*(i+k-j)
            else:
                continue
    else:
        for k in range(0,j-i+1):
            expi += Holiday_List[k]*Cu*(j-i-k)
        for k in range(j-i+1,120-i):
            expi += Holiday_List[k]*Cp*(i+k-j)
    return expi

# def fn(i,n):
#     arr = numpy.array([])
#     for j in range(0,120,12):
#         v= Ei(i,j,n) +



def valuefunction(n):
        V = np.zeros(shape=(n + 1, 31))
        for i in range(31):
            # arr= np.zeros(shape=(1,10))
            ls=[]
            for j in range(0,120,12):
                ls.append(ei(i,j,n)) #array had a trouble with floar arguments
            z= min(ls)
            V[n, i] =z

        holWeeks_list = [1, 8, 18, 28, 29, 30, 31, 32, 33, 42, 52]
        for k in range(n - 1, 0, -1):
            for i in range(29, -1, -1):
                if k not in holWeeks_list:
                  # arr2=np.zeros(shape=(1,10))
                  for j in range(0,120,12):
                      ls1=[]
                      ls2=[]
                      for z in range(0,j-i+1):
                          if j-i>0:
                            print(f'z1{z}')
                            ls1.append(Regular_List[z]*V[n+1,0])
                            print(f"ls1{ls1}")
                          else:
                              continue
                      for z in range(j-i+1,120-i):
                          if (120-i)<52 and (j-i+1)>0:
                            print(f'z2{z}')
                            ls2.append(Regular_List[z]*V[n+1,i+z-j+1])
                            print(ls2)
                          else:
                              continue
                    # ls1=[Regular_List[z]*V[n+1,0] for z in range(0,j-1+1)]
                    # ls2=[Regular_List[z]*V[n+1,i+z-j+1] for z in range(j-1,52)]
                      ls3=ei(i,j,n)+ sum(ls1)+sum(ls2)
                  V[k, i] = min(ls3)
                  print(k, i, V[k, i])
                else:
                    arr2 = np.zeros(shape=(1, 10))
                    for j in range(0, 120, 12):
                        p = j / 12
                    ls1 = [Holiday_List[k]*V[n + 1, 0] for k in range(0, j - 1 + 1)]
                    ls2 = [Holiday_List[k] * V[n + 1, i + k - j + 1] for k in range(j - 1, 120 - i)]
                    arr2[1, p] = ei(i, j, n) + sum(ls1) + sum(ls2)
                    V[k, i] = min(arr2)
                    print(k, i, V[k, i])

        return V[1, 0]
#k * (i + 1), (k + i) * V[k + 1, i])
print(valuefunction(4))




