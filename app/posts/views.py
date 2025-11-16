from flask import render_template, abort, redirect, url_for, flash, request, current_app, session
from . import post_bp
from .forms import PostForm
from .. import db
from .models import User, Post, PostCategory,Tag
from sqlalchemy import select

# url_prefix="/post"

# ---------------------------------------------------------------
# 1. Створення поста (Create)
# ---------------------------------------------------------------
@post_bp.route('/create', methods=["GET", "POST"]) 
def create():
    form = PostForm()
    
    user_query = select(User).order_by(User.username)
    form.user.choices = [
        (user.id, user.username) for user in db.session.scalars(user_query)
    ]

    tag_query = select(Tag).order_by(Tag.name)
    form.tags.choices = [
        (tag.id, tag.name)    # id → value, name → label
        for tag in db.session.scalars(tag_query)
    ]

    if form.validate_on_submit():
        
        selected_user = db.session.get(User, form.user.data)

        selected_tags = [
            db.session.get(Tag, tag_id) 
            for tag_id in form.tags.data
        ]

        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.posted.data,
            category=PostCategory(form.category.data),
            is_active=form.is_active.data,
            user=selected_user  
        )

        new_post.tags.extend(selected_tags)
        
        db.session.add(new_post)
        db.session.commit()
        
        flash("Пост успішно створено!", "success")
        
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
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        # При POST-запиті форма заповниться з 'request.form'
        form = PostForm()
    else: # GET
        form = PostForm(obj=post)
        form.user.data = post.user_id # Встановлюємо ID обраного юзера
        form.tags.data = [tag.id for tag in post.tags] # Встановлюємо список ID тегів

    user_query = select(User).order_by(User.username)
    form.user.choices = [
        (user.id, user.username) for user in db.session.scalars(user_query)
    ]
    tag_query = select(Tag).order_by(Tag.name)
    form.tags.choices = [
        (tag.id, tag.name) for tag in db.session.scalars(tag_query)
    ]

    # 4. Валідація та оновлення
    if form.validate_on_submit():
        
        # 5. Отримуємо об'єкти User та Tag з БД (як у 'create')
        selected_user = db.session.get(User, form.user.data)
        selected_tags = [
            db.session.get(Tag, tag_id) 
            for tag_id in form.tags.data
        ]
        
        # 6. Оновлюємо поля існуючого об'єкта 'post'
        post.title = form.title.data
        post.content = form.content.data
        post.posted = form.posted.data
        post.category = PostCategory(form.category.data)
        post.is_active = form.is_active.data
        
        # 7. Оновлюємо зв'язки
        post.user = selected_user
        post.tags = selected_tags  

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