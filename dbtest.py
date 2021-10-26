import pymysql
from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy

# 2.创建Flask对象app并初始化
dbtestapp = Flask(__name__)  # __name__的作用是为了确认资源所在的路径
dbtestapp.secret_key = 'xiejunan'

conn = pymysql.connect(host="localhost", user="root", password="2012shijiemori", database="film", charset="utf8")

cursor = conn.cursor()

dbtestapp = Flask(__name__)


@dbtestapp.route('/login', methods=['GET', 'POST'])
def show():
    if request.method == 'GET':
        # 插入操作

        sql_insert_film = """insert into film.film(imdb, film_name_ch, film_name_en) values(2,'爱乐之城','La La Land')"""
        sql_insert_Cast = """insert into film.Cast(person_id, imdb, cast_type, person_name) values(3, 2, 'actress',
        'Emma Stone')"""
        try:
            cursor.execute(sql_insert_film)
            cursor.execute(sql_insert_Cast)
            #     提交
            conn.commit()
        except Exception as e:
            conn.rollback()


        # 查询操作
        sql = "SELECT * FROM user"
        try:
            cursor.execute(sql)

            results = cursor.fetchall()
            for row in results:
                # person_name = row[3]
                # cast_type = row[2]
                # print("Big boy is %s, %s." % (person_name, cast_type))
                return '<h>你就是%s！</h>' % (row[0])
        except:
            print("Error!")
    cursor.close()
    conn.close()


if __name__ == '__main__':
    dbtestapp.run()



    # 更新操作
    # sql_update_film = "update film.Cast set person_name = '%s' where person_id = %d"
    # sql_update_film2= "update film.Cast set cast_type = '%s' where person_id = %d "
    #
    # try:
    #     cursor.execute(sql_update_film % ("Nobody", 2))
    #     cursor.execute(sql_update_film2 % ("actor", 2))
    #     conn.commit()
    # except Exception as e:
    #     conn.rollback()

    # 删除操作
    # sql_delete= "delete from film.Cast where person_id = %d"
    #
    # try:
    #     cursor.execute(sql_delete % (2))
    #     conn.commit()
    # except Exception as e:
#     conn.rollback()
