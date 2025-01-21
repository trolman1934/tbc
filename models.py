from flask_login import UserMixin


from ext import db, login_manager


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    img = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, default=0)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')




    def __repr__(self):
        return f'<Product {self.name}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

