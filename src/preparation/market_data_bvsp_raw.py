import pandas as pd #importing pandas

#defining columns name
cols_names = ['date','close','open','max','min','volume','returnsOpenPrev']
#reading csv file
df = pd.read_csv('market_data_bvsp.csv',names=cols_names,header=1)

#replacing commas for dots and casting as floats
cols_2_change = ['close','open','max','min','returnsOpenPrev','date']


#replacing commas for dots and casting as floats
cols_2_change = ['close','open','max','min','returnsOpenPrev','date']

for col_name in cols_2_change:
    if col_name == 'returnsOpenPrev':
        df[col_name] = df[col_name].apply(lambda x: x.replace('%',''))
    if col_name == 'date':
        df[col_name] = df[col_name].apply(lambda x: x.replace('.','/'))
    if (col_name == 'open'):
        df[col_name]= df[col_name].apply(lambda x: x.replace('.',''))
    if (col_name == 'close'):
        df[col_name]= df[col_name].apply(lambda x: x.replace('.',''))
    if (col_name == 'min') | (col_name == 'max'):
        df[col_name]= df[col_name].apply(lambda x: x.replace('.',''))
    df[col_name] = df[col_name].apply(lambda x: x.replace(',','.'))

for col_name in cols_2_change:
    if col_name == 'date':
        break
    df[col_name] = df[col_name].astype('float64')
    if col_name == 'returnsOpenPrev':
        df[col_name] = df[col_name]/100
df['volume'] = df['volume'].apply(lambda x: x.replace(',','.'))
df['volume'].replace('-',0,inplace=True)


#extracting operands 'K' and 'M' and converting values
df['volume'] = (df.volume.replace(r'[KM]+$', '', regex=True).astype(float) * df.volume.str.extract(r'[\d\.]+([KM]+)', expand=False) \
                .fillna(1) \
                .replace(['K','M'], [10**3, 10**6]).astype(int))

 #write to csv

df.to_csv('../../data/raw/market_data_bvsp_raw.csv')