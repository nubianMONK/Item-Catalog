from datetime import datetime
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer.backend.sqla import (OAuthConsumerMixin)
from flask_login import (LoginManager, UserMixin)


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
login_manager = LoginManager()


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    picture = db.Column(db.String(250))
    role = db.Column(db.String(64))
    items = db.relationship('Item',
                            backref='item_creator',
                            lazy='dynamic')

    def __repr__(self):
        return '<User {}:{}>'.format(self.id, self.username)


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


class Item(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(64), index=True,)
    item_description = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category',
                               backref='category_item',
                               lazy='dynamic', uselist=True)

    def __repr__(self):
        return '<Item {}:{}>'.format(self.id, self.item_name)


class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(64), index=True, unique=True)
    items = db.relationship('Item',
                            backref='item_category',
                            lazy='dynamic')

    def __repr__(self):
        return '<Category {}:{}>'.format(self.id, self.category_name)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
