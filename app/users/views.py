from flask import Blueprint, url_for, redirect, request, render_template, flash, session, make_response, current_app
from .forms import LoginForm, RegistrationForm, UpdateAccountForm, ChangePasswordForm
from .. import db
from .models import User
from flask_login import login_user, login_required, current_user, logout_user

import os
import secrets
from PIL import Image

from datetime import datetime

# Defining a blueprint for user-related routes
users_bp = Blueprint(
    'users_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@users_bp.route("/hi/<string:name>")  # /hi/ivan?age=45
def greetings(name):
    """Renders a greeting page with a name (uppercase) and optional age from query params."""
    name = name.upper()
    # Safely get 'age' argument, defaulting to None, and convert to int
    age = request.args.get("age", None, type=int)
    return render_template("users/hi.html", name=name, age=age, title="Greeting Page")

@users_bp.route("/admin")
def admin():
    """Redirects to the greetings route with specific parameters for 'administrator'."""
    # Example of generating an external URL
    to_url = url_for("users_bp.greetings", name="administrator", age=45, _external=True, title="Greeting Page")
    print(to_url)
    return redirect(to_url)

@users_bp.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()
    
    if current_user.is_authenticated:
        return redirect(url_for('users_bp.account'))

    if form.validate_on_submit():
        
        hashed_password = User.hash_password(form.password.data)

        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()
        
        flash(f"Ваш акаунт створено! Тепер ви можете увійти.", "success")
        
        return redirect(url_for('users_bp.login')) 
    return render_template("users/register.html", title="Реєстрація", form=form)

@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    """Обробляє вхід користувача з перевіркою пароля через хешування."""
    form = LoginForm()

    if form.validate_on_submit():
        username_or_email = form.username.data  
        password = form.password.data
        remember = form.remember.data
        
        user = User.query.filter_by(username=username_or_email).first()

        if user and user.check_password(password):
            
            session['user_id'] = user.id  
            session['username'] = user.username 

            login_user(user, remember=form.remember.data)
            
            current_app.logger.info(f"Successful login for user: {user.username}")

            remember_msg = "із запам'ятовуванням" if remember else "без запам'ятовування"
            flash(f"Вхід успішно виконано, {user.username}! ({remember_msg})", 'success')

            return redirect(url_for('users_bp.profile'))

        else:
            current_app.logger.warning(f"Failed login attempt for user: {username_or_email}")

            flash('Неправильне ім\'я користувача або пароль.', 'error')
            return redirect(url_for('users_bp.login'))
        
    elif request.method == 'POST':
        current_app.logger.debug(f"Login form validation failed. Errors: {form.errors}")

    return render_template("users/login.html", title="Сторінка входу", form=form)

@users_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Displays user profile and handles cookie management (add/delete)."""
    username = session.get("username")
    if not username:
        flash("Please log in to view this page.", "warning")
        return redirect(url_for("users_bp.login"))

    # --- Handle POST requests (form submission) ---
    if request.method == "POST":
        # Create a redirect response object; cookies are set on the response object.
        resp = make_response(redirect(url_for("users_bp.profile")))

        # Determine which action button was pressed
        action = request.form.get("action")

        if action == "add_cookie":
            key = request.form.get("cookie_key")
            value = request.form.get("cookie_value")
            expiry_str = request.form.get("cookie_expiry")

            if key and value:
                max_age = None
                # Set max_age if provided and valid
                if expiry_str and expiry_str.isdigit():
                    max_age = int(expiry_str)

                resp.set_cookie(key, value, max_age=max_age)
                flash(f"Кукі '{key}' успішно додано.", "success")

        elif action == "delete_one":
            key_to_delete = request.form.get("cookie_key_to_delete")
            if key_to_delete:
                resp.delete_cookie(key_to_delete)
                flash(f"Кукі '{key_to_delete}' видалено.", "info")

        elif action == "delete_all":
            # Iterate through all cookies received in the request
            deleted_count = 0
            for key in request.cookies.keys():
                # DO NOT delete the session cookie, as it would log the user out
                if key != "session":
                    resp.delete_cookie(key)
                    deleted_count += 1
            flash(f"Видалено {deleted_count} кукі (крім сесії).", "info")

        return resp

    # --- Handle GET request (just display the page) ---
    return render_template(
        "users/profile.html", title="Profile Page", username=username
    )


@users_bp.route("/logout")
def logout():
    """Logs out the user by removing 'username' from the session."""
    session.pop("username", None)
    logout_user()

    flash("You have been logged out.", "info")
    return redirect(url_for("users_bp.login"))

@users_bp.route("/set-theme/<theme_name>")
def set_theme(theme_name):
    """Sets the color scheme and saves it to a cookie."""
    if theme_name not in ("light", "dark"):
        theme_name = "dark"  # Default to dark

    # Redirects back to the page the user came from, or profile if not available
    redirect_to = request.referrer or url_for("users_bp.profile")

    # Create the response object for setting the cookie
    resp = make_response(redirect(redirect_to))

    # Set the 'theme' cookie for 1 year
    max_age_seconds = 365 * 24 * 60 * 60
    resp.set_cookie("theme", theme_name, max_age=max_age_seconds)

    flash(f"Тему змінено на {theme_name}.", "info")
    return resp

def save_picture(form_picture):
    """
    Зберігає:
    1. Оригінал зображення (file_name.ext).
    2. Мініатюру 128x128 (thumb_file_name.ext).
    Повертає ім'я файлу оригіналу.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    images_folder = os.path.join(current_app.root_path, 'static/images')
    original_path = os.path.join(images_folder, picture_fn)
    thumb_path = os.path.join(images_folder, 'thumb_' + picture_fn)

    i = Image.open(form_picture)

    i.save(original_path)

    i.thumbnail((128, 128))
    i.save(thumb_path)

    return picture_fn

@users_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@users_bp.route("/account", methods=["GET","POST"])
@login_required
def account():
    """
    Обробляє запит до сторінки акаунту та дозволяє оновлювати дані.
    """
    form = UpdateAccountForm()
    pwd_form = ChangePasswordForm()

    if form.submit.data and form.validate():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        
        db.session.commit()
        flash('Ваш акаунт успішно оновлено!', 'success')
        return redirect(url_for('users_bp.account'))
    
    if pwd_form.submit_pass.data and pwd_form.validate():
        if current_user.check_password(pwd_form.old_password.data):
            hashed_password = User.hash_password(pwd_form.new_password.data)
            current_user.password = hashed_password
            
            db.session.commit()
            flash('Ваш пароль успішно змінено!', 'success')
            return redirect(url_for('users_bp.account'))
        else:
            flash('Старий пароль введено невірно.', 'error')

    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_file = url_for('static', filename='images/' + (current_user.image or 'profile_default.jpg'))

    return render_template(
            "users/account.html", 
            title="Мій акаунт", 
            user=current_user, 
            form=form, 
            pwd_form=pwd_form, 
            image_file=image_file
        )

@users_bp.route("/users")
@login_required
def list_users():
    """
    Отримує список усіх користувачів з бази даних та їх кількість.
    """

    users = User.query.order_by(User.username).all()

    user_count = len(users)

    return render_template(
        "users/list_users.html", 
        title="Список користувачів", 
        users=users, 
        user_count=user_count
    )