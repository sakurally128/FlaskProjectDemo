from flask import Flask,render_template,request,redirect,url_for,session
from decorators import login_required
from models import User,Question
from exts import db
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'questions':Question.query.order_by(db.desc(Question.create_time)).all()
    }
    return render_template("index.html",**context)


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        telephone = request.form.get("telephone")
        password = request.form.get("password")

        user = User.query.filter(User.telephone == telephone,User.password == password).first()
        if user:
            session["user_id"] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u"手机号或密码错误，请查证后从新输入！"

@app.route('/logout')
def logout():
    session.pop("user_id")
    return redirect(url_for('login'))



@app.route('/regist/',methods=["GET","POST"])
def regist():
    if request.method == "GET":
        return render_template("regist.html")
    else:
        telephone = request.form.get("telephone")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u"该手机号码已被注册，请更换手机号码"
        else:
            #判断密码与重复密码是否相等
            if password1 != password2:
                return u"两次密码不相等，请核对后再填写"
            else:
                user = User(telephone = telephone,username = username,password=password1)
                db.session.add(user)
                db.session.commit()
                #注册成功，跳转到登陆界面
                return redirect(url_for('login'))

@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get("title")
        content = request.form.get("content")
        question = Question(title = title,content = content)
        user_id = session.get("user_id")
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("index"))
    
@app.route('/add_answer')
def add_answer():
    content = request.form.get("answer_content")


@app.route('/detail/<question_id>')
def detail(question_id):
    context = {
        'question': Question.query.filter(Question.id == question_id).first()
    }
    return render_template("detail.html",**context)

@app.context_processor
def my_context_processor():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {"user":user}
    return {}
if __name__ == '__main__':
    app.run()
