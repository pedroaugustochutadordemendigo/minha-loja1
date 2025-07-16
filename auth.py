from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from ..models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registrar novo usuário"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'Campo {field} é obrigatório'}, 400
        
        # Verificar se usuário já existe
        if User.query.filter_by(username=data['username']).first():
            return {'error': 'Nome de usuário já existe'}, 400
        
        if User.query.filter_by(email=data['email']).first():
            return {'error': 'Email já está em uso'}, 400
        
        # Criar novo usuário
        user = User.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone=data.get('phone')
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Fazer login automático
        session['user_id'] = user.id
        session['user_username'] = user.username
        
        return {
            'message': 'Usuário criado com sucesso',
            'user': user.to_dict()
        }, 201
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Erro ao criar usuário: {str(e)}'}, 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Fazer login do usuário"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data.get('username') or not data.get('password'):
            return {'error': 'Username e password são obrigatórios'}, 400
        
        # Buscar usuário
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return {'error': 'Credenciais inválidas'}, 401
        
        if not user.is_active:
            return {'error': 'Conta desativada'}, 401
        
        # Criar sessão
        session['user_id'] = user.id
        session['user_username'] = user.username
        session['is_admin'] = user.is_admin
        
        return {
            'message': 'Login realizado com sucesso',
            'user': user.to_dict()
        }, 200
        
    except Exception as e:
        return {'error': f'Erro ao fazer login: {str(e)}'}, 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Fazer logout do usuário"""
    try:
        session.clear()
        return {'message': 'Logout realizado com sucesso'}, 200
    except Exception as e:
        return {'error': f'Erro ao fazer logout: {str(e)}'}, 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Obter dados do usuário logado"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Usuário não autenticado'}, 401
        
        user = User.query.get(user_id)
        if not user:
            session.clear()
            return {'error': 'Usuário não encontrado'}, 404
        
        return {'user': user.to_dict()}, 200
        
    except Exception as e:
        return {'error': f'Erro ao obter usuário: {str(e)}'}, 500

@auth_bp.route('/profile', methods=['PUT'])
def update_profile():
    """Atualizar perfil do usuário"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Usuário não autenticado'}, 401
        
        user = User.query.get(user_id)
        if not user:
            return {'error': 'Usuário não encontrado'}, 404
        
        data = request.get_json()
        
        # Atualizar campos permitidos
        allowed_fields = ['first_name', 'last_name', 'phone', 'email']
        for field in allowed_fields:
            if field in data:
                # Verificar se email já está em uso por outro usuário
                if field == 'email' and data[field] != user.email:
                    existing_user = User.query.filter_by(email=data[field]).first()
                    if existing_user:
                        return {'error': 'Email já está em uso'}, 400
                
                setattr(user, field, data[field])
        
        db.session.commit()
        
        return {
            'message': 'Perfil atualizado com sucesso',
            'user': user.to_dict()
        }, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Erro ao atualizar perfil: {str(e)}'}, 500

@auth_bp.route('/change-password', methods=['PUT'])
def change_password():
    """Alterar senha do usuário"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Usuário não autenticado'}, 401
        
        user = User.query.get(user_id)
        if not user:
            return {'error': 'Usuário não encontrado'}, 404
        
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data.get('current_password') or not data.get('new_password'):
            return {'error': 'Senha atual e nova senha são obrigatórias'}, 400
        
        # Verificar senha atual
        if not user.check_password(data['current_password']):
            return {'error': 'Senha atual incorreta'}, 400
        
        # Atualizar senha
        user.set_password(data['new_password'])
        db.session.commit()
        
        return {'message': 'Senha alterada com sucesso'}, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Erro ao alterar senha: {str(e)}'}, 500

@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    """Verificar se há uma sessão ativa"""
    try:
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user and user.is_active:
                return {
                    'authenticated': True,
                    'user': user.to_dict()
                }, 200
        
        return {'authenticated': False}, 200
        
    except Exception as e:
        return {'error': f'Erro ao verificar sessão: {str(e)}'}, 500

