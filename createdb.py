from wtforms.validators import email
from werkzeug.security import generate_password_hash
from ext import app, db
from models import Product, User


products = ({"name": "iphone", "price":4000, "img": "smartphone.jpg"},
      {"name": "iphone2", "price":3000, "img": "smartphone.jpg"},
      {"name": "iphone3", "price":2000, "img": "smartphone.jpg"},)




users = {
    "gela": {"fullname": "gela", "age":24, "role": "admin"},
    "jimi": {"fullname": "jimi", "age":32, "role": "moderator"},
    "givi": {"fullname": "givi", "age":27, "role": "user"},
}

with app.app_context():
  db.drop_all()
  db.create_all()
  for product in products:
    new_product = Product(name=product["name"], price=product["price"], img=product["img"], description="hi")
    db.session.add(new_product)
    db.session.commit()

  hashed_password = generate_password_hash("adminpassword")

  admin_user = User(email="admin@example.com", password=hashed_password, role="admin")

  db.session.add(admin_user)
  db.session.commit()








