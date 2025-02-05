from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    channels = db.relationship("Channel", back_populates="user", cascade="all, delete")

    def set_password(self, input):
        self.password_hash = generate_password_hash(input)

    def check_password(self, input):
        return check_password_hash(self.password_hash, input)

    @staticmethod
    def verify_email(email):
        """Validate email format"""
        email_regex =  r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")

    @staticmethod
    def verify_password(password):
        """Validate password criteria"""
        if len(password) < 6:
            raise ValueError("Given password too short")
        
    @classmethod
    def get_all_emails(cls):
        return cls.query.with_entities(cls.email, cls.created_at).all()
    
    @classmethod
    def get_all_users(cls):
        return cls.query.all()
    
    @classmethod
    def get_user(cls, email):
        return cls.query.filter_by(email=email).first()
    
        
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at
        }
    
    def __repr__(self):
        return f"User {self.email}"


channel_brand = db.Table(
    "channel_brand",
    db.Column("channel_id", db.Integer, db.ForeignKey("channels.id"), primary_key=True),
    db.Column("brand_id", db.Integer, db.ForeignKey("brands.id"), primary_key=True),
)

# Association table for many-to-many relationship between Channels and Sizes
channel_size = db.Table(
    "channel_size",
    db.Column("channel_id", db.Integer, db.ForeignKey("channels.id"), primary_key=True),
    db.Column("size_id", db.Integer, db.ForeignKey("sizes.id"), primary_key=True),
)

class Brand(db.Model):
    __tablename__ = "brands"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    channels = db.relationship(
        "Channel", secondary=channel_brand, back_populates="brands"
)

    def __repr__(self):
        return f"Brand {self.name}"
    
class Size(db.Model):
    __tablename__ = "sizes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    channels = db.relationship(
        "Channel", secondary=channel_size, back_populates="sizes"
    )

    def __repr__(self):
        return f"Size {self.name}"
    
class MainCategory(db.Model):
    __tablename__ = 'main_categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    gender = db.Column(db.String(10), nullable=False)  # boys, girls, unisex
    subcategories = db.relationship('SubCategory', backref='main_category', lazy=True)

    def __repr__(self):
        return f"<MainCategory {self.name}, Gender: {self.gender}>"
    
class SubCategory(db.Model):
    __tablename__ = 'subcategories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # boys, girls, unisex
    main_category_id = db.Column(db.Integer, db.ForeignKey('main_categories.id'), nullable=False)

    def __repr__(self):
        return f"<SubCategory {self.name}, Gender: {self.gender}>"

class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)  # Mandatory and unique
    query_identifier = db.Column(db.Integer, nullable=False, unique=True)  # Identifier for frontend params
    search = db.Column(db.Text, nullable=True)  # Optional search query
    min_price = db.Column(db.Integer, nullable=True)  # Optional minimum price
    max_price = db.Column(db.Integer, nullable=True)  # Optional maximum price
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)  # Optional user association
    user = db.relationship('User', back_populates='channels', lazy='joined')  # Optimize queries
    sizes = db.relationship('Size', secondary=channel_size, back_populates='channels')
    brands = db.relationship('Brand', secondary=channel_brand, back_populates='channels')
    main_category_id = db.Column(db.Integer, db.ForeignKey('main_categories.id'), nullable=True, index=True)  # Optional main category
    main_category = db.relationship('MainCategory', backref=db.backref("channels", lazy='dynamic'))
    sub_category_id = db.Column(db.Integer, db.ForeignKey("subcategories.id"), nullable=True, index=True)  # Optional subcategory
    sub_category = db.relationship('SubCategory', backref=db.backref("channels", lazy='dynamic'))


    @classmethod
    def get_all_channels(cls):
        try:
            channels = cls.query.all()
            return channels
        except Exception as e:
            print("Error when retrieving all channels", e)
            return []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "query_identifier": self.query_identifier,
            "search": self.search if self.search else None,
            "min_price": self.min_price if self.min_price else None,
            "max_price": self.max_price if self.max_price else None,
            "user_id": self.user_id,
            "brands": [brand.name for brand in self.brands] if self.brands else [],
            "sizes": [size.name for size in self.sizes] if self.sizes else [],
            "main_category": self.main_category.name if self.main_category else None,
            "sub_category": self.sub_category.name if self.sub_category else None
        }
    
    def __repr__(self):
        return f"Channel: {self.name}"
