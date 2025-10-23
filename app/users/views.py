from flask import Blueprint, url_for, redirect, request, render_template, flash, session

# Defining a blueprint
users_bp = Blueprint(
    'users_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@users_bp.route("/hi/<string:name>") #/hi/ivan?age=45
def greetings (name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html",name=name, age=age, title="Greating Page")

@users_bp.route("/admin")
def admin():
    to_url = url_for("users_bp.greetings", name="administrator", age=45, _external=True,title="Greating Page")
    print(to_url)
    return redirect(to_url)

@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            session['username'] = request.form['username']
            flash('You were successfully logged in','success')
            return redirect(url_for('users_bp.profile'))
    return render_template("users/login.html",title="Login Page", error=error)

@users_bp.route("/profile")
def profile():
    username = session.get('username')
    if not username:
        flash('Please log in to view this page.', 'warning')
        return redirect(url_for('users_bp.login'))
    return render_template("users/profile.html",title="Profile Page", username=username)

@users_bp.route("/logout")
def logout():
    session.pop('username', None) 
    # session.clear()
    
    flash('You have been logged out.', 'info')
    return redirect(url_for('users_bp.login'))