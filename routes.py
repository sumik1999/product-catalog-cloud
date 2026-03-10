from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Product
from gcs_utils import upload_to_gcs, allowed_file, delete_from_gcs
from config import Config
import decimal
import os

main = Blueprint('main', __name__)

@main.route('/')
# Display all products on the homepage, ordered by creation date (newest first)
def index():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('index.html', products=products)

@main.route('/add', methods=['GET', 'POST'])
def add_product():
    # Handle form submission for adding a new product
    if request.method == 'POST':
        errors = {}
        
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price_str = request.form.get('price', '').strip()
        file = request.files.get('image')
        
        if not name:
            errors['name'] = 'Product name is required'
        elif len(name) > 200:
            errors['name'] = 'Product name must be 200 characters or less'
        
        if not price_str:
            errors['price'] = 'Price is required'
        else:
            try:
                price = decimal.Decimal(price_str)
                if price < 0:
                    errors['price'] = 'Price cannot be negative'
                elif price > 999999.99:
                    errors['price'] = 'Price is too large'
            except decimal.InvalidOperation:
                errors['price'] = 'Invalid price format'
        
        image_url = None
        if file and file.filename:
            if not allowed_file(file.filename):
                errors['image'] = 'Invalid file type. Allowed: png, jpg, jpeg, gif, webp'
            elif file.content_length and file.content_length > Config.MAX_CONTENT_LENGTH:
                errors['image'] = 'File size too large (max 16MB)'
            else:
                try:
                    image_url = upload_to_gcs(file, Config.GCS_BUCKET_NAME)
                except Exception as e:
                    errors['image'] = f'Failed to upload image: {str(e)}'
        
        if errors:
            for error in errors.values():
                flash(error, 'error')
            return render_template('add_product.html', 
                                   name=name, 
                                   description=description, 
                                   price=price_str,
                                   errors=errors)
        
        product = Product(
            name=name,
            description=description,
            price=price,
            image_url=image_url
        )
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('add_product.html')

@main.route('/product/<int:product_id>')
def product_detail(product_id):
    # Display detailed information about a specific product
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@main.route('/product/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    # Handle deletion of a product
    product = Product.query.get_or_404(product_id)
    
    if product.image_url:
        delete_from_gcs(product.image_url, Config.GCS_BUCKET_NAME)
    
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('main.index'))
