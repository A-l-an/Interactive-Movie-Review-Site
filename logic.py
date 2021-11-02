# 逻辑处理单元 #

from flask import Flask, render_template, request, url_for, session, redirect
import pymysql

conn = pymysql.connect(host="localhost", user="root", password="2012shijiemori", database="film", charset="utf8")

cursor = conn.cursor()


def index_ori():
    if request.method == 'GET':
        user_name = session.get('username')
        return render_template('index.html', user_name=user_name)
    else:
        session['filmname'] = request.form['search_film']
        # return get_film()
        return redirect('/films')


def get_login():
    if request.method == 'GET':
        user_name = session.get('username')
        return render_template('login.html', user_name=user_name)
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
                    session['username'] = user_name
                    # return render_template('index.html', user_name=user_name)
                    return redirect('/')
                    # return url_for('index')
                return '<h>账号密码错误！</h>'


def get_register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        user_name = request.form['username']
        user_password = request.form['password']
        if len(user_name) == 0 | len(user_password) == 0:
            return render_template('register.html')
        insert_user(user_name, user_password)
        return redirect('/login')


def get_film():
    # film_name_ch = request.form['search_film']
    film_name_ch = session.get('filmname')
    # 取电影信息 #
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
    # 取每列中的元素
    cast_types = [film_cast[2] for film_cast in film_casts]
    person_names = [film_cast[3] for film_cast in film_casts]

    # 取精选评论 #
    sql_film_comment_good = 'select * from film.comment where imdb' + '=' + '%s'
    cursor.execute(sql_film_comment_good, [film_imdb])

    film_comment_info = cursor.fetchone()
    author = film_comment_info[2]
    comment_content = film_comment_info[3]
    film_time = film_comment_info[4]
    comment_like = film_comment_info[5]

    session['film_imdb_now'] = film_imdb
    user_name = session.get('username')
    if film_imdb:
        # get_cast(film_imdb)
        return render_template('film.html', film_imdb=film_imdb, film_name_en=film_name_en, description=description,
                               cast_types=cast_types, person_names=person_names, user_name=user_name,
                               author=author, comment_content=comment_content, film_time=film_time,
                               comment_like=comment_like)


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
        # 所有评论
        sql_film_com_all = 'select * from film.comment where imdb' + '=' + '%s'
        imdb = session.get('film_imdb_now')
        cursor.execute(sql_film_com_all, [imdb])
        film_comments = cursor.fetchall()  # 这是字典

        user_name = session.get('username')
        return render_template('comments.html', user_name=user_name, film_comments=film_comments)
    else:
        comment_id = request.form['Comment_ID']
        imdb = session.get('film_imdb_now')
        user_name = session.get('username')
        comment_content = request.form['Comment']
        film_time = request.form['Time']
        # 插入数据
        sql_insert_comment = 'insert into film.comment values(' + '%s' + ', %s' + ', %s' + ', %s' + ', %s' + ', %s' + ', %s' ')'
        try:
            cursor.execute(sql_insert_comment, [comment_id, imdb, user_name, comment_content, film_time,
                                                '0', '2021-11-01 22:06:08'])
            # 提交
            conn.commit()
        except Exception as e:
            conn.rollback()

        # 所有评论
        sql_film_com_all = 'select * from film.comment where imdb' + '=' + '%s'
        cursor.execute(sql_film_com_all, [imdb])
        film_comments = cursor.fetchall()  # 这是字典

    return render_template("comments.html", comment_id=comment_id, imdb=imdb, user_name=user_name,
                           comment_content=comment_content, film_time=film_time,
                           film_comments=film_comments)


def get_delete():
    if request.method == 'GET':
        user_name = session.get('username')
        return render_template('delete.html', user_name=user_name)
    else:
        delete_comment_ID = request.form['Comment_ID']
        #     判断是不是该评论本用户/管理员
        sql_select_username = 'select user_name from film.comment where comment_id = ' + '%s'
        cursor.execute(sql_select_username, delete_comment_ID)
        author_name = cursor.fetchall()
        my_name = session.get('username')
        if (my_name == author_name[0][0]) | (my_name == 'sudo'):
            # 删除操作
            sql_delete = "delete from film.comment where comment_id = %s"

            try:
                cursor.execute(sql_delete, delete_comment_ID)
                conn.commit()
                return redirect('/comment/asdakbdjaksssknd')
            except Exception as e:
                conn.rollback()
                return '<h>不可操作！</h>'
        else:
            return '<h>不可操作！</h>'


def get_update():
    if request.method == 'GET':
        user_name = session.get('username')
        return render_template('update.html', user_name=user_name)
    else:
        comment_content_new = request.form['Comment']
        update_comment_ID = request.form['Comment_ID']
        #     判断是不是该评论本用户/管理员
        sql_select_username = 'select user_name from film.comment where comment_id = ' + '%s'
        cursor.execute(sql_select_username, update_comment_ID)
        author_name = cursor.fetchall()
        my_name = session.get('username')
        if (my_name == author_name[0][0]) | (my_name == 'sudo'):
            # 更新操作
            sql_update = "update film.comment set comment_content = %s where comment_id = %s"

            try:
                cursor.execute(sql_update, [comment_content_new, update_comment_ID])
                conn.commit()
                return redirect('/comment/asdakbdjaksssknd')
            except Exception as e:
                conn.rollback()
                return '<h>不可操作！</h>'
        else:
            return '<h>不可操作！</h>'


# 更新点赞的数据
def get_likes():
    if request.method == 'GET':
        user_name = session.get('username')
        return render_template('likes.html', user_name=user_name)
    else:
        update_comment_ID = request.form['Comment_ID']
        sql_select_username = 'select * from film.comment where comment_id = ' + '%s'
        cursor.execute(sql_select_username, update_comment_ID)
        comment_infos = cursor.fetchall()
        my_name = session.get('username')

        for comment_info in comment_infos:
            author_name = comment_info[2]
            comment_like_old = comment_info[5]
            comment_like_new = comment_like_old + 1

        # 更新操作
        sql_update = "update film.comment set comment_like = %s where comment_id = %s"

        try:
            cursor.execute(sql_update, [comment_like_new, update_comment_ID])
            conn.commit()
            return redirect('/comment/asdakbdjaksssknd')
        except Exception as e:
            conn.rollback()
            return '<h>不可操作！</h>'


def get_filmfest():
    # 还没改（和数据库有关）
    # film_name_ch = request.form['search_film']
    # sql_film_name = 'select * from film.film where film_name_ch' + '=' + '%s'
    # cursor.execute(sql_film_name, [film_name_ch])
    #
    # film_infos = cursor.fetchall()
    #
    # for film_info in film_infos:
    #     film_imdb = film_info[0]
    #     film_name_ch = film_info[1]
    #     film_name_en = film_info[2]
    #     description = film_info[3]
    #
    # sql_film_cast = 'select * from film.cast where imdb' + '=' + '%s'
    # cursor.execute(sql_film_cast, [film_imdb])
    # film_casts = cursor.fetchall()
    #
    # cast_types = [film_cast[2] for film_cast in film_casts]
    # person_names = [film_cast[3] for film_cast in film_casts]
    #
    # user_name = session.get('username')
    # if film_imdb:
    #     # get_cast(film_imdb)
    #     return render_template('film.html', film_imdb=film_imdb, film_name_en=film_name_en,
    #                            description=description, cast_types=cast_types, person_names=person_names,
    #                            user_name=user_name)
    return render_template('filmfest.html')


def show_user():
    if request.method == 'GET':
        user_name = session.get('username')
        person = request.a['film_comment[2]']
        # 取电影信息 #
        sql_person = 'select * from film.user where user_name' + '=' + '%s'
        cursor.execute(sql_person, [person])
        person_infos = cursor.fetchall()

        for person_info in person_infos:
            person_fans = person_info[0]

        return render_template('user.html', person_fans=person_fans, person=person)


def get_like():
    if request.method == 'GET':
        user_name = session.get('username')
        return render_template('follow.html', user_name=user_name)
    else:
        author = request.form['username']
        sql_select_fans = 'select * from film.user where user_name = ' + '%s'
        cursor.execute(sql_select_fans, author)
        user_infos = cursor.fetchall()
        my_name = session.get('username')

        for user_info in user_infos:
            fans_old = user_info[2]
            fans_new = fans_old + 1

        # 更新操作
        sql_update_fans = "update film.user set user_fans = %s where user_name = %s"

        try:
            cursor.execute(sql_update_fans, [fans_new, author])
            conn.commit()
            return redirect('/user')
        except Exception as e:
            conn.rollback()
            return '<h>不可操作！</h>'

    return '<h>账号密码错误！</h>'


# 插入操作
def insert_user(user_name, user_password):
    sql_insert_user = 'insert into film.user values(' + '%s' + ', %s' + ', %s' ')'
    try:
        cursor.execute(sql_insert_user, [user_name, user_password, '0'])
        # 提交
        conn.commit()
    except Exception as e:
        conn.rollback()
