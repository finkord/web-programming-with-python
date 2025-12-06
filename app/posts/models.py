# app/posts/models.py
from datetime import datetime

from .. import db
import enum

from sqlalchemy import (
    String, Text, DateTime, 
    Boolean, Enum, ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.users.models import User

class PostCategory(enum.Enum):
    news = 'news'
    publication = 'publication'
    tech = 'tech'
    other = 'other'

post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    posted: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow
    )
    
    category: Mapped[PostCategory] = mapped_column(
        Enum(PostCategory), 
        nullable=True  
    )
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, back_populates="posts")

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r})"

class Tag(db.Model):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    posts: Mapped[list["Post"]] = relationship(secondary=post_tags, back_populates="tags")

    def __repr__(self) -> str:
        return f"Tag(id={self.id!r}, name={self.name!r})"

