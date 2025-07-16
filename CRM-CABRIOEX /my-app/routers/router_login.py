from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash
from conexion.conexionBD import connectionBD
from controllers.funciones_login import dataLoginSesion, info_perfil_session, recibeInsertRegisterUser, procesar_update_perfil

# Creación de un Blueprint para el login
login_bp = Blueprint('login_bp', __name__, template_folder='templates', static_folder='static')

PATH_URL_LOGIN = "public/login"


@login_bp.route('/')
def inicio():
    if 'conectado' in session:
        return render_template('public/base_cpanel.html', dataLogin=dataLoginSesion())
    else:
        return render_template(f'{PATH_URL_LOGIN}/base_login.html')


@login_bp.route('/mi-perfil')
def perfil():
    if 'conectado' in session:
        return render_template(f'public/perfil/perfil.html', info_perfil_session=info_perfil_session())
    else:
        return redirect(url_for('login_bp.inicio'))


@login_bp.route('/register-user')
def cpanelRegisterUser():
    if 'conectado' in session:
        return redirect(url_for('login_bp.inicio'))
    else:
        return render_template(f'{PATH_URL_LOGIN}/auth_register.html')


@login_bp.route('/recovery-password')
def cpanelRecoveryPassUser():
    if 'conectado' in session:
        return redirect(url_for('login_bp.inicio'))
    else:
        return render_template(f'{PATH_URL_LOGIN}/auth_forgot_password.html')


@login_bp.route('/saved-register', methods=['POST'])
def cpanelResgisterUserBD():
    if request.method == 'POST' and 'name_surname' in request.form and 'pass_user' in request.form:
        name_surname = request.form['name_surname']
        email_user = request.form['email_user']
        pass_user = request.form['pass_user']

        resultData = recibeInsertRegisterUser(
            name_surname, email_user, pass_user)
        if (resultData != 0):
            flash('la cuenta fue creada correctamente.', 'success')
            return redirect(url_for('login_bp.inicio'))
        else:
            return redirect(url_for('login_bp.inicio'))
    else:
        flash('el método HTTP es incorrecto', 'error')
        return redirect(url_for('login_bp.inicio'))


@login_bp.route("/actualizar-datos-perfil", methods=['POST'])
def actualizarPerfil():
    if request.method == 'POST':
        if 'conectado' in session:
            respuesta = procesar_update_perfil(request.form)
            if respuesta == 1:
                flash('Los datos fuerón actualizados correctamente.', 'success')
                return redirect(url_for('login_bp.inicio'))
            elif respuesta == 0:
                flash(
                    'La contraseña actual esta incorrecta, por favor verifique.', 'error')
                return redirect(url_for('login_bp.perfil'))
            elif respuesta == 2:
                flash('Ambas claves deben se igual, por favor verifique.', 'error')
                return redirect(url_for('login_bp.perfil'))
            elif respuesta == 3:
                flash('La Clave actual es obligatoria.', 'error')
                return redirect(url_for('login_bp.perfil'))
        else:
            flash('primero debes iniciar sesión.', 'error')
            return redirect(url_for('login_bp.inicio'))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('login_bp.inicio'))


@login_bp.route('/login', methods=['POST'])
def loginCliente():
    if 'conectado' in session:
        return redirect(url_for('login_bp.inicio'))
    else:
        if request.method == 'POST' and 'email_user' in request.form and 'pass_user' in request.form:

            email_user = str(request.form['email_user'])
            pass_user = str(request.form['pass_user'])

            conexion_MySQLdb = connectionBD()
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE email_user = %s", [email_user])
            account = cursor.fetchone()

            if account:
                if check_password_hash(account['pass_user'], pass_user):
                    session['conectado'] = True
                    session['id'] = account['id']
                    session['name_surname'] = account['name_surname']
                    session['email_user'] = account['email_user']

                    flash('la sesión fue correcta.', 'success')
                    return redirect(url_for('login_bp.inicio'))
                else:
                    flash('datos incorrectos por favor revise.', 'error')
                    return render_template(f'{PATH_URL_LOGIN}/base_login.html')
            else:
                flash('el usuario no existe, por favor verifique.', 'error')
                return render_template(f'{PATH_URL_LOGIN}/base_login.html')
        else:
            flash('primero debes iniciar sesión.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')


@login_bp.route('/closed-session')
def cerraSesion():
    if 'conectado' in session:
        session.pop('conectado', None)
        session.pop('id', None)
        session.pop('name_surname', None)
        session.pop('email', None)
        flash('tu sesión fue cerrada correctamente.', 'success')
        return redirect(url_for('login_bp.inicio'))
    else:
        flash('recuerde debe iniciar sesión.', 'error')
        return render_template(f'{PATH_URL_LOGIN}/base_login.html')
