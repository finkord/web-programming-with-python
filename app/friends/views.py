from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from .. import db
from . import friends_bp
from .models import Friend, FriendGroup
from .forms import FriendForm, SearchForm, GroupForm
from sqlalchemy import select

@friends_bp.route('/', methods=['GET'])
@login_required
def list_friends():
    """Виводить список друзів поточного користувача з пошуком та сортуванням."""
    search_form = SearchForm(request.args)
    
    # Базовий запит: тільки друзі поточного користувача
    query = select(Friend).where(Friend.user_id == current_user.id)

    # Пошук
    search_query = request.args.get('query')
    if search_query:
        query = query.where(Friend.last_name.ilike(f"%{search_query}%"))

    # Сортування (за прізвищем)
    query = query.order_by(Friend.last_name)

    friends = db.session.scalars(query).all()

    return render_template('list.html', friends=friends, search_form=search_form, title="Мої Друзі")

@friends_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_friend():
    form = FriendForm()
    # Підтягуємо варіанти груп з БД
    form.group_id.choices = [(g.id, g.name) for g in db.session.scalars(select(FriendGroup)).all()]

    if form.validate_on_submit():
        new_friend = Friend(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            email=form.email.data,
            group_id=form.group_id.data,
            user_id=current_user.id  # Прив'язка до поточного юзера
        )
        db.session.add(new_friend)
        db.session.commit()
        flash('Друга успішно додано!', 'success')
        return redirect(url_for('friends.list_friends'))

    return render_template('form.html', form=form, title="Додати друга")

@friends_bp.route('/<int:id>')
@login_required
def detail_friend(id):
    friend = db.get_or_404(Friend, id)
    # Перевірка прав доступу
    if friend.user_id != current_user.id:
        abort(403)
    return render_template('detail.html', friend=friend, title="Детальна Інформація")

@friends_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_friend(id):
    friend = db.get_or_404(Friend, id)
    
    if friend.user_id != current_user.id:
        abort(403)

    form = FriendForm(obj=friend)
    form.group_id.choices = [(g.id, g.name) for g in db.session.scalars(select(FriendGroup)).all()]

    if form.validate_on_submit():
        form.populate_obj(friend) # Автоматичне оновлення полів
        db.session.commit()
        flash('Дані оновлено!', 'success')
        return redirect(url_for('friends.detail_friend', id=friend.id))

    return render_template('form.html', form=form, title="Редагувати друга")

@friends_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_friend(id):
    friend = db.get_or_404(Friend, id)
    
    if friend.user_id != current_user.id:
        abort(403)

    db.session.delete(friend)
    db.session.commit()
    flash('Друга видалено.', 'info')
    return redirect(url_for('friends.list_friends'))

@friends_bp.route('/groups/create', methods=['GET', 'POST'])
@login_required
def create_group():
    form = GroupForm()
    
    if form.validate_on_submit():
        new_group = FriendGroup(name=form.name.data)
        db.session.add(new_group)
        db.session.commit()
        flash('Нову групу успішно створено!', 'success')
        # Повертаємось до створення друга, адже часто групу створюють саме для цього
        return redirect(url_for('friends.create_friend'))
    
    return render_template('group_form.html', form=form, title="Створити групу")