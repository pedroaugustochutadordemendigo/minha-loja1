from flask import Blueprint, request, jsonify, session
from src.models.user import db
from src.models.product import Product, ProductVariant
from src.models.order import Cart, CartItem
import uuid

cart_bp = Blueprint('cart', __name__)

def get_or_create_cart():
    """Obter ou criar carrinho para o usuário/sessão"""
    user_id = session.get('user_id')
    session_id = session.get('cart_session_id')
    
    if not session_id:
        session_id = str(uuid.uuid4())
        session['cart_session_id'] = session_id
    
    # Buscar carrinho existente
    if user_id:
        cart = Cart.query.filter_by(user_id=user_id).first()
    else:
        cart = Cart.query.filter_by(session_id=session_id).first()
    
    # Criar novo carrinho se não existir
    if not cart:
        cart = Cart(
            user_id=user_id if user_id else None,
            session_id=session_id if not user_id else None
        )
        db.session.add(cart)
        db.session.commit()
    
    return cart

@cart_bp.route('/cart', methods=['GET'])
def get_cart():
    """Obter carrinho atual"""
    try:
        cart = get_or_create_cart()
        
        return jsonify({
            'success': True,
            'cart': cart.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500