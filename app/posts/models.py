# app/posts/models.py
from datetime import datetime
from .. import db
import enum

class PostCategory(enum.Enum):
    news = 'news'
    publication = 'publication'
    tech = 'tech'
    other = 'other'

class Post(db.Model):
    """
    ORM-модель Post для Flask-SQLAlchemy.
    """
    __tablename__ = 'posts'

    # Поле id (Integer, Primary Key)
    id = db.Column(db.Integer, primary_key=True)

    # Поле title (String(150), Not Null)
    # nullable=False еквівалентно Not Null
    title = db.Column(db.String(150), nullable=False)

    # Поле content (Text, Not Null)
    content = db.Column(db.Text, nullable=False)

    # Поле posted (DateTime, Default = datetime.utcnow)
    posted = db.Column(db.DateTime, default=datetime.utcnow)

    # Поле category (Enum)
    category = db.Column(db.Enum(PostCategory))

    #Поле is_active (Boolean, Default = True)
    # Визначає, чи пост активний і відображається на сайті
    is_active = db.Column(db.Boolean, default=True)

    # Поле author (String(20), Default = 'Anonymous')
    # Ім’я автора поста
    author = db.Column(db.String(20), default='Anonymous')

    def __repr__(self):
        """
        Метод __repr__ згідно з завданням.
        Повертає офіційне рядкове представлення об'єкта.
        """
        return f"<Post(id={self.id}, title='{self.title}', author='{self.author}')>"

    # def __str__(self):
    #     """
    #     Метод __str__ повертає "людське" представлення об'єкта.
    #     """
    #     return self.title