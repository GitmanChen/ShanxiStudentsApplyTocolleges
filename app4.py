import requests
from flask import Flask, render_template,  request, make_response, jsonify,redirect
import json
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
@app.route('/')
def indexlogin():
    return render_template('indexlogin.html')
@app.route('/index')   
def index():
    return render_template('index.html')

@app.route('/sub', methods=['GET','POST'])
def login():
    user = request.form.get('username')  # Use request.form
    mobile = request.form.get('phone')     
    #1.连接MySQL
    mydb = mysql.connector.connect(host="localhost", user="root", password="123065", database="userlist")
    cursor = mydb.cursor()
    #2.发送指令
    sql= "insert into usersmessages(name,numbers) values(%s,%s)"
    cursor.execute(sql, [user,mobile])
    mydb.commit()
    #3.关闭
    cursor.close()
    mydb.close()
    return redirect('/index')
def get_conn(db_name):
    conn = mysql.connector.connect(user='root', password='123065', host='localhost', database=db_name)
    return conn
conn1 = get_conn('2022scorerank')
cursor1 = conn1.cursor()
conn2 = get_conn('2022scoreline')
cursor2 = conn2.cursor()
@app.route('/way', methods=['GET','POST'])

def submit_form():
    if request.method == 'GET':
        rank = request.args.get('rank')
        subject = request.args.get('subject')
    elif    request.method == 'POST':
        data=request.get_json()
        rank=data.get('rank')
        subject=data.get('subject')
        print(rank)
        print(subject)
    def get_colleges(rank,subject):
        rank =float(rank)
        
        
        if subject == 'arts':
            db_name = 'arts'
        elif subject=='science':
            db_name = 'sciences'
        
        rank_equal="SELECT 分数 AS num2 FROM 2022scorerank.%s WHERE 累计人数 = CAST(%s AS SIGNED) ORDER BY 累计人数 ASC   LIMIT 1"
        rank_exceeds="SELECT 分数 AS num2 FROM 2022scorerank.%s WHERE 累计人数 > CAST(%s AS SIGNED) "
        miniscore = "SELECT 院校名称 FROM 2022scoreline.%s WHERE 最低分 BETWEEN %s - 11 AND %s + 2"
        cursor1.execute(rank_equal % (db_name, rank,))
        result=cursor1.fetchone()

        if result:
            print(result)
        else:
            cursor1.execute(rank_exceeds %(db_name, rank,))
            results=cursor1.fetchall()
            result=list(results)[0]
        result=float(result[0])
        print(result)

        cursor2.execute(miniscore %(db_name, result, result))
        results = cursor2.fetchall()
        results = list(results)
        return results
        
    results=get_colleges(rank, subject)
    json_colleges =[]
    for college in results:
        json_colleges.append({
            'name':college
        })
    response = jsonify(json_colleges)     
    if request.method == 'GET':
        response = make_response(response)
        response.headers['Content-Type'] = 'application/json'
        return response
    elif    request.method == 'POST':
        return response

if __name__== '__main__':
    app.run(debug=True)

