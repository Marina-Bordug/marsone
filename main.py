import secrets
from data import db_session
from flask import Flask, render_template, redirect
from data.users import User
from data.jobs import Jobs
from forms.user import RegisterForm

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(16)
db_session.global_init("db/users.db")


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template("index.html", news=jobs)


@app.route("/login")
def login():
    return "qwe"


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == "__main__":
    user = User()
    user.surname = "Kelly"
    user.name = "Green"
    user.age = 23
    user.position = "astronaut"
    user.speciality = "research engineer"
    user.address = "module_3"
    user.email = "kelly_astronaut@mars.org"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    # user.name = "Пользователь 3"
    # user.about = "биография пользователя 3"
    # user.email = "email3@email.ru"
    # db_sess = db_session.create_session()
    # user = db_sess.query(User).filter(User.id == 2).first()
    # news = News(title="Вторая новость", content="Привет второй блог!",
    #             user=user, is_private=False)
    # for n in user.news:
    #     print(n.title)
    # db_sess.add(news)
    # db_sess.commit()
    # user = db_sess.query(User).first()
    # user.name = "qwe"
    # db_sess.delete(user)
    # db_sess.add(user)
    # db_sess.commit()
    app.run(host="127.0.0.1", port=8080)
