#!/usr/bin/env python3 

import os,sys
from pybufrkit.decoder import Decoder
from pybufrkit.dataquery import NodePathParser, DataQuerent
import numpy as np
import pandas as pd
from functools import reduce

def query_1d(bufr_message,id):
    query_result = DataQuerent(NodePathParser()).query(bufr_message, id)
    dic = query_result.results
    for k, v in dic.items():
        val = v[0]
        return val

def query(bufr_message,id):
    query_result = DataQuerent(NodePathParser()).query(bufr_message, id)
    dic = query_result.results
    for k, v in dic.items():
        val = v[0]
        val2 = reduce(lambda x,y: x+y,val)
        val3 = []
        for var in val2:
            if var == None : var = np.nan
            val3.append(var)
        return val3

def calc_ascrate(time,geop):
    nz   = len(time)
    asc  = np.zeros(nz,dtype=np.float)
    for i in np.arange(1,nz):
        dz = geop[i] - geop[i-1]
        dt = time[i] - time[i-1]
        if not dt == 0 and not dz == 0 :
            asc[i] = (geop[i] - geop[i-1]) / (time[i] - time[i-1])
        else : asc[i] = np.nan
    return asc

def main():
    BUFR_FILE = sys.argv[1]
    print("input: %s" % BUFR_FILE)
    basename  = os.path.basename(BUFR_FILE)
    fname     = basename.split(".")[0]
    gi        = "output/%s.txt" % fname
    print("output: %s" % gi)
    decoder = Decoder()
    with open(BUFR_FILE, 'rb') as ins:
        bufr_message = decoder.process(ins.read())
    slat  = query_1d(bufr_message,'005001')
    slon  = query_1d(bufr_message,'006001')

    #st   = query_1d(bufr_message,'001001')
    #id   = query_1d(bufr_message,'001002')
    #stid = str(st)+str("%0.3i"%id)

    time = np.array(query(bufr_message,'004086'))
    pres = np.array(query(bufr_message,'007004'),dtype=np.float)
    temp = np.array(query(bufr_message,'012101'),dtype=np.float)
    dewp = np.array(query(bufr_message,'012103'),dtype=np.float)
    geop = np.array(query(bufr_message,'010009'),dtype=np.float)
    wdir = np.array(query(bufr_message,'011001'),dtype=np.float)
    wspd = np.array(query(bufr_message,'011002'),dtype=np.float)
    dlat = np.array(query(bufr_message,'005015'),dtype=np.float)
    dlon = np.array(query(bufr_message,'006015'),dtype=np.float)

    lat  = slat+dlat
    lon  = slon+dlon
    columns = ["ptime","pres","temp","dewp","geop","wdir","wspd","lat","lon"]
    df = pd.DataFrame([time,pres,temp,dewp,geop,wdir,wspd,lat,lon])
    df2 = df.T
    df2.columns = columns
    df3 = df2[df2.ptime >= 0]
    df3.to_csv(gi,index=False,na_rep=np.nan,sep=",")

if __name__ == "__main__" : main()
    

        

