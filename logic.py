# 逻辑处理单元 #

from flask import Flask, render_template, request, url_for
import pymysql

conn = pymysql.connect(host="localhost", user="root", password="2012shijiemori", database="film", charset="utf8")

cursor = conn.cursor()


def index_ori():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return get_film()


def get_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_name = request.form['user_name']
        password = request.form['password']
        if len(user_name) == 0 | len(password) == 0:
            return render_template('login.html')

        cursor.execute('select user_name from film.user')
        user_names = cursor.fetchall()

        for user in user_names:
            if request.form['user_name'] == user[0]:
                sql_pw = 'select user_password from film.user where user_name' + '=' + '%s'
                cursor.execute(sql_pw, (user[0]))

                pw = cursor.fetchall()

                if request.form['password'] == pw[0][0]:
                    # if request.form['password'] == pw:
                    # return render_template('index.html', user_name=user_name)
                    # return url_for('index')
                return '<h>账号密码错误！</h>'
        cursor.close()
        conn.close()


def get_register():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_name = request.form['user_name']
        user_password = request.form['password']
        if len(user_name) == 0 | len(user_password) == 0:
            return render_template('register.html')
        insert_user(user_name, user_password)

    return render_template("register.html")


def get_film():
    film_name_ch = request.form['search_film']
    sql_film_name = 'select * from film.film where film_name_ch' + '=' + '%s'
    cursor.execute(sql_film_name, [film_name_ch])

    film_infos = cursor.fetchall()

    for film_info in film_infos:
        film_imdb = film_info[0]
        film_name_ch = film_info[1]
        film_name_en = film_info[2]
        description = film_info[3]

    sql_film_cast = 'select * from film.cast where imdb' + '=' + '%s'
    cursor.execute(sql_film_cast, [film_imdb])
    film_casts = cursor.fetchall()

    # for film_cast in film_casts:
    #     cast_types = film_cast[2]
    #     person_names = film_cast[3]
    cast_types = [film_cast[2] for film_cast in film_casts]
    person_names = [film_cast[3] for film_cast in film_casts]

    if film_imdb:
        # get_cast(film_imdb)
        return render_template('film.html', film_imdb=film_imdb, film_name_en=film_name_en,
                               description=description, cast_types=cast_types, person_names=person_names)


def get_imdb(film_name_ch):
    sql_film_imdb = 'select imdb from film.film where film_name_ch' + '=' + '%s'
    cursor.execute(sql_film_imdb, [film_name_ch])
    film_imdb = cursor.fetchone()
    return film_imdb


def get_cast(film_imdb):
    # film_imdb = get_imdb(film_name_ch)

    sql_film_cast = 'select * from film.cast where imdb' + '=' + '%d'
    cursor.execute(sql_film_cast, film_imdb)
    film_casts = cursor.fetchall()

    for film_cast in film_casts:
        cast_type = film_cast[2]
        person_name = film_cast[3]

    if film_imdb:
        # return url_for('film', imdb=film_imdb)
        print(person_name)
        return render_template('film.html', person_name=person_name, cast_type=cast_type)


def get_comment():
    if request.method == 'GET':
        return render_template('comment_new.html')
    else:
        return render_template("comment_new.html")


def get_comments():
    if request.method == 'GET':

        return render_template('comments.html')
    else:
        comment_id=request.form['Comment_ID']
        imdb=request.form['IMDB']
        user_id=request.form['user']
        comment_content=request.form['Comment']
        comment_time=request.form['Time']

        # 插入数据
        sql_insert_comment = 'insert into film.comment values(' + '%s' + ', %s' + ', %s' + ', %s' + ', %s'')'
        try:
            cursor.execute(sql_insert_comment, [comment_id, imdb, user_id, comment_content, comment_time])
            # 提交
            conn.commit()
        except Exception as e:
            conn.rollback()
    return render_template("comments.html", comment_id=comment_id, imdb=imdb, user_id=user_id,
                           comment_content=comment_content, comment_time=comment_time)


def get_likes():
    # 更新点赞的数据
    sql_update_film = "update film.Cast set person_name = '%s' where person_id = %d"
    sql_update_film2= "update film.Cast set cast_type = '%s' where person_id = %d "

    try:
        cursor.execute(sql_update_film % ("Nobody", 2))
        cursor.execute(sql_update_film2 % ("actor", 2))
        conn.commit()
    except Exception as e:
        conn.rollback()

# 还没做完
def get_user():
    author=request.form['user_id']
    cursor.execute('select user_name from film.user')
    user_names = cursor.fetchall()

    for user in user_names:
        if request.form['user_name'] == user[0]:
            sql_pw = 'select user_password from film.user where user_name' + '=' + '%s'
            cursor.execute(sql_pw, (user[0]))

            pw = cursor.fetchall()

            if request.form['password'] == pw[0][0]:
                # if request.form['password'] == pw:
                return render_template('index.html', user_name=user_name)

            return '<h>账号密码错误！</h>'

# 插入操作
def insert_user(user_name, user_password):
    sql_insert_user = 'insert into film.user values(' + '%s' + ', %s' + ')'
    try:
        cursor.execute(sql_insert_user, [user_name, user_password])
        # 提交
        conn.commit()
    except Exception as e:
        conn.rollback()

    cursor.close()
