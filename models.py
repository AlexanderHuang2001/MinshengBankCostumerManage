from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.String, unique=True, nullable=False)
    mobile = db.Column(db.String, unique=True, nullable=False)
    real_name = db.Column(db.String, nullable=False)
    province = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    login_ip = db.Column(db.String, nullable=False)
    login_time = db.Column(db.String, nullable=False)
    enabled = db.Column(db.Integer, nullable=False)
    vip_level = db.Column(db.Integer, nullable=False)
    push_ratio = db.Column(db.Float, nullable=True)  # 允许为NULL
    send_num = db.Column(db.Integer, nullable=True)  # 允许为NULL
    risk_ratio = db.Column(db.Float, nullable=True)  # 允许为NULL