import numpy as np
import pandas as pd
import datetime
import time


cols2keep = ['date','close','open','max','min','volume']

mk_data_sanb11 = pd.read_csv('../../data/raw/market_data_sanb11_raw.csv',usecols=cols2keep)
mk_data_itub4 = pd.read_csv('../../data/raw/market_data_itub4_raw.csv',usecols=cols2keep)
mk_data_bbdc3 = pd.read_csv('../../data/raw/market_data_bbdc3_raw.csv',usecols=cols2keep)
mk_data_bvsp = pd.read_csv('../../data/raw/market_data_bvsp_raw.csv',usecols=cols2keep)

mk_data_sanb11['date'] = mk_data_sanb11.date.apply(lambda x: datetime.datetime.strptime(x, "%d/%m/%Y"))
mk_data_itub4['date'] = mk_data_itub4.date.apply(lambda x: datetime.datetime.strptime(x, "%d/%m/%Y"))
mk_data_bbdc3['date'] = mk_data_bbdc3.date.apply(lambda x: datetime.datetime.strptime(x, "%d/%m/%Y"))
mk_data_bvsp['date'] = mk_data_bvsp.date.apply(lambda x: datetime.datetime.strptime(x, "%d/%m/%Y"))

mk_data_sanb11.sort_values(by='date',ascending=False,inplace=True)
mk_data_itub4.sort_values(by='date',ascending=False,inplace=True)
mk_data_bbdc3.sort_values(by='date',ascending=False,inplace=True)
mk_data_bvsp.sort_values(by='date',ascending=False,inplace=True)



def mk_returnsPrev(df, open_close, window):
    ls = []
    ls_nan = []
    for i,item in enumerate(df[open_close]):
        last = len(df[open_close]) - window
        if i == last:
            break
        div = df[open_close][i+window]
        ret = (item - div) / div
        ls.append(ret)
        diff = len(df[open_close]) - len(ls)
    for j in range(0,diff):
        ls_nan.append(np.nan)
    return ls + ls_nan
    

    def mk_returnsNext(df, open_close, window):
    ls = []
    ls_nan = []
    for i, item in enumerate(df[open_close]):
        if i in range(0,window):
            continue
        den = df[open_close][i-window]
        ret = (den - item) / item
        ls.append(ret)
        diff = len(df[open_close]) - len(ls)
    for j in range(0,diff):
        ls_nan.append(np.nan)
    return ls_nan + ls


for i in range(1,11):
    mk_data_sanb11['ReturnsClosePrevRaw' + str(i)]  = mk_returnsPrev(df=mk_data_sanb11,open_close='close',window=i)
    mk_data_sanb11['ReturnsOpenPrevRaw'  + str(i)]  = mk_returnsPrev(df=mk_data_sanb11,open_close='open',window=i)
    mk_data_sanb11['ReturnsCloseNextRaw' + str(i)]  = mk_returnsNext(df=mk_data_sanb11,open_close='close',window=i)
    mk_data_sanb11['ReturnsOpenNextRaw'  + str(i)]  = mk_returnsNext(df=mk_data_sanb11,open_close='open',window=i)
    
for i in range(1,11):
    mk_data_itub4['ReturnsClosePrevRaw' + str(i)]  = mk_returnsPrev(df=mk_data_itub4,open_close='close',window=i)
    mk_data_itub4['ReturnsOpenPrevRaw'  + str(i)]  = mk_returnsPrev(df=mk_data_itub4,open_close='open',window=i)
    mk_data_itub4['ReturnsCloseNextRaw' + str(i)]  = mk_returnsNext(df=mk_data_itub4,open_close='close',window=i)
    mk_data_itub4['ReturnsOpenNextRaw'  + str(i)]  = mk_returnsNext(df=mk_data_itub4,open_close='open',window=i)


for i in range(1,11):
    mk_data_bbdc3['ReturnsClosePrevRaw' + str(i)]  = mk_returnsPrev(df=mk_data_bbdc3,open_close='close',window=i)
    mk_data_bbdc3['ReturnsOpenPrevRaw'  + str(i)]  = mk_returnsPrev(df=mk_data_bbdc3,open_close='open',window=i)
    mk_data_bbdc3['ReturnsCloseNextRaw' + str(i)]  = mk_returnsNext(df=mk_data_bbdc3,open_close='close',window=i)
    mk_data_bbdc3['ReturnsOpenNextRaw'  + str(i)]  = mk_returnsNext(df=mk_data_bbdc3,open_close='open',window=i)


for i in range(1,11):
    mk_data_bvsp['ReturnsClosePrevRaw' + str(i)]  = mk_returnsPrev(df=mk_data_bvsp,open_close='close',window=i)
    mk_data_bvsp['ReturnsOpenPrevRaw'  + str(i)]  = mk_returnsPrev(df=mk_data_bvsp,open_close='open',window=i)
    mk_data_bvsp['ReturnsCloseNextRaw' + str(i)]  = mk_returnsNext(df=mk_data_bvsp,open_close='close',window=i)
    mk_data_bvsp['ReturnsOpenNextRaw'  + str(i)]  = mk_returnsNext(df=mk_data_bvsp,open_close='open',window=i)


mk_data_sanb11.set_index('date',inplace=True)
mk_data_itub4.set_index('date',inplace=True)
mk_data_bbdc3.set_index('date',inplace=True)
mk_data_bvsp.set_index('date',inplace=True)

mk_data_sanb11 = mk_data_sanb11.add_prefix('sanb11_')
mk_data_itub4 = mk_data_bvsp.add_prefix('itub4_')
mk_data_bbdc3 = mk_data_bvsp.add_prefix('bbdc3_')
mk_data_bvsp = mk_data_bvsp.add_prefix('bvsp_')

mk_data_sanb11 = mk_data_sanb11.merge(mk_data_bvsp,how='left',left_index=True,right_index=True)

for i in range(1,11):
    mk_data_sanb11['sanb_11_ReturnsClosePrevMkt' + str(i)]  = mk_data_sanb11['sanb11_ReturnsClosePrevRaw' + str(i)] / mk_data_sanb11['bvsp_ReturnsClosePrevRaw' + str(i)]
    mk_data_sanb11['sanb_11_ReturnsOpenPrevMkt'  + str(i)]  = mk_data_sanb11['sanb11_ReturnsOpenPrevRaw' + str(i)] / mk_data_sanb11['bvsp_ReturnsOpenPrevRaw' + str(i)]
    mk_data_sanb11['sanb_11_ReturnsCloseNextMkt' + str(i)]  = mk_data_sanb11['sanb11_ReturnsCloseNextRaw' + str(i)] / mk_data_sanb11['bvsp_ReturnsCloseNextRaw' + str(i)]
    mk_data_sanb11['sanb_11_ReturnsOpenNextMkt'  + str(i)]  = mk_data_sanb11['sanb11_ReturnsOpenNextRaw' + str(i)] / mk_data_sanb11['bvsp_ReturnsOpenNextRaw' + str(i)]

mk_data_sanb11 = mk_data_sanb11.merge(mk_data_itub4,how='left',left_index=True,right_index=True)
mk_data_sanb11 = mk_data_sanb11.merge(mk_data_bbdc3,how='left',left_index=True,right_index=True)


mk_data_sanb11.to_csv('../../data/processed/mkt_data.csv')