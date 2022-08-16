import sqlite3

def create_table(database,table):
    con = sqlite3.connect(database)
    cur = con.cursor()
    if table == 'items':
        cur.execute('''
            create table if not exists itemstable(
                id integer primary key autoincrement,
                name text, 
                price integer
                )''')
    elif table == 'sales':
        cur.execute('''
            create table if not exists salestable(
                id integer primary key autoincrement,
                date text,
                name text, 
                salesCount integer
                )''')
    cur.close()
    con.close()

def data_fetch(database,table):
    con = sqlite3.connect(database)
    cur = con.cursor()
    if table == 'itemstable':
        db = cur.execute('select * from itemstable').fetchall()
    elif table == 'salestable':
        db = cur.execute('select * from salestable order by date').fetchall()
    cur.close()
    con.close()
    return db

def sum_each_item(database):
    con = sqlite3.connect(database)
    cur = con.cursor()
    db = cur.execute('''select itemstable.name, sum(price*salesCount) as sum 
                    from itemstable inner join salestable 
                    on itemstable.name = salestable.name 
                    group by itemstable.name;''').fetchall()
    cur.close()
    con.close()
    return db

def sum_daily(database):
    con = sqlite3.connect(database)
    cur = con.cursor()
    db = cur.execute('''select date,sum(price*salesCount) as sum 
                    from itemstable inner join salestable 
                    on itemstable.name=salestable.name 
                    group by date''').fetchall()
    cur.close()
    con.close()
    return db

def sum_monthly(database):
    con = sqlite3.connect(database)
    cur = con.cursor()
    db = cur.execute('''select substr(date, 6 ,2) as month,sum(price*salesCount) as sum 
                    from itemstable inner join salestable 
                    on itemstable.name=salestable.name 
                    group by month''').fetchall()
    cur.close()
    con.close()
    return db