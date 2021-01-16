import pandas as pd
import sqlite3 as sql

def connect_to_db(path):
    return sql.connect(path)

#df2 = pd.read_sql('select * from ext_Transactions',con=conn)
#print(df2.head())
#df = pd.read_csv('export.csv',delimiter=';', header=None, names=['Date','Date1','Post','Value','BALANCE'])
#df.drop(columns=['Date1'],inplace=True)
#df.Value = df.Value.str.replace('.','').str.replace(',','.').astype('float64')
#df.BALANCE = df.BALANCE.str.replace('.','').str.replace(',','.').astype('float64')
#df['USER'] = 1
#df['ACCOUNT'] = 1
#df.rename(columns={'Acc_Value:B',})
def insert_transactions(conn, df):
    df.to_sql('ext_Transactions',con=conn,if_exists='append',index=False)

def get_transactions(conn):
    df = pd.read_sql('select * from ext_Transactions',con=conn)
    return df