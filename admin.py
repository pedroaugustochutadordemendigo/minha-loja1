from flask import Blueprint, request, jsonify, session
from ..models import db, User, Product, Order, Category

admin_bp = Blueprint('admin', __name__)

def require_admin():
    """Verificar se usuário é administrador"""
    user_id = session.get('user_id')
    if not user_id:
        return {'error': 'Usuário não autenticado'}, 401
    
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return {'error': 'Acesso negado'}, 403
    
    return None

@admin_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Obter dados do dashboard administrativo"""
    try:
        auth_error = require_admin()
        if auth_error:
            return auth_error
        
        # Estatísticas básicas
        total_products = Product.query.filter_by(is_active=True).count()
        total_orders = Order.query.count()
        total_users = User.query.filter_by(is_active=True).count()
        
        # Pedidos recentes
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        
        return {
            'stats': {
                'total_products': total_products,
                'total_orders': total_orders,
                'total_users': total_users
            },
            'recent_orders': [order.to_dict(include_items=False) for order in recent_orders]
        }, 200
        
    except Exception as e:
        return {'error': f'Erro ao carregar dashboard: {str(e)}'}, 500

@admin_bp.route('/orders', methods=['GET'])
def get_all_orders():
    """Listar todos os pedidos"""
    try:
        auth_error = require_admin()
        if auth_error:
            return auth_error
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = Order.query.order_by(Order.created_at.desc())\
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

