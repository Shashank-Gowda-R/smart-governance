from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
# import sqlite3
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from datetime import date, datetime



app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# dbs = sqlite3.connect("users.db")

# cursor = dbs.cursor()


#to be codded 
#login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Database Table Creation Section
# app.app_context().push()

#to create tables
#inside terminal
# from server import app, db
# app.app_context().push()
# db.create_all()

#Sign up table which contains data of user
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    phoneno = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    
# cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username varchar(250) NOT NULL UNIQUE, fname varchar(250), lname varchar(250), phoneno varchar(250), email varchar(250), password varchar(250))")
   
    # usernamess = db.relationship('userBalance', backref='user')

class remBal(UserMixin, db.Model):
    # __tablename__ = "users_balances"
    # username = db.Column(db.String(100), primary_key=True, db.ForeignKey('user.username'))
    username = db.Column(db.String(100), primary_key=True)
    balance = db.Column(db.Integer)

# cursor.execute("CREATE TABLE balances (username varchar(250) PRIMARY KEY, balance INTEGER)")

class clientTranscation(UserMixin, db.Model):
    # __tablename__ = "client_transcation"
    transcation_id = db.Column(db.String(100), primary_key=True)
    f_username = db.Column(db.String(100))
    t_username = db.Column(db.String(100))
    amount = db.Column(db.String(100))
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))


#other class section





@app.route("/login_or_sign_up", methods=["GET", "POST"])
def login_or_sign_up():

    #login
    global c_u
    if request.method == "POST":
        if request.form["submit"] == "log_in":


            l_username = request.form["l_username"]
            l_password = request.form["l_password"]
            print(l_username, l_password) 

            user = User.query.filter_by(username=l_username).first()
            if not user:
                flash("this username does not exist, Please Register")
                return redirect(url_for('login_or_sign_up'))
            elif not check_password_hash(user.password, l_password):
                flash("Password zincorrect, PLease Try Again")
                return redirect(url_for('login_or_sign_up'))
            else:

                login_user(user)
                return redirect(url_for('home'))
        
        #sign up
        if request.form["submit"] == "Sign_up":

            if User.query.filter_by(username=request.form.get('l_username')).first():
            #User already exists
                flash("You've already signed up with that username, log in instead!")
                return redirect(url_for('login'))


            s_username = request.form["s_username"]
            s_fname = request.form["s_fname"]
            s_lname = request.form["s_lname"]
            s_phoneno = request.form["s_phoneno"]
            s_email = request.form["s_email"]
            s_password = request.form["s_password"]
            print(s_username, s_fname, s_lname, s_phoneno, s_email, s_password)

            hash_and_salted_password = generate_password_hash(
                s_password,
                method='pbkdf2:sha256',
                salt_length=8
            )

            new_user = User(
                username = s_username,
                fname = s_fname,
                lname = s_lname,
                phoneno = s_phoneno,
                email = s_email,
                password = hash_and_salted_password
            )
            db.session.add(new_user)
            db.session.commit()

            # cursor.execute(f"INSERT INTO users VALUES({s_username}, {s_fname}, {s_lname}, {s_phoneno}, {s_email}, {hash_and_salted_password})")

            new_ub = remBal(
                username = s_username,
                balance = 1000
            )
            db.session.add(new_ub)
            db.session.commit()
            
            # cursor.execute(f"INSERT INTO balances VALUES({s_username}, 100)")
            login_user(new_user)
            return redirect(url_for("home"))

            #database of new user
            # modelName = s_username + "db"
            # class modelName(db.Model):
            #     transcation_id = db.Column(db.Integer, primary_key=True)
            #     transaction_amt = db.Column(db.Integer)
            #     remaning_amt = db.Column(db.Integer)
            # # db.create_all()
            # modelName.__table__.create(db.session.bind, checkfirst=True)

            print("new user data inserted into database")


    return render_template("loginorsignup.html", logged_in=current_user.is_authenticated)

@app.route("/")
def main():
    return redirect(url_for('login_or_sign_up'))


#home page or main landing page
@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    # print(current_user.username)
    cu_bal = remBal.query.filter_by(username=current_user.username).first()
    return render_template("home.html", username=current_user.username, bal = cu_bal.balance, logged_in=True)

#logout
@app.route('/logout')
def logout():
    logout_user()
    c_u = "null"
    return redirect(url_for('login_or_sign_up'))


#pay section

#username pay
@app.route("/pay/username", methods=["GET", "POST"])
@login_required
def pay_username():
    if request.method == 'POST':
        p_username = request.form["username"]
        p_amount = int(request.form["amount"])
        # remBal.query.filter_by(username=request.form.get('l_username')).first()
        # User.query.filter_by(username=l_username).first()
        fuser = remBal.query.filter_by(username=current_user.username).first()
        print(fuser.balance, p_username, p_amount)
        if fuser.balance < p_amount:
            flash("Insuffecient amount")
            return redirect(url_for('pay_username'))
        else:
            tuser = remBal.query.filter_by(username=p_username).first()
            if not tuser:
                flash("Username dosent exist")
                return redirect(url_for('pay_username'))
            else:
                #updating database
                tuser.balance += p_amount
                fuser.balance -= p_amount
                db.session.commit()
                flash(f"{p_amount} sucessfully sent to {p_username}")
                obj = clientTranscation.query.all()
                tno = int(obj[-1].transcation_id)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                f_username = fuser.username
                new_trans = clientTranscation(
                    transcation_id = tno + 1,
                    f_username = f_username,
                    t_username = p_username,
                    amount = p_amount,
                    date = date.today(),
                    time = current_time
                )
                db.session.add(new_trans)
                db.session.commit()




    return render_template("pay_username.html", username=current_user.username, logged_in=True)

#qr pay
@app.route("/pay/qr", methods=["GET", "POST"])
@login_required
def pay_qr():
    return render_template("pay_qr.html")

#phone no pay
@app.route("/pay/phoneno", methods=["GET", "POST"])
@login_required
def pay_phoneno():
    if request.method == 'POST':
        p_phonenumber = request.form["pno"]
        p_amount = int(request.form["amount"])
        # remBal.query.filter_by(username=request.form.get('l_username')).first()
        # fu = User.query.filter_by(phoneno=p_phonenumber).first()
        fuser = remBal.query.filter_by(username=current_user.username).first()
        if fuser.balance < p_amount:
            flash("Insuffecient amount")
            return redirect(url_for('pay_phoneno'))
        else:
            tu = User.query.filter_by(phoneno=p_phonenumber).first()
            if not tu:
                flash("Phone Number dosent exist")
                return redirect(url_for('pay_username'))
            else:
                #updating database
                tuser = remBal.query.filter_by(username=tu.username).first()
                tuser.balance += p_amount
                fuser.balance -= p_amount
                db.session.commit()
                flash(f"{p_amount} sucessfully sent to {p_phonenumber}")
                obj = clientTranscation.query.all()
                tno = int(obj[-1].transcation_id)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                f_username = fuser.username
                new_trans = clientTranscation(
                    transcation_id = tno + 1,
                    f_username = f_username,
                    t_username = p_phonenumber,
                    amount = p_amount,
                    date = date.today(),
                    time = current_time
                )
                db.session.add(new_trans)
                db.session.commit()


    return render_template("pay_phoneno.html", username=current_user.username, logged_in=True)

#bank transfer
@app.route("/pay/banktransfer", methods=["GET", "POST"])
@login_required
def pay_banktransfer():
    return render_template("pay_banktransfer.html")

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    cu_bal = remBal.query.filter_by(username=current_user.username).first()
    trans = clientTranscation.query.all()
    return render_template("history.html",username=current_user.username, bal = cu_bal.balance, trans = trans)


#loan section
@app.route("/loan/avail", methods=["GET", "POST"])
@login_required
def loanavail():
    return render_template("avail_loan.html", username=current_user.username)

@app.route("/loan/pay", methods=["GET", "POST"])
@login_required
def loanpay():
    return render_template("pay_loan.html", username=current_user.username)

if __name__ == "__main__":
    app.run(debug=True)

