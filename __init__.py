from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar todos os modelos para garantir que sejam registrados
from .user import User
from .product import Product, Category, ProductImage, ProductVariant
from .order import Order, OrderItem, Cart, CartItem

__all__ = [
    'db',
    'User',
    'Product',
    'Category', 
    'ProductImage',
    'ProductVariant',
    'Order',
    'OrderItem',
    'Cart',
    'CartItem'
]

