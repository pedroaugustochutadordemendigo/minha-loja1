    
    # Cupom de desconto
    coupon_code = db.Column(db.String(50))
    
    # Endereço de entrega
    shipping_address_line1 = db.Column(db.String(200), nullable=False)
    shipping_address_line2 = db.Column(db.String(200))
    shipping_city = db.Column(db.String(100), nullable=False)
    shipping_state = db.Column(db.String(50), nullable=False)
    shipping_zipcode = db.Column(db.String(20), nullable=False)
    shipping_country = db.Column(db.String(50), default='Brasil')
    
    # Endereço de cobrança
    billing_address_line1 = db.Column(db.String(200))
    billing_address_line2 = db.Column(db.String(200))
    billing_city = db.Column(db.String(100))
    billing_state = db.Column(db.String(50))
    billing_zipcode = db.Column(db.String(20))
    billing_country = db.Column(db.String(50), default='Brasil')
    
    # Informações de envio
    shipping_method = db.Column(db.String(100))
    tracking_code = db.Column(db.String(100))
    estimated_delivery = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    
    # Pagamento
    payment_method = db.Column(db.Enum(PaymentMethod))
    payment_id = db.Column(db.String(100))  # ID do pagamento no gateway
    payment_data = db.Column(db.JSON)  # Dados adicionais do pagamento
    
    # Observações
    notes = db.Column(db.Text)
    admin_notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    user = db.relationship('User', backref='orders')
    
    def generate_order_number(self):
        """Gera um número único para o pedido"""
        import random
        import string
        timestamp = datetime.now().strftime('%Y%m%d')
        random_part = ''.join(random.choices(string.digits, k=4))
        return f"PK{timestamp}{random_part}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'customer_email': self.customer_email,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'status': self.status.value if self.status else None,
            'payment_status': self.payment_status.value if self.payment_status else None,
            'subtotal': float(self.subtotal),
            'shipping_cost': float(self.shipping_cost),
            'discount_amount': float(self.discount_amount),
            'total_amount': float(self.total_amount),
            'coupon_code': self.coupon_code,
            'shipping_address': {
                'line1': self.shipping_address_line1,
                'line2': self.shipping_address_line2,
                'city': self.shipping_city,
                'state': self.shipping_state,
                'zipcode': self.shipping_zipcode,
                'country': self.shipping_country
            },
            'shipping_method': self.shipping_method,
            'tracking_code': self.tracking_code,
            'payment_method': self.payment_method.value if self.payment_method else None,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.id'))
    
    # Informações do produto no momento da compra
    product_name = db.Column(db.String(200), nullable=False)
    product_sku = db.Column(db.String(100))
    variant_info = db.Column(db.JSON)  # Tamanho, cor, etc.
    
    # Preços e quantidades
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    product = db.relationship('Product', backref='order_items')
    variant = db.relationship('ProductVariant', backref='order_items')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_sku': self.product_sku,
            'variant_info': self.variant_info,
            'unit_price': float(self.unit_price),
            'quantity': self.quantity,
            'total_price': float(self.total_price)
        }

class Cart(db.Model):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100))  # Para usuários não logados
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')
    user = db.relationship('User', backref='carts')
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items)
    
    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items)
    
    def to_dict(self):
        return {
            'id': self.id,
            'total_items': self.total_items,
            'total_amount': float(self.total_amount),
            'items': [item.to_dict() for item in self.items],
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.id'))
    
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    product = db.relationship('Product', backref='cart_items')
    variant = db.relationship('ProductVariant', backref='cart_items')
    
    @property
    def total_price(self):
        return self.unit_price * self.quantity
    
    def to_dict(self):
        return {
            'id': self.id,
            'product': self.product.to_dict() if self.product else None,
            'variant': self.variant.to_dict() if self.variant else None,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'total_price': float(self.total_price),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

