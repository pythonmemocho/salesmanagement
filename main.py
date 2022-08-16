from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
import sqlite3

from _sql import *

#データベース名を設定
DATABASE = 'database.db'

#データベースを作成
create_table(DATABASE,'items')
create_table(DATABASE,'sales')

#Flaskの初期化
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/itemsList", methods=["GET","POST"])
def items():
    database = data_fetch(DATABASE,'itemstable')
    db = ({'id':data[0],'name':data[1],'price':data[2]} for data in database)
    return render_template("itemsList.html", db=db)

@app.route("/sales", methods=["GET","POST"])
def sales():
    menu = data_fetch(DATABASE,'itemstable')
    sales = data_fetch(DATABASE,'salestable')
    join = sum_each_item(DATABASE)
    date_join = sum_daily(DATABASE)
    month_join = sum_monthly(DATABASE)
    
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
    elif key == 'items':
        name = request.form['name']
        price = request.form['price']
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute('insert into itemstable(name, price) values (?,?)',[name,price])
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
    elif key == 'items':
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute('delete from itemstable where id=?',[delete_id])
    con.commit()
    cur.close()
    con.close()
    return redirect(url_for(key))


if __name__ == "__main__":
    app.run(debug=True)

