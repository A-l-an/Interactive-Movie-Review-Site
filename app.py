import pymysql
from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy

# 2.创建Flask对象app并初始化
import logic

app = Flask(__name__)  # __name__的作用是为了确认资源所在的路径
app.secret_key = 'xiejunan'

conn = pymysql.connect(host="localhost", user="root", password="2012shijiemori", database="film", charset="utf8")

cursor = conn.cursor()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def show():
    show_data = logic.get_show()
    return show_data


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_data = logic.get_login()
    return login_data


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_name = request.form['username']
        user_password = request.form['password']
        if len(user_name) == 0 | len(user_password) == 0:
            return render_template('register.html')
        insert_user(user_name, user_password)

    return render_template("register.html")

    # 查询操作
    # sql = "SELECT * FROM Cast"
    # try:
    #     cursor.execute(sql)
    #
    #     results = cursor.fetchall()
    #
    #     for row in results:
    #         person_name = row[3]
    #         cast_type = row[2]
    #         # print("Big boy is %s, %s." % (person_name, cast_type))
    #         return render_template("index.html", person_name=person_name)
    # except:
    #     print("Error!")
    # cursor.close()


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

if __name__ == '__main__':
    app.run(debug=True)
