from flask import Blueprint, url_for, redirect, request, render_template, flash, session,request,request, make_response

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
    # error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            # error = 'Invalid credentials'
            flash('Invalid credentials','error')
        else:
            session['username'] = request.form['username']
            flash('You were successfully logged in','success')

            return redirect(url_for('users_bp.profile'))
    return render_template("users/login.html",title="Login Page")

@users_bp.route("/profile", methods=["GET", "POST"])  # Додано methods
def profile():
    username = session.get("username")
    if not username:
        flash("Please log in to view this page.", "warning")
        return redirect(url_for("users_bp.login"))

    # --- Обробка POST-запитів (коли форма відправлена) ---
    if request.method == "POST":
        # Створюємо відповідь-перенаправлення.
        # Кукі встановлюються на об'єкт відповіді (response).
        resp = make_response(redirect(url_for("users_bp.profile")))

        # Визначаємо, яка форма була відправлена, за іменем кнопки
        action = request.form.get("action")

        if action == "add_cookie":
            key = request.form.get("cookie_key")
            value = request.form.get("cookie_value")
            expiry_str = request.form.get("cookie_expiry")

            if key and value:
                max_age = None
                # Встановлюємо термін дії, якщо він вказаний і є числом
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
            # Проходимо по всіх кукі, які прийшли в запиті
            deleted_count = 0
            for key in request.cookies.keys():
                # НЕ видаляємо кукі сесії, інакше користувач вийде з системи
                if key != "session":
                    resp.delete_cookie(key)
                    deleted_count += 1
            flash(f"Видалено {deleted_count} кукі (крім сесії).", "info")

        return resp

    # --- Обробка GET-запиту (просто показ сторінки) ---
    return render_template(
        "users/profile.html", title="Profile Page", username=username
    )


@users_bp.route("/logout")
def logout():
    session.pop("username", None)

    flash("You have been logged out.", "info")
    return redirect(url_for("users_bp.login"))