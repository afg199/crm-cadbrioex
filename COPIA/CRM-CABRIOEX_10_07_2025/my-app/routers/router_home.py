from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error
import subprocess
import os
from werkzeug.utils import secure_filename

# Importando cenexión a BD
from controllers.funciones_home import *

PATH_URL = "public/empleados"

# Nueva ruta para importar datos desde el CSV
@app.route('/importar-datos-csv', methods=['POST'])
def importar_datos_csv():
    if 'conectado' in session:
        if 'archivo_csv' not in request.files:
            flash('No se ha seleccionado ningún archivo', 'error')
            return redirect(url_for('lista_empleados'))

        file = request.files['archivo_csv']

        if file.filename == '':
            flash('No se ha seleccionado ningún archivo', 'error')
            return redirect(url_for('lista_empleados'))

        if file and file.filename.endswith('.csv'):
            try:
                # Guardar el archivo temporalmente
                filename = secure_filename(file.filename)
                temp_path = os.path.join('my-app/datos excel', filename)
                file.save(temp_path)

                # Ruta al script import_excel.py
                script_path = './my-app/datos excel/import_excel.py'
                
                # Ejecutar el script de importación con la ruta del archivo temporal
                result = subprocess.run(['python3', script_path, temp_path], capture_output=True, text=True, check=True)
                
                flash('Datos importados desde el CSV correctamente.', 'success')
                print("Salida del script import_excel.py:", result.stdout)
                if result.stderr:
                    print("Errores del script import_excel.py:", result.stderr)

            except subprocess.CalledProcessError as e:
                flash(f'Error al importar datos desde el CSV: {e.stderr}', 'error')
                print("Error al ejecutar el script:", e.stderr)
            except Exception as e:
                flash(f'Ocurrió un error inesperado: {e}', 'error')
            finally:
                # Eliminar el archivo temporal
                if os.path.exists(temp_path):
                    os.remove(temp_path)

            return redirect(url_for('lista_empleados'))
        else:
            flash('Por favor, suba un archivo con formato .csv', 'warning')
            return redirect(url_for('lista_empleados'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

#Activa pagina Registrar CLIENTE
@app.route('/registrar-empleado', methods=['GET'])
def viewFormEmpleado():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

#Registrar CLIENTE
@app.route('/form-registrar-empleado', methods=['POST'])
def formEmpleado():
    if 'conectado' in session:
        resultado = procesar_form_empleado(request.form)
        if resultado:
            return redirect(url_for('lista_empleados'))
        else:
            flash('El empleado NO fue registrado.', 'error')
            return render_template(f'{PATH_URL}/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

#Activa pagina Registrar EQUIPO de un cliente
@app.route('/registrar-equipo/<int:id_cliente>/<nombre>/<apellido>', methods=['GET'])
def viewFormEquipo(id_cliente, nombre, apellido):
    # Aquí recibes el id del empleado y puedes usarlo en el formulario
    return render_template(f'{PATH_URL}/form_equipo.html', id_cliente=id_cliente, nombre=nombre, apellido=apellido)

#Registrar EQUIPO de un cliente
@app.route('/form-registrar-equipo', methods=['POST'])
def formEquipo():
    if 'conectado' in session:
        resultado = procesar_form_equipo(request.form)
        id_Clientes = request.form['id_cliente']  # <-- obtienes el id del formulario
        if resultado:
            detalle_empleado = sql_detalles_empleadosBD(id_Clientes)
            equipos_cliente=sql_lista_equipo_clienteBD(id_Clientes)
            return render_template(f'{PATH_URL}/detalles_empleado.html', detalle_empleado=detalle_empleado, equipos_cliente=equipos_cliente)
        else:
            flash('El equipo NO fue registrado.', 'error')
            return redirect(url_for('inicio'))    
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

#Activa pagina Registrar de SERVICIO de un cliente
@app.route('/registrar-servicio/<int:id_equipo>', methods=['GET'])
def viewFormServicio(id_equipo):
    # Aquí recibes el id del empleado y puedes usarlo en el formulario
    return render_template(f'{PATH_URL}/form_servicio.html', id_equipo=id_equipo)

#Registrar SERVICIO de un cliente
@app.route('/form-registrar-servicio', methods=['POST'])
def formServicio():
    if 'conectado' in session:
        resultado = procesar_form_servicio(request.form)
        id_Equipos = request.form['id_equipo']  # <-- obtienes el id del formulario
        if resultado:
            detalle_equipo = sql_detalles_equipoBD(id_Equipos)
            servcios_equipo=sql_lista_equipo_servicioBD(id_Equipos)
            return render_template(f'{PATH_URL}/detalles_equipo.html', detalle_equipo=detalle_equipo, servcios_equipo=servcios_equipo)
        else:
            flash('El servicio NO fue registrado.', 'error')
            return redirect(url_for('inicio'))    
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Lista de clientes
@app.route('/lista-de-empleados', methods=['GET'])
def lista_empleados():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_empleados.html', empleados=sql_lista_empleadosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Detalles de un CLIENTE
@app.route("/detalles-empleado/", methods=['GET'])
@app.route("/detalles-empleado/<int:idEmpleado>", methods=['GET'])
def detalleEmpleado(idEmpleado=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idEmpleado es None o no está presente en la URL
        if idEmpleado is None:
            return redirect(url_for('inicio'))
        else:
            detalle_empleado = sql_detalles_empleadosBD(idEmpleado)
            equipos_cliente=sql_lista_equipo_clienteBD(idEmpleado)
            return render_template(f'{PATH_URL}/detalles_empleado.html', detalle_empleado=detalle_empleado, equipos_cliente=equipos_cliente)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Detalles de un EQUIPO 
@app.route("/detalles-equipo/", methods=['GET'])
@app.route("/detalles-equipo/<int:idEquipo>", methods=['GET'])
def detalleEquipo(idEquipo=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idEquipo es None o no está presente en la URL
        if idEquipo is None:
            return redirect(url_for('inicio'))
        else:
            detalle_equipo = sql_detalles_equipoBD(idEquipo)
            servcios_equipo=sql_lista_equipo_servicioBD(idEquipo)
            return render_template(f'{PATH_URL}/detalles_equipo.html', detalle_equipo=detalle_equipo, servcios_equipo=servcios_equipo)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Detalles de un SERVICIO 
@app.route("/detalles-servicio/", methods=['GET'])
@app.route("/detalles-servicio/<int:idServicio>", methods=['GET'])
def detalleServicio(idServicio=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idServicio es None o no está presente en la URL
        if idServicio is None:
            return redirect(url_for('inicio'))
        else:
            detalle_servicio = sql_detalles_servicioBD(idServicio)
            return render_template(f'{PATH_URL}/detalles_servicio.html', detalle_servicio=detalle_servicio)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Buscadon de empleados
@app.route("/buscando-empleado", methods=['POST'])
def viewBuscarEmpleadoBD():
    resultadoBusqueda = buscarEmpleadoBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_empleado.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})

# Editar CLIENTE
@app.route("/editar-cliente/<int:id>", methods=['GET'])
def viewEditarCliente(id):
    if 'conectado' in session:
        respuestaCliente = buscarClienteUnico(id)
        if respuestaCliente:
            return render_template(f'{PATH_URL}/form_cliente_update.html', respuestaCliente=respuestaCliente)
        else:
            flash('El cliente no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Recibir formulario para actulizar informacion de CLIENTE
@app.route('/actualizar-cliente', methods=['POST'])
def actualizarCliente():
    resultData = procesar_actualizacion_form_cliente(request)
    id_Clientes = request.form['id_Clientes']  # <-- obtienes el id del formulario
    if resultData:
        detalle_empleado = sql_detalles_empleadosBD(id_Clientes)
        equipos_cliente=sql_lista_equipo_clienteBD(id_Clientes)
        return render_template(f'{PATH_URL}/detalles_empleado.html', detalle_empleado=detalle_empleado, equipos_cliente=equipos_cliente)

# Editar EQUIPO
@app.route("/editar-equipo/<int:id>", methods=['GET'])
def viewEditarEquipo(id):
    if 'conectado' in session:
        respuestaEquipo = buscarEquipoUnico(id)
        if respuestaEquipo:
            return render_template(f'{PATH_URL}/form_equipo_update.html', respuestaEquipo=respuestaEquipo)
        else:
            flash('El equipo no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Recibir formulario para actulizar informacion de EQUIPO
@app.route('/actualizar-equipo', methods=['POST'])
def actualizarEquipo():
    resultDataEquipo = procesar_actualizacion_form_equipo(request)
    id_Equipos = request.form['id_Equipos']  # <-- obtienes el id del formulario
    if resultDataEquipo:
        detalle_equipo = sql_detalles_equipoBD(id_Equipos)
        servcios_equipo=sql_lista_equipo_servicioBD(id_Equipos)
        return render_template(f'{PATH_URL}/detalles_equipo.html', detalle_equipo=detalle_equipo, servcios_equipo=servcios_equipo)
    
# Editar SERVICIO
@app.route("/editar-servicio/<int:id>", methods=['GET'])
def viewEditarServicio(id):
    if 'conectado' in session:
        respuestaServicio = buscarServicioUnico(id)
        if respuestaServicio:
            return render_template(f'{PATH_URL}/form_servicio_update.html', respuestaServicio=respuestaServicio)
        else:
            flash('El servicio no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Recibir formulario para actulizar informacion de SERVICIO
@app.route('/actualizar-servicio', methods=['POST'])
def actualizarServicio():
    resultDataServicio = procesar_actualizacion_form_servicio(request)
    id_servicio = request.form['id_Servicios']  # <-- obtienes el id del formulario
    if resultDataServicio:
        detalle_servicio = sql_detalles_servicioBD(id_servicio)
        return render_template(f'{PATH_URL}/detalles_servicio.html', detalle_servicio=detalle_servicio)


@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('inicioCpanel'))


@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))

# Eliminar CLIENTE
@app.route('/borrar-empleado/<string:id_Clientes>', methods=['GET'])
def borrarEmpleado(id_Clientes):
    resp = eliminarEmpleado(id_Clientes)
    if resp:
        flash('El Cliente fue eliminado correctamente', 'success')
        return redirect(url_for('lista_empleados'))

# Eliminar EQUIPO
@app.route('/borrar-equipo/<string:id_Equipos>/<string:id_Clientes>', methods=['GET'])
def borrarEquipo(id_Equipos,id_Clientes):
    resp = eliminarEquipo(id_Equipos)
    if resp:
        flash('El Equipo fue eliminado correctamente', 'success')
        detalle_empleado = sql_detalles_empleadosBD(id_Clientes)
        equipos_cliente=sql_lista_equipo_clienteBD(id_Clientes)
        return render_template(f'{PATH_URL}/detalles_empleado.html', detalle_empleado=detalle_empleado, equipos_cliente=equipos_cliente)

# Eliminar SERVICIO
@app.route('/borrar-servicio/<string:id_Servicios>/<string:id_Equipos>', methods=['GET'])
def borrarServicio(id_Servicios,id_Equipos):
    resp = eliminarServicio(id_Servicios)
    if resp:
        flash('El Servicio fue eliminado correctamente', 'success')
        detalle_equipo = sql_detalles_equipoBD(id_Equipos)
        servcios_equipo=sql_lista_equipo_servicioBD(id_Equipos)
        return render_template(f'{PATH_URL}/detalles_equipo.html', detalle_equipo=detalle_equipo, servcios_equipo=servcios_equipo)

@app.route("/descargar-informe-empleados/", methods=['GET'])
def reporteBD():
    if 'conectado' in session:
        return generarReporteExcel()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

