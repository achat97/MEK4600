import numpy as np
import pandas as pd
from geopy import distance
import matplotlib.pyplot as plt
from readData import *

plt.style.use('seaborn-v0_8')
dfAC,dfOP,dfPT = readData()

def latlon(position):
    if position != 0:
        l = int(str(position)[:2])
        min = float(str(position)[2:4]+"."+str(position)[4:])/60
        ll = l+min
        return ll

startLa,startLo = dfAC['la']['10:58:17'],dfAC['lo']['10:58:17']
startLa,startLo = latlon(startLa),latlon(startLo)
startPoint = (startLa,startLo)

dfAC['la'] = dfAC['la'].apply(latlon)
dfAC['lo'] = dfAC['lo'].apply(latlon)

dfOP['la'] = dfOP['la'].apply(latlon)
dfOP['lo'] = dfOP['lo'].apply(latlon)

dfOP = dfOP.dropna()

AClatlon,OPlatlon = list(dfAC[['la','lo']].apply(tuple, axis=1)),list(dfOP[['la','lo']].apply(tuple, axis=1))
ACdistance,OPdistance = np.zeros(len(AClatlon)),np.zeros(len(OPlatlon))

for i in range(len(ACdistance)):
    ACdistance[i] = distance.distance(AClatlon[i],startPoint).meters

for i in range(len(OPdistance)):
    OPdistance[i] = distance.distance(OPlatlon[i],startPoint).meters

dfAC['distance'] = ACdistance
dfOP['distance'] = OPdistance

def plotRounds(round1=True,round2=True,round3=True):

    if round1 == True:
        plt.title("Round 1")
        plt.plot(dfAC['lo']['11:13:2':'11:17:12'],dfAC['la']['11:13:2':'11:17:12'],label="Sensor 1")
        plt.plot(dfOP['lo']['11:13:2':'11:17:12'],dfOP['la']['11:13:2':'11:17:12'],label="Sensor 2")
        plt.title('Round 1')
        plt.xlabel("longiutde")
        plt.ylabel("latitude")
        plt.legend()
        plt.show()

    if round2 == True:
        plt.title("Round 2")
        plt.plot(dfAC['lo']['11:19:5':'11:24:3'],dfAC['la']['11:19:5':'11:24:3'],label="Sensor 1")
        plt.plot(dfOP['lo']['11:19:5':'11:24:2'],dfOP['la']['11:19:5':'11:24:2'],label="Sensor 2")
        plt.title('Round 2')
        plt.xlabel("longiutde")
        plt.ylabel("latitude")
        plt.legend()
        plt.show()

    if round3 == True:
        plt.title("Round 3")
        plt.plot(dfAC['lo']['11:42:2':'11:47:10'],dfAC['la']['11:42:2':'11:47:10'],label="Sensor 1")
        plt.plot(dfOP['lo']['11:42:5':'11:47:13'],dfOP['la']['11:42:5':'11:47:13'],label="Sensor 2")
        plt.title('Round 3')
        plt.xlabel("longiutde")
        plt.ylabel("latitude")
        plt.legend()
        plt.show()


def Distance(df1,df2):
    times = []
    index1 = list(df1.index)
    index2 = list(df2.index)

    for time1 in index1:
        for time2 in index2:
            if time1 == time2:
                times.append(time1)

    dist1 = np.zeros(len(times))
    dist2 = np.zeros(len(times))

    for i in range(len(times)):
        dist1[i] = df1['distance'][times[i]]
        dist2[i] = df2['distance'][times[i]]
    return times,dist1,dist2


times1,round1dist1,round1dist2 = Distance(dfAC['11:13:2':'11:17:12'],dfOP['11:13:2':'11:17:12'])
validation1 = abs(round1dist1-round1dist2)
error1 = abs(validation1-5)
MAE1 = np.sum(error1)/len(error1)


times2,round2dist1,round2dist2 =  Distance(dfAC['11:19:5':'11:24:3'],dfOP['11:19:5':'11:24:2'])
validation2 = abs(round2dist1-round2dist2)
error2 = abs(validation2-5)
MAE2 = np.sum(error2)/len(error2)


print(f"MAE,round 1: {MAE1:.2f}m")
print(f"MAE,round 2: {MAE2:.2f}m")

plotRounds()

plt.plot(times1,error1)
plt.hlines(y=1.8,xmin=times1[0],xmax=times1[-1],linestyles="--",label="Stated Accuracy")
plt.legend()
plt.title('Error Round 1')
plt.xlabel('time')
plt.ylabel('error[m]')
plt.show()

plt.plot(times2,error2)
plt.hlines(y=1.8,xmin=times2[0],xmax=times2[-1],linestyles="--",label="Stated Accuracy")
plt.legend()
plt.title('Error Round 2')
plt.xlabel('time')
plt.ylabel('error[m]')
plt.show()
