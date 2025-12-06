from .. import db
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class FriendGroup(db.Model):
    __tablename__ = 'friend_groups'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Зв'язок: одна група має багато друзів
    friends: Mapped[list["Friend"]] = relationship(back_populates="group")

    def __repr__(self):
        return self.name

class Friend(db.Model):
    __tablename__ = 'friends'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(120), nullable=True)
    
    # Зовнішній ключ для групи
    group_id: Mapped[int] = mapped_column(ForeignKey('friend_groups.id'), nullable=False)
    group: Mapped["FriendGroup"] = relationship(back_populates="friends")

    # Зовнішній ключ для користувача (власника запису)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship()

    def __repr__(self):
        return f"<Friend {self.first_name} {self.last_name}>"