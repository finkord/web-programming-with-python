from flask import render_template, abort, redirect, url_for, flash, request, current_app, session
from . import post_bp
from .forms import PostForm
from .. import db
from .models import Post, PostCategory # Потрібно імпортувати моделі

# url_prefix="/post"

# ---------------------------------------------------------------
# 1. Створення поста (Create)
# ---------------------------------------------------------------
@post_bp.route('/create', methods=["GET", "POST"]) 
def create():
    form = PostForm()
    if form.validate_on_submit():
        
        # --- ЛОГІКА ДЛЯ ВИЗНАЧЕННЯ АВТОРА ---
        author_name = 'Anonymous' # Значення за замовчуванням
        
        # Припускаємо, що ви зберігаєте ім'я користувача 
        # в session['username'] під час логіну
        if 'username' in session:
            author_name = session['username']
        # ---------------------------------------

        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.posted.data,
            category=PostCategory(form.category.data),
            is_active=form.is_active.data,
            author=author_name  # <-- 2. Додано нове поле
        )
        
        db.session.add(new_post)
        db.session.commit()
        
        flash("Пост успішно створено!", "success")
        # 3. Виправлено помилку в url_for (було 'posts.get_posts')
        return redirect(url_for('posts.get_posts'))

    return render_template("add_post.html", form=form, title="Створення поста")

# ---------------------------------------------------------------
# 2. Отримання списку постів (Read - All)
# ---------------------------------------------------------------
@post_bp.route('/') 
def get_posts():
    # Отримуємо всі *активні* пости, сортуємо за датою (новіші спочатку)
    show_all = request.args.get('show_all') == 'true'

    query = Post.query

    if not show_all:
        query = query.filter_by(is_active=True)
    
    posts = query.order_by(Post.posted.desc()).all()
    
    return render_template("all_posts.html", posts=posts)

# ---------------------------------------------------------------
# 3. Перегляд конкретного поста (Read - One)
# ---------------------------------------------------------------
@post_bp.route('/<int:id>') 
def detail_post(id):
    # .first_or_404() автоматично поверне 404, якщо пост не знайдено
    post = Post.query.filter_by(id=id).first_or_404()
    
    return render_template("detail_post.html", post=post)

# ---------------------------------------------------------------
# 4. Редагування поста (Update)
# ---------------------------------------------------------------
@post_bp.route('/<int:id>/update', methods=["GET", "POST"]) 
def update(id):
    # .get_or_404() знайде пост за primary key, або поверне 404
    post = Post.query.get_or_404(id)
    
    # При GET-запиті: створюємо форму, наповнену даними з об'єкта 'post'
    # При POST-запиті: створюємо форму з даними, що прийшли
    form = PostForm(obj=post) if request.method == 'GET' else PostForm()

    if form.validate_on_submit():
        # Оновлюємо поля існуючого об'єкта 'post' даними з форми
        post.title = form.title.data
        post.content = form.content.data
        post.posted = form.posted.data
        post.category = PostCategory(form.category.data)
        post.is_active = form.is_active.data
        
        db.session.commit() # Зберігаємо зміни
        
        flash("Пост успішно оновлено!", "info")
        return redirect(url_for('posts.detail_post', id=post.id))

    return render_template("add_post.html", form=form, title="Редагування поста", post=post)

# ---------------------------------------------------------------
# 5. Видалення поста (Delete)
# ---------------------------------------------------------------
# Додаємо метод POST для безпечного видалення
@post_bp.route('/<int:id>/delete', methods=["GET", "POST"]) 
def delete(id):
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        # Якщо користувач підтвердив видалення (натиснув кнопку в формі)
        db.session.delete(post)
        db.session.commit()
        flash("Пост було видалено.", "success")
        return redirect(url_for('posts.get_posts'))
        
    # Якщо це GET-запит, просто показуємо сторінку підтвердження
    return render_template("delete_confirm.html", post=post)