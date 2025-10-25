from flask import Blueprint, url_for, redirect, request, render_template, flash, session, make_response
from .forms import LoginForm
from app import app # Assuming the Flask app instance is imported as 'app'

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

@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    """Handles user login, form validation, session management, and logging."""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        # Simple hardcoded credential check
        if username == 'admin' and password == 'secret':
            session['username'] = username

            # Log successful login attempt
            app.logger.info(f"Successful login for user: {username}")

            remember_msg = "із запам'ятовуванням" if remember else "без запам'ятовування"
            flash(f"Вхід успішно виконано, {username}! ({remember_msg})", 'success')

            return redirect(url_for('users_bp.profile'))

        else:
            # Log failed login attempt
            app.logger.warning(f"Failed login attempt for user: {username}")

            flash('Неправильне ім\'я користувача або пароль.', 'error')
            return redirect(url_for('users_bp.login'))

    # Log form validation errors for POST requests
    elif request.method == 'POST':
        app.logger.debug(f"Login form validation failed. Errors: {form.errors}")

    return render_template("users/login.html", title="Login Page", form=form)

@users_bp.route("/profile", methods=["GET", "POST"])
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
