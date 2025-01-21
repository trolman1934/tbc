import os
from itertools import product
from werkzeug.security import generate_password_hash


from flask import Flask, render_template, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from forms import RegistrationForm, LoginForm, ProductForm
from ext import app, db
from models import Product, User


@app.route('/reg', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('This email is already registered. Please use a different email.', 'danger')
            return redirect(url_for('register'))


        new_user = User(

            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('registration.html', form=form)



@app.route('/log', methods=['GET', 'POST'])
def login():
    form1 = LoginForm()
    if form1.validate_on_submit():
        user = User.query.filter(User.email == form1.email.data).first()
        if user and check_password_hash(user.password, form1.password.data):
            login_user(user)
            return redirect("/")
        else:
            print("User not found or password incorrect.")
    else:
        print("Form validation failed.")

    return render_template('login.html', form=form1)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')

    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/products')
def product_list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)


@app.route("/create_product", methods=['GET', 'POST'])
def create_product():
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash('You do not have permission to create products.', 'danger')
        return redirect(url_for('index'))

    products = Product.query.all()
    form = ProductForm()

    if form.validate_on_submit():
        image = form.img.data
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new_product = Product(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                img=filename
            )

            db.session.add(new_product)
            db.session.commit()

            flash('Product created successfully!', 'success')
            return redirect(url_for('product_list'))
    print(form.errors)

    return render_template('create_product.html', form=form, products=products)



@app.route("/delete_product/<int:product_id>", methods=["GET", "POST"])
def delete_product(product_id):
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash('You do not have permission to create products.', 'danger')
        return redirect(url_for('index'))
    product = Product.query.get(product_id)

    db.session.delete(product)
    db.session.commit()
    return redirect("/products")



@app.route("/edit_product/<int:product_id>", methods=['GET', 'POST'])
def edit_product(product_id):
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash('You do not have permission to create products.', 'danger')
        return redirect(url_for('index'))
    product = Product.query.get_or_404(product_id)
    form = ProductForm()

    if form.validate_on_submit():

        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data


        if form.img.data:
            image = form.img.data
            if allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                product.img = filename


        db.session.commit()

        flash('Product updated successfully!', 'success')
        return redirect(url_for('product_list'))

    return render_template('edit_product.html', form=form, product=product)



@app.route('/like_product/<int:product_id>', methods=['POST'])
def like_product(product_id):
    if not current_user.is_authenticated:
        flash('You must be logged in to like a product.', 'danger')
        return redirect(url_for('login'))

    product = Product.query.get_or_404(product_id)
    product.likes += 1
    db.session.commit()

    flash('Product liked!', 'success')
    return redirect(url_for('product_list'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']