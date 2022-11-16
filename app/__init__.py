from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_user, login_required, logout_user, current_user




db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'cuentas'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
	db.init_app(app)


	from .views import views
	from .auth import auth

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')

	from .models import User, Servicios, Empresas, Pagos

	create_database(app)

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)



	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))


	return app



def create_database(app):
	if not path.exists('app/' + DB_NAME):
		with app.app_context():
			db.create_all()
			print('Database Created Successfully!')


