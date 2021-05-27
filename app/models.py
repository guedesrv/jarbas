from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time
from app import db, login_manager, app_config


class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app_config['production'].SECRET_KEY, algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app_config['production'].SECRET_KEY, algorithms=['HS256'])['reset_password']
        except Exception as e:
            raise e
        return User.query.get(id)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class Company(db.Model):
    """
    Create a Company table
    """

    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    link = db.Column(db.String(200))
    image = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Company: {}>'.format(self.name)


class Product(db.Model):
    """
    Create a Product table
    """

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    link = db.Column(db.String(200))
    min_price = db.Column(db.Float)
    max_price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    word_less = db.relationship('WordLess', backref='products', lazy=True)

    def __repr__(self):
        return '<Product: {}>'.format(self.name)

class WordLess(db.Model):
    """
    Create a WordLess table
    """

    __tablename__ = 'word_less'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    def __repr__(self):
        return '<WordLess: {}>'.format(self.name)