# 接口逻辑单元 #


from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy

import logic

# 创建Flask对象app并初始化
app = Flask(__name__)  # __name__的作用是为了确认资源所在的路径
app.secret_key = 'xiejunan'


@app.route('/', methods=['GET', 'POST'])
def index():
    show_data = logic.index_ori()
    return show_data


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_data = logic.get_login()
    return login_data


@app.route("/register", methods=["GET", "POST"])
def register():
    register_data = logic.get_register()
    return register_data


@app.route("/films", methods=["GET", "POST"])
def film():
    film_data = logic.get_film()
    return film_data


@app.route("/comment/new", methods=["GET", "POST"])
def comment():
    comment_data = logic.get_comment()
    return comment_data


@app.route("/comment/asdakbdjaksssknd", methods=["GET", "POST"])
def comments():
    comments_data = logic.get_comments()
    return comments_data


@app.route("/comment/asdakbdjaksssknd", methods=["GET", "POST"])
def likes():
    likes_data = logic.get_likes()
    return likes_data

@app.route("/user", methods=["GET", "POST"])
def user():
    user_data = logic.get_user()
    return user_data

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
