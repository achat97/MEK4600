import numpy as np
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


def readData():
    dfAC = pd.read_csv("outfile_COM6_AC.txt",delim_whitespace=True,header=0,usecols=[1,2,3,5,7,9], names=['hh','mm','ss','la','lo','v'])
    dfAC = dfAC[~dfAC.isin(['error!']).any(axis=1)]
    dfAC = dfAC.astype('Int64')

    dfAC['time']= dfAC['hh'].astype(str)+':'+dfAC['mm'].astype(str)+':'+dfAC['ss'].astype(str)
    dfAC.drop(dfAC.columns[[0,1,2]], axis=1,inplace=True)
    first_column = dfAC.pop('time')
    dfAC.insert(0,'time', first_column)
    dfAC = dfAC.set_index('time')
    dfAC = dfAC.dropna()


    dfOP = pd.read_csv("outfile_COM7_OP.txt",header=0 ,usecols=[1,2,3,5,7,9], names=['hh','mm','ss','la','lo','v'])
    dfOP = dfOP[~dfOP.isin(['error!']).any(axis=1)]
    dfOP = dfOP.astype('Int64')
    dfOP["hh"] = dfOP["hh"]+1

    dfOP['time']= dfOP['hh'].astype(str)+':'+dfOP['mm'].astype(str)+':'+dfOP['ss'].astype(str)
    dfOP.drop(dfOP.columns[[0,1,2]], axis=1,inplace=True)
    first_column = dfOP.pop('time')
    dfOP.insert(0,'time', first_column)
    dfOP = dfOP.set_index('time')
    dfOP = dfOP.dropna()



    dfPT = pd.read_csv("outfile_COM9_PT_second_run.txt",header=0 ,usecols=[1,2,3,5,7,9], names=['hh','mm','ss','la','lo','v'])
    dfPT = dfPT[~dfPT.isin(['error!']).any(axis=1)]
    dfPT = dfPT.astype('Int64')

    dfPT['time']= dfPT['hh'].astype(str)+':'+dfPT['mm'].astype(str)+':'+dfPT['ss'].astype(str)
    dfPT.drop(dfPT.columns[[0,1,2]], axis=1,inplace=True)
    first_column = dfPT.pop('time')
    dfPT.insert(0,'time', first_column)
    dfPT = dfPT.set_index('time')
    dfPT = dfPT.dropna()



    return dfAC,dfOP,dfPT
