from flask import Blueprint, request, jsonify, session
from ..models import db, Order, OrderItem, Cart, CartItem, Product
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['GET'])
def get_orders():
    """Listar pedidos do usuário"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Usuário não autenticado'}, 401
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        pagination = Order.query.filter_by(user_id=user_id)\
            .order_by(Order.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'orders': [order.to_dict(include_items=False) for order in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }, 200
        
    except Exception as e:
        return {'error': f'Erro ao buscar pedidos: {str(e)}'}, 500

@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Obter detalhes de um pedido"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Usuário não autenticado'}, 401
        
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if not order:
            return {'error': 'Pedido não encontrado'}, 404
        
        return {'order': order.to_dict()}, 200
        
    except Exception as e:
        return {'error': f'Erro ao buscar pedido: {str(e)}'}, 500

@orders_bp.route('/create', methods=['POST'])
def create_order():
    """Criar novo pedido a partir do carrinho"""
    try:
        data = request.get_json()
        user_id = session.get('user_id')
        
        # Validar dados obrigatórios
        required_fields = ['customer_name', 'customer_email', 'shipping_address']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'Campo {field} é obrigatório'}, 400
        
        # Obter carrinho
        cart_session_id = session.get('cart_session_id')
        if user_id:
            cart = Cart.query.filter_by(user_id=user_id).first()
        else:
            cart = Cart.query.filter_by(session_id=cart_session_id).first()
        
        if not cart or not cart.items:
            return {'error': 'Carrinho vazio'}, 400
        
        # Criar pedido
        order = Order(
            user_id=user_id,
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            customer_phone=data.get('customer_phone'),
            customer_document=data.get('customer_document'),
            subtotal=cart.total_amount,
            shipping_cost=data.get('shipping_cost', 0),
            total_amount=cart.total_amount + data.get('shipping_cost', 0),
            shipping_address_line1=data['shipping_address']['line1'],
            shipping_address_line2=data['shipping_address'].get('line2'),
            shipping_city=data['shipping_address']['city'],
            shipping_state=data['shipping_address']['state'],
            shipping_zipcode=data['shipping_address']['zipcode'],
            shipping_method=data.get('shipping_method'),
            payment_method=data.get('payment_method'),
            notes=data.get('notes')
        )
        
        # Gerar número do pedido
        order.order_number = order.generate_order_number()
        
        db.session.add(order)
        db.session.flush()  # Para obter o ID do pedido
        
        # Criar itens do pedido
        for cart_item in cart.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                variant_id=cart_item.variant_id,
                product_name=cart_item.product.name,
                product_sku=cart_item.variant.sku if cart_item.variant else None,
                variant_info=cart_item.variant.to_dict() if cart_item.variant else None,
                unit_price=cart_item.unit_price,
                quantity=cart_item.quantity,
                total_price=cart_item.total_price
            )
            db.session.add(order_item)
        
        # Limpar carrinho
        cart.clear()
        
        db.session.commit()
        
        return {
            'message': 'Pedido criado com sucesso',
            'order': order.to_dict()
        }, 201
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Erro ao criar pedido: {str(e)}'}, 500

