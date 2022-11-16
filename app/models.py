from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150))
	user = db.Column(db.String(150))
	email = db.Column(db.String(150), unique=True)
	password = db.Column(db.String(150))
	avatar = db.Column(db.String(200))
	role = db.Column(db.Integer)

class Empresas(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	empresa = db.Column(db.String(200), unique=True)

class Servicios(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(200), unique=True)

class Pagos(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	servicio = db.Column(db.String(200))
	fecha_venc = db.Column(db.String(15))
	empresa = db.Column(db.String(200))
	fecha_pago = db.Column(db.String(15))
	importe = db.Column(db.Float)
	comprobante = db.Column(db.String(200))
	id_user = db.Column(db.Integer)
