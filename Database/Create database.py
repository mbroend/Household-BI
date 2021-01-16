import sqlite3
conn = sqlite3.connect('household.db')

print('Opened database succesfully')


conn.execute('''CREATE TABLE ext_Transactions
         (USER INT   NOT NULL,
         ACCOUNT INT     NOT NULL,
         DATE           Date     NULL,
         POST            text      NULL,
         VALUE         REAL,
         BALANCE         REAL
         );''')
print("Table created successfully")

conn.close()
