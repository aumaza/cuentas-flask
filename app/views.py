from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from markupsafe import escape
from os.path import join, dirname, realpath
import imghdr
import os
from . import db
import json
import datetime
import shutil




views = Blueprint('views', '__name__')
from .models import User, Empresas, Servicios, Pagos


@views.route('/')
@login_required
def home():
	return render_template('index.html', user=current_user)


@views.route('/main')
@login_required
def main():
	return render_template('main.html', user=current_user)



# ==========================================================
# VISTAS DE TABLAS
# ==========================================================


@views.route('/usuarios')
@login_required
def usuarios():
	users = User.query
	count = User.query.count()
	return render_template('users.html', users=users, count=count, user=current_user)

@views.route('/empresas')
@login_required
def empresas():
	companies = Empresas.query
	count = Empresas.query.count()
	return render_template('companies.html', companies=companies, count=count, user=current_user)

@views.route('/servicios')
@login_required
def servicios():
	services = Servicios.query
	count = Servicios.query.count()
	print(services)
	return render_template('service.html', services=services, count=count, user=current_user)

@views.route('/pagos/<int:id>')
@login_required
def pagos(id):
	pays = Pagos.query.filter_by(id_user=id)
	count = Pagos.query.filter_by(id_user=id).count()
	return render_template('payments.html', pays=pays, count=count, user=current_user)


# ==========================================================
# FORMULARIOS DE CARGA DE DATOS
# ==========================================================

@views.route('/agregar_servicio', methods=['GET', 'POST'])
@login_required
def add_service():
	if request.method == 'POST':
		service = request.form.get('service')

		descripcion = Servicios.query.filter_by(descripcion=service).first()

		if descripcion:
			flash('Servicio Existente!', category='error')
		elif len(service) == 0:
			flash('Debe ingresar el Servicio!', category='error')
		else:
			new_service = Servicios(descripcion=service)
			db.session.add(new_service)
			db.session.commit()
			#login_user(user, remember=True)
			flash('Servicio guardado satisfactoriamente!', category='success')
			return redirect(url_for('views.servicios'))

	return render_template('add_service.html', user=current_user)


@views.route('/agregar_empresa', methods=['GET', 'POST'])
@login_required
def add_companie():
	if request.method == 'POST':
		companie = request.form.get('companie')

		empresa = Empresas.query.filter_by(empresa=companie).first()

		if empresa:
			flash('Empresa Existente!', category='error')
		elif len(companie) == 0:
			flash('Debe ingresar una empresa', category='error')
		else:
			new_empresa = Empresas(empresa=companie)
			db.session.add(new_empresa)
			db.session.commit()
			flash('Empresa Agregada Exitosamente!', category='success')
			return redirect(url_for('views.empresas'))

	return render_template('add_companie.html', user=current_user)


@views.route('/agregar_pago/<int:id>', methods=['GET', 'POST'])
@login_required
def add_payment(id):
	usr = User.query.get_or_404(id)

	if request.method == 'POST':
		service = request.form.get('service')
		companie = request.form.get('companie')
		f_venc = request.form.get('fecha_venc')
		f_pay = request.form.get('fecha_pago')
		payment = request.form.get('importe')

		print(service)
		print(companie)
		print(f_venc)
		print(f_pay)
		print(payment)

		if len(service) == 0 or len(companie) == 0 or len(f_venc) == 0 or len(f_pay) == 0 or len(payment) == 0:
			flash('Hay campos sin completar', category='error')
		else:
			new_payment = Pagos(servicio=service, fecha_venc=f_venc, empresa=companie, fecha_pago=f_pay, importe=payment, id_user=usr.id)
			db.session.add(new_payment)
			db.session.commit()
			flash('Pago Agregado Exitosamente!', category='success')
			return redirect(url_for('views.pagos'))



	servicios = Servicios.query.order_by(Servicios.descripcion.asc())
	empresas = Empresas.query.order_by(Empresas.empresa.asc())
	return render_template('add_payment.html', services=servicios, companies=empresas, user=current_user)


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


@views.route('/avatar/<int:id>', methods=['GET', 'POST'])
@login_required
def load_picture(id):
	usr = User.query.get_or_404(id)
	allow_types = ['.jpg', '.png', '.svg', '.gif']
	UPLOADS_PATH = 'app/static/uploads/'
		
	if request.method == 'POST':
		uploaded_file = request.files['file']
		filename = secure_filename(uploaded_file.filename)
		
		if filename != '':
			file_ext = os.path.splitext(filename)[1]
			if file_ext not in allow_types or \
					file_ext != validate_image(uploaded_file.stream):
				flash('El tipo de archivo debe ser JPG, PNG, SVG o GIF!', category='error')
			uploaded_file.save(UPLOADS_PATH+filename)
			
			usr.avatar = filename
			db.session.add(usr)
			db.session.commit()
			flash('Imagen Subida Exitosamente!', category='success')
		return redirect(url_for('views.main'))

	return render_template('avatar.html', user=current_user)


@views.route('add_ticket/<int:id>', methods=['GET', 'POST'])
@login_required
def add_ticket(id):
	payment = Pagos.query.get_or_404(id)
	allow_types = '.pdf'
	UPLOADS_PATH = 'app/static/tickets/'

	if request.method == 'POST':
		uploaded_file = request.files['file']
		filename = secure_filename(uploaded_file.filename)

		if filename != '':
			file_ext = os.path.splitext(filename)[1]
			print(file_ext)
			if file_ext not in allow_types:
				flash('El tipo de archivo debe ser PDF!', category='error')
			uploaded_file.save(UPLOADS_PATH+filename)

			payment.comprobante = filename
			db.session.add(payment)
			db.session.commit()
			flash('Comprobante Cargado Exitosamente!', category='success')
		return redirect(url_for('views.main'))

	return render_template('ticket.html', payment=payment, user=current_user)


@views.route('/open_ticket/<path:comprobante>', methods=['GET', 'POST'])
@login_required
def open_ticket(comprobante):
	dirname = 'app/static/tickets/'
	return redirect(url_for('static', filename='tickets/' + comprobante), code=301)


@views.route('/info_extended/<int:id>', methods=['GET', 'POST'])
@login_required
def info_extended(id):
	payment = Pagos.query.get_or_404(id)
	return render_template('info_extended.html', payment=payment, user=current_user)


# ==========================================================
# FORMULARIOS DE EDICION DE DATOS
# ==========================================================

@views.route('/update_service/<int:id>', methods=['GET', 'POST'])
@login_required
def update_service(id):
	service = Servicios.query.get_or_404(id)

	if request.method == 'POST':
		descripcion = request.form.get('service')

		if len(descripcion) == 0:
			flash('Debe ingresar una Descripción para el Servicio', category='error')
		else:
			service.descripcion = descripcion
			db.session.add(service)
			db.session.commit()
			flash('Registro Actualizado!', category='success')
			return redirect(url_for('views.servicios'))

	
	return render_template('update_service.html', service=service, user=current_user)


@views.route('/update_companie/<int:id>', methods=['GET', 'POST'])
@login_required
def update_companie(id):
	companie = Empresas.query.get_or_404(id)

	if request.method == 'POST':
		empresa = request.form.get('companie')

		if len(empresa) == 0:
			flash('Debe ingresar una Compañia!', category='error')
		else:
			companie.empresa = empresa
			db.session.add(companie)
			db.session.commit()
			flash('Registro Actualizado!', category='success')
			return redirect(url_for('views.empresas'))

	return render_template('update_companie.html', companie=companie, user=current_user)



@views.route('/update_payment/<int:id>', methods=['GET', 'POST'])
@login_required
def update_payment(id):
	services = Servicios.query
	companies = Empresas.query
	payment = Pagos.query.get_or_404(id)

	if request.method == 'POST':
		service = request.form.get('service')
		companie = request.form.get('companie')
		f_venc = request.form.get('fecha_venc')
		f_pay = request.form.get('fecha_pago')
		pay = request.form.get('importe')

		print('Servicio: ', service)
		print('Empresa: ', companie)
		print('Fecha Venc.: ', f_venc)
		print('Fecha Pago: ', f_pay)
		print('Importe: $', pay)

		if len(service) == 0 or len(companie) == 0 or len(f_venc) == 0 or len(f_pay) == 0 or len(pay) == 0:
			flash('Hay campos sin completar', category='error')
		else:
			payment.servicio = service
			payment.empresa = companie
			payment.fecha_venc = f_venc
			payment.fecha_pago = f_pay
			payment.importe = pay
			db.session.add(payment)
			db.session.commit()
			flash('Pago Actualizado Exitosamente!', category='success')
			return redirect(url_for('views.pagos'))


	return render_template('update_payment.html', services=services, companies=companies, payment=payment, user=current_user)


@views.route('/change_password/<int:id>', methods=['GET', 'POST'])
@login_required
def change_password(id):
	usr = User.query.get_or_404(id)

	if request.method == 'POST':
		password_1 = request.form.get('password_1')
		password_2 = request.form.get('password_2')

		if len(password_1) == 0 or len(password_2) == 0:
			flash('Debe Ingresar los passwords!', category='error')
		elif len(password_1) < 8 or len(password_2) < 8:
			flash('Los passwords no pueden tener menos de 8 caracteres!', category='error')
		elif password_1 != password_2:
			flash('Los passwords no coinciden!', category='error')
		else:
			usr.password = generate_password_hash(password_1, method='sha256')
			db.session.add(usr)
			db.session.commit()
			flash('El Password ha sido actualizado Exitosamente!', category='success')
			return redirect(url_for('auth.logout'))


	return render_template('change_password.html', user=current_user)


@views.route('/user_bio/<int:id>', methods=['GET', 'POST'])
@login_required
def user_bio(id):
	usr = User.query.get_or_404(id)

	if request.method == 'POST':
		name = request.form.get('name')
		email = request.form.get('email')

		if len(name) == 0 or len(email) == 0:
			flash('Debe completar los campos!', category='error')
		elif name == usr.name and email == usr.email:
			flash('Los datos no serán modificados. Ambos son iguales a los ya registrados!', category='error')
		else:
			usr.name = name
			usr.user = email
			usr.email = email
			db.session.add(usr)
			db.session.commit()
			flash('Los datos han sido modificados exitosamente', category='success')
			return redirect(url_for('auth.logout'))

	return render_template('user_bio.html', usr=usr, user=current_user)



# ==========================================================
# FORMULARIOS DE ELIMINACION DE DATOS
# ==========================================================

@views.route('/delete_payment/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_payment(id):
	payment = Pagos.query.get_or_404(id)

	if request.method == 'POST':
		accept = request.form.get('pay_delete')
		db.session.delete(payment)
		db.session.commit()
		flash('Registro Eliminado!', category='success')
		return redirect(url_for('views.pagos'))


	return render_template('delete_payment.html', payment=payment, user=current_user)
