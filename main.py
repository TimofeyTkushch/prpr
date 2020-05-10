from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_restful import abort

from data import db_session

from data.users import User
from data.news import News
from data.mmodels import MModels


from data.kub import Model
from data.kub import Dataset
from data.kub import FittingAndEvaluating
from data.kub import all_
from data.kub import numzn


from data.register import RegisterForm
from data.register import LoginForm

from data.news import NewsForm
from data.mmodels import MModelsForm

import os


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'our_secret_key'
model = ''
res = ''


db_session.global_init("db/neuroweb.sqlite")
    
@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)    

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form, message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/")
def index():
    session = db_session.create_session()
    if current_user.is_authenticated:
        news = session.query(News).filter((News.user == current_user) | (News.is_private != True))
    else:
        news = session.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)

@app.route("/makemodelpage",  methods=['GET', 'POST'])
def makemodelpage():
    global model
    global res
    form = MModelsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        model = MModels(
            name = form.name.data,
            p1 = form.p1.data,
            p2 = form.p2.data,
            p3 = form.p3.data,
            p4 = form.p4.data,
            p5 = form.p5.data,
            p6 = form.p6.data,
            )
        params=(
            model.name,
            model.p1,
            model.p2,
            model.p3,
            model.p4,
            model.p5,
            model.p6)
        res = all_(*params)
        res.pict()
        current_user.mmodels.append(model)
        session.merge(current_user)
        session.commit()
        return redirect('/risunok')
    return render_template("makemodelpage.html", form=form)
@app.route("/risunok",  methods=['GET', 'POST'])
def risunok():
    global res
    num = numzn()
    adres = f'img/pic{num}.png'
    print(adres)
    if res != '':
        return render_template('risunok.html', adres=adres)
    return 'Вы не создавали модель'
@app.route('/teach', methods=['GET', 'POST'])
def teach():
    global res
    if res != '':
        res.fitting()
        num = numzn()
        adres = f'img/pic{num}.png'
        return render_template('risunoktought.html', adres=adres)
    return 'Вы не создавали модель'
@app.route('/estimate', methods=['GET', 'POST'])
def estimate():
    global res
    if res != '':
        mark = res.evaluating()
        num = numzn()
        adres = f'img/pic{num}.png'
        return render_template('risunokwithmark.html', mark=mark, adres=adres)
    return 'Вы не создавали модель'

@app.route("/yourmodelsdata",  methods=['GET', 'POST'])
def yourmodelsdata():
    session = db_session.create_session()
    session.merge(current_user)
    data = session.query(MModels).filter((MModels.user == current_user))
    session.commit()
    return render_template("yourmodelsdata.html", model=data)

@app.route('/addnews',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('addnews.html', title='Добавление новости', 
                           form=form)    

@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id, 
                                          News.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id, 
                                          News.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addnews.html', title='Редактирование новости', form=form)    

@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    session = db_session.create_session()
    news = session.query(News).filter(News.id == id,
                                      News.user == current_user).first()
    if news:
        session.delete(news)
        session.commit()
    else:
        abort(404)
    return redirect('/')    
   

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
