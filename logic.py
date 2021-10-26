from flask import Flask, render_template, request
import pymysql

conn = pymysql.connect(host="localhost", user="root", password="2012shijiemori", database="film", charset="utf8")

cursor = conn.cursor()

def get_show():
    return render_template('register.html')

def get_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        if len(username) == 0 | len(password) == 0:
            return render_template('login.html')

        cursor.execute('select user_name from film.user')
        usernames = cursor.fetchall()

        for user in usernames:
            if request.form['username'] == user[0]:
                sql_pw = 'select user_password from film.user where user_name'+'='+'%s'
                cursor.execute(sql_pw, (user[0]))

                pw = cursor.fetchall()

                # if request.form['password'] == pw[0][0]:
                if request.form['password'] == pw:
                    return '<h>欢迎回来，%s!</h>' % user[0]

                return '<h>账号密码错误！</h>'
        cursor.close()
        conn.close()
