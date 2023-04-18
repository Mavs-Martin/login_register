# used for routing
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user_mod import User
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
from flask import flash

# view login / reg page

@app.route("/")
def index():
    return render_template("index.html")


#========REGISTER - METHOD - ACTION
@app.route("/user/register", methods = ['post'])
def user_reg():
    # print (request.form)
    if not  User.validate(request.form):
        return redirect("/")
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    user_data={
        **request.form,
        'password': pw_hash
    }
    
    user_id = User.create(user_data)
    session['user_id'] = user_id

    return redirect("/dashboard")

#==============LOGIN ACTION /POST==========
@app.route("/users/login", methods=['post'])
def user_login():
    print (request.form)
    user_in_db = User.get_by_email(request.form['email'])
    print(user_in_db)
    if not user_in_db:  
        flash("invalid credentials", "login")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("invalid credentials", "login")
        return redirect("/")
    session['user_id'] = user_in_db.id

    return redirect("/dashboard")

#============dashboard is a render or view
@app.route("/dashboard")
def dash():
    #! ROUTE GUARD
    if 'user_id' not in session:
        return redirect("/")
    logged_user = User.get_by_id(session['user_id'])
    return render_template("welcome.html", logged_user=logged_user)


#!=============LOGOUT===================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")