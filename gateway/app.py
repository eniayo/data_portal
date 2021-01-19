# Importing require libraries
from flask import Flask, render_template, flash, redirect, request, session, logging, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

#Now create flask application object
app = Flask(__name__)

#Database Configuration and Creating object of SQLAlchemy
app.config['SECRET_KEY'] = '!9m@S-dThyIlW[pHQbN^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:eniayo1998@localhost/portal'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'usertable'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    username = db.Column(db.String(15))
    email = db.Column(db.String(50))
    password = db.Column(db.String(256))


    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return "<User %r>" % self.username

@app.route('/')
def home():
    return render_template('index.html')

#User Registration Api End Point
@app.route('/register/', methods = ['GET', 'POST'])
def register():
    #Creating RegistrationForm class object
    form = RegisterForm(request.form)

    #Checking that method is post and form is valid or not
    if request.method == 'POST' and form.validate():
        #if all is fine, generate hashed password
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        #create new user model object
        new_user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password)
        db.session.add(new_user)
        db.sesssion.commit()
        flash('You have successfully registered', 'success')
        return redirect(url_for('login'))

    else:
        return render_template('register.html', form = form)

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    #Creating Login form object
    form = LoginForm(request.form)
    #verifying that method is post and form is valid 
    if request.method == 'POST' and form.validate:
        #checking that user is exist or not by email
        user = User.query.filter_by(email = form.email.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                flash('You have successfully logged in.', "success")
                session['logged_in'] = True
                session['email'] = user.email
                session['username'] = user.username
                return redirect(url_for('home'))
            else:
                # if password is in correct, redirect to login page
                flash('Username or Password  Incorrect', "Danger")

                return redirect(url_for('login'))
    return render_template('login.html', form = form)

@app.route('/logout/')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
