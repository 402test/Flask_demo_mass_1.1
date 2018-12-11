from flask import Flask, render_template, request, redirect, make_response, session
import pymysql
from random_active_code import get_active_code
from send_email import Mail
# 使用 pymysql代替 MySQLdb
pymysql.install_as_MySQLdb()
from flask_sqlalchemy import SQLAlchemy
from get_verify_code import get_verify_code #  验证码
from io import BytesIO
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost:3306/hcw_xidu_demo_one'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True  #  自动提交
app.config['SECRET_KEY']='suisuibianbian'#  session  key
db = SQLAlchemy(app)
class User(db.Model):
    '''
    用户表
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String)
    password = db.Column(db.String)
    age = db.Column(db.Integer)
    sex = db.Column(db.Integer)
    email = db.Column(db.Integer)
    active = db.Column(db.Integer)
    active_code = db.Column(db.String)

    def __init__(self,user_id,name,password,age,sex,email,active_code):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.age = age
        self.sex = sex
        self.email = email
        self.active='0'
        self.active_code = active_code

    def __repr__(self):
        return 'User %s,%s,%s,%s,%s,%s,%s'%(self.user_id,self.name,self.password,self.age\
                                            ,self.sex,self.email,self.active)


@app.route('/')
def index_view():
    # 首页
    return render_template('index.html')


@app.route('/login')
def login_views():
    return render_template('login.html')

#   邮箱激活  访问链接之后  在数据库里面  把active 改成 1
@app.route('/vetify/<active_code>')
def vetify_email(active_code):
    updata_active  = User.query.filter(User.active_code==active_code).first()
    updata_active.active = 1
    db.session.add(updata_active)
    return 'ok'

@app.route('/register',methods=['GET','POST'])
def register_views():
    if request.method =='GET':
        return render_template('register.html')
    else:
        # 接受注册页面传递的参数
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        sex = request.form.get('sex')
        age = request.form.get('age')
        #  先验证验证码是否正确
        if request.form.get('img') != session.get('img'):
            print(request.form.get('img'))
            print(session.get('img'))
            del session['img']
            return render_template('register.html', img_error='验证码错误')
        print('验证成功')
        #  再发送邮件
        active_code = get_active_code()#  生成随机链接
        send_email_state = Mail(email,'127.0.0.1/vetify/%s'%active_code)
        send_email_state.send()
        print(locals())

        #  存库
        #          获取最后一位用户的user_id
        u_id = db.session.query(User).order_by('id DESC').limit(1)
        user_id = u_id.first().user_id+1

        #  插入

        user = User(user_id,name,password,age,sex,email,active_code)
        db.session.add(user)


        return render_template('register.html',msg='邮件已发送到你的邮箱,请验证')


@app.route('/code')
def code_views():
    img,code = get_verify_code()
    buf = BytesIO()
    img.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpg'
    session['img'] = code
    return response

if __name__ =='__main__':
    app.run(debug=True)

#print(User.query.filter_by().all())
