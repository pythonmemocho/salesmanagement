from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
import sqlite3

#データベース名を設定
DATABASE = 'database.db'

#データベース作成用の関数
def create_table(table):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    if table == 'menu':
        cur.execute('''
            create table if not exists menutable(
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

#データベースを作成
create_table('menu')
create_table('sales')

#Flaskの初期化
app = Flask(__name__)

def data_fetch(database,table):
    con = sqlite3.connect(database)
    cur = con.cursor()
    if table == 'menutable':
        db = cur.execute('select * from menutable').fetchall()
    elif table == 'salestable':
        db = cur.execute('select * from salestable order by date').fetchall()
    cur.close()
    con.close()
    return db

def sumEachItem(database):
    con = sqlite3.connect(database)
    cur = con.cursor()
    db = cur.execute('''select menutable.name, sum(price*salesCount) as sum 
                    from menutable inner join salestable 
                    on menutable.name = salestable.name 
                    group by menutable.name;''').fetchall()
    cur.close()
    con.close()
    return db

def sumDaily(database):
    con = sqlite3.connect(database)
    cur = con.cursor()
    db = cur.execute('''select date,sum(price*salesCount) as sum 
                    from menutable inner join salestable 
                    on menutable.name=salestable.name 
                    group by date''').fetchall()
    cur.close()
    con.close()
    return db

def sumMonthly(database):
    con = sqlite3.connect(database)
    cur = con.cursor()
    db = cur.execute('''select substr(date, 6 ,2) as month,sum(price*salesCount) as sum 
                    from menutable inner join salestable 
                    on menutable.name=salestable.name 
                    group by month''').fetchall()
    cur.close()
    con.close()
    return db


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/menu", methods=["GET","POST"])
def menu():
    database = data_fetch(DATABASE,'menutable')
    db = ({'id':data[0],'name':data[1],'price':data[2]} for data in database)
    return render_template("menu.html", db=db)

@app.route("/sales", methods=["GET","POST"])
def sales():
    menu = data_fetch(DATABASE,'menutable')
    sales = data_fetch(DATABASE,'salestable')
    join = sumEachItem(DATABASE)
    date_join = sumDaily(DATABASE)
    month_join = sumMonthly(DATABASE)
    
    menudb = [{'id':data[0],'name':data[1],'price':data[2]} for data in menu]
    salesdb = [{'id':data[0],'date':data[1],'name':data[2],'count':data[3]} for data in sales]
    joindb = [{'name':data[0],'sum':data[1]} for data in join]
    date_joindb = [{'date':data[0],'sum':data[1]} for data in date_join]
    monthlysum_db = [{'date':data[0],'sum':data[1]} for data in month_join]
    return render_template("sales.html", 
                           menu_db=menudb, 
                           sales_db=salesdb,
                           join_db=joindb,
                           date_join_db=date_joindb,
                           monthlysum_db=monthlysum_db)

@app.route('/register/<string:key>', methods=['POST'])
def register(key):
    if key == 'sales':
        date = request.form['date']
        name = request.form['name']
        count = request.form['count']
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute('insert into salestable(date, name, salesCount) values (?,?,?)',[date,name,count])
    elif key == 'menu':
        name = request.form['name']
        price = request.form['price']
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute('insert into menutable(name, price) values (?,?)',[name,price])
    con.commit()
    cur.close()
    con.close()
    return redirect(url_for(key))

@app.route('/delete/<string:key>', methods=['POST'])
def delete(key):
    delete_id = request.form["id"]
    if key == 'sales':
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute('delete from salestable where id=?',[delete_id])
    elif key == 'menu':
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute('delete from menutable where id=?',[delete_id])
    con.commit()
    cur.close()
    con.close()
    return redirect(url_for(key))


if __name__ == "__main__":
    app.run(debug=True)

