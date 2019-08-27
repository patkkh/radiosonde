import os,sys,glob
import pandas as pd
import numpy as np

class UPP():
    def __init__(self):
        self.name = "uppraw"
        self.columns = ["sec","p","t","u","wspd","wdir","alt","geo","dew","asc","lat","lon"]

    def minsec2sec(self,df):
        min = df.str.split(":").str[0].astype('int')
        sec = df.str.split(":").str[1].astype('int')
        return min*60 + sec

    def read_raw_kma(self,fi):
        skip_rows = 11
        columns = ["minsec","p","t","u","wspd_kt","wdir","lon","lat","alt","geo","dew","ascmm"]
        df = pd.read_csv(fi,skiprows=skip_rows,names=columns,sep="\s+",encoding='utf-8')
        df = df.replace(',',np.nan)
        df = df.replace('/////',np.nan)
        df = df.replace('//',np.nan)
        df['sec']   = self.minsec2sec(df.minsec)
        del(df['minsec'])
        df['wspd_kt'] = df['wspd_kt'].astype(float)
        df['wspd'] = df.wspd_kt * 0.51444
        del(df['wspd_kt'])
        df['ascmm'] = df['ascmm'].astype(float)
        df['asc']   = df.ascmm / 60
        del(df['ascmm'])
        df['alt'] = df['alt'].astype(float)
        df = df.sort_index(axis=1)
        return df

    def read_raw_vais(self,fi):
        skip_rows = 6
        columns = ["min","sec","p","t","u","wspd","wdir","alt","geo","dew","asc","lat","lon"]
        df = pd.read_csv(fi,skiprows=skip_rows,names=columns,sep="\s+",encoding='utf-8')
        df = df.replace(99999,np.nan)
        return df

    def read_gps_mdb(self,MDB):
        df = mdb.read_table(MDB,"GPS")
        sec = df.FlightTime / 1000
        sec = sec.astype('int')
        alt = df.Altitude
        nz  = len(alt)
        asc = np.zeros(nz)
        for i in np.arange(nz-1):
            dh = alt[i+1] - alt[i]
            dt = sec[i+1] - sec[i]
            if not dh == 0 and not dt == 0:
                asc[i+1] = dh / dt
        df['sec'] = sec
        df['asc'] = asc
        df['alt'] = df.Altitude
        del(df['Altitude'])
        return df

    def get_ftime(self,fi):
        dumy = fi.split("_")[-1]
        fdate = dumy.split(".")[0]
        fdate = pd.to_datetime(fdate)
        return fdate

    def get_ftime_bufr(self,fi):
        date = fi.split("_")[2]
        time = fi.split("_")[3]
        fdate = pd.to_datetime(date+time)
        return fdate

    def get_mdb_time(self,fi):
        dumy = fi.split("-")
        date = dumy[0]
        hour = dumy[1]
        fdate = date+hour+"0000"
        return fdate
