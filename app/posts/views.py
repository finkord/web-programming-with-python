from flask import render_template, abort, redirect, url_for, flash, request, current_app, session
from . import post_bp
from .forms import PostForm
from .. import db
from .models import Post, PostCategory, Tag
from sqlalchemy import select

from app.users.models import User

# url_prefix="/post"

# ---------------------------------------------------------------
# 1. Створення поста (Create)
# ---------------------------------------------------------------
@post_bp.route('/create', methods=["GET", "POST"]) 
def create():
    form = PostForm()
    
    # Використовуємо select для отримання списку юзерів
    user_query = select(User).order_by(User.username)
    form.user.choices = [
        (user.id, user.username) for user in db.session.scalars(user_query)
    ]

    # Використовуємо select для отримання списку тегів
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

    stmt = select(Post)

    if not show_all:
        stmt = stmt.where(Post.is_active.is_(True)) # Більш "пітонічний" варіант для SQLAlchemy
    
    stmt = stmt.order_by(Post.posted.desc())
    
    posts = db.session.scalars(stmt).all()
    
    return render_template("all_posts.html", posts=posts)

# ---------------------------------------------------------------
# 3. Перегляд конкретного поста (Read - One)
# ---------------------------------------------------------------
@post_bp.route('/<int:id>') 
def detail_post(id):
    # Новий синтаксис: db.get_or_404(Model, id)
    post = db.get_or_404(Post, id)
    
    return render_template("detail_post.html", post=post)

# ---------------------------------------------------------------
# 4. Редагування поста (Update)
# ---------------------------------------------------------------
@post_bp.route('/<int:id>/update', methods=["GET", "POST"]) 
def update(id):
    # Новий синтаксис
    post = db.get_or_404(Post, id)
    
    if request.method == 'POST':
        form = PostForm()
    else: # GET
        form = PostForm(obj=post)
        form.user.data = post.user_id 
        form.tags.data = [tag.id for tag in post.tags]

    # Оновлюємо вибір для полів SelectField (теж через select)
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
        
        selected_user = db.session.get(User, form.user.data)
        selected_tags = [
            db.session.get(Tag, tag_id) 
            for tag_id in form.tags.data
        ]
        
        post.title = form.title.data
        post.content = form.content.data
        post.posted = form.posted.data
        post.category = PostCategory(form.category.data)
        post.is_active = form.is_active.data
        
        post.user = selected_user
        post.tags = selected_tags  

        db.session.commit()
        
        flash("Пост успішно оновлено!", "info")
        return redirect(url_for('posts.detail_post', id=post.id))
    return render_template("add_post.html", form=form, title="Редагування поста", post=post)

# ---------------------------------------------------------------
# 5. Видалення поста (Delete)
# ---------------------------------------------------------------
@post_bp.route('/<int:id>/delete', methods=["GET", "POST"]) 
def delete(id):
    # Новий синтаксис
    post = db.get_or_404(Post, id)
    
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash("Пост було видалено.", "success")
        return redirect(url_for('posts.get_posts'))
        
    return render_template("delete_confirm.html", post=post)