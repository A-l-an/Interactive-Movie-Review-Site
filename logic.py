# 逻辑处理单元 #

from flask import Flask, render_template, request, url_for
import pymysql

conn = pymysql.connect(host="localhost", user="root", password="2012shijiemori", database="film", charset="utf8")

cursor = conn.cursor()


def index_ori():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # 中文查找是什么电影
        film_name = request.form['search_film']
        sql_film_name = 'select * from film.film where film_name_ch' + '=' + '%s'
        cursor.execute(sql_film_name, [film_name])

        film_infos = cursor.fetchall()

        for film_info in film_infos:
            film_imdb = film_info[0]
            film_name_ch = film_info[1]
            film_name_en = film_info[2]

        if film_imdb:
            # return url_for('film', imdb=film_imdb)
            return render_template('film.html', film_imdb=film_imdb, film_name_en=film_name_en)
    return render_template('index.html')

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
                sql_pw = 'select user_password from film.user where user_name' + '=' + '%s'
                cursor.execute(sql_pw, (user[0]))

                pw = cursor.fetchall()

                if request.form['password'] == pw[0][0]:
                    # if request.form['password'] == pw:
                    return render_template('index.html', user_name=username)

                return '<h>账号密码错误！</h>'
        cursor.close()
        conn.close()


def get_register():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_name = request.form['username']
        user_password = request.form['password']
        if len(user_name) == 0 | len(user_password) == 0:
            return render_template('register.html')
        insert_user(user_name, user_password)

    return render_template("register.html")

def get_film(imdb):
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # 中文查找是什么电影
        film_name = request.form['search_film']
        sql_film_name = 'select * from film.film where film_name_ch' + '=' + '%s'
        cursor.execute(sql_film_name, [film_name])

        film_infos = cursor.fetchall()

        for film_info in film_infos:
            film_imdb = film_info[0]
            film_name_ch = film_info[1]
            film_name_en = film_info[2]

        if film_imdb:
            # return url_for('film', imdb=film_imdb)
            return render_template('film.html', film_imdb=film_imdb, film_name_en=film_name_en)

# 插入操作
def insert_user(user_name, user_password):
    sql_insert_user = 'insert into film.user values(' + '%s' + ', %s' + ')'
    try:
        cursor.execute(sql_insert_user, [user_name, user_password])
        #     提交
        conn.commit()
    except Exception as e:
        conn.rollback()

    cursor.close()
