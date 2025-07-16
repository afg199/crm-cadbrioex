from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from mysql.connector.errors import Error
import subprocess
import os
from werkzeug.utils import secure_filename

# Importando conexión a BD
from controllers.funciones_home import (
    procesar_form_empleado,
    procesar_form_equipo,
    procesar_form_servicio,
    sql_lista_empleadosBD,
    sql_detalles_empleadosBD,
    sql_lista_equipo_clienteBD,
    sql_detalles_equipoBD,
    sql_lista_equipo_servicioBD,
    sql_detalles_servicioBD,
    buscarEmpleadoBD,
    buscarClienteUnico,
    procesar_actualizacion_form_cliente,
    buscarEquipoUnico,
    procesar_actualizacion_form_equipo,
    buscarServicioUnico,
    procesar_actualizacion_form_servicio,
    lista_usuariosBD,
    eliminarUsuario,
    eliminarEmpleado,
    eliminarEquipo,
    eliminarServicio,
    generarReporteExcel,
    obtener_estadisticas_dashboard,
   
    # NUEVAS FUNCIONES PARA DASHBOARD REDISEÑADO
    obtener_datos_marcas,
    obtener_datos_garantias,
    obtener_clientes_por_poblacion,
    obtener_servicios_por_tipo,
    obtener_todas_poblaciones
)

home_bp = Blueprint('home_bp', __name__, template_folder='templates', url_prefix='/')

PATH_URL = "public/empleados"

# Nueva ruta para importar datos desde el CSV
@home_bp.route('/importar-datos-csv', methods=['POST'])
def importar_datos_csv():
    if 'conectado' in session:
        if 'archivo_csv' not in request.files:
            flash('No se ha seleccionado ningún archivo', 'error')
            return redirect(url_for('home_bp.lista_empleados'))

        file = request.files['archivo_csv']

        if file.filename == '':
            flash('No se ha seleccionado ningún archivo', 'error')
            return redirect(url_for('home_bp.lista_empleados'))

        if file and file.filename.endswith('.csv'):
            try:
                # RUTAS ABSOLUTAS FIJAS - NO FALLAN
                base_path = "/Users/angelfernandez/Desktop/MIS PROYECTOS/CADBRIOEX/CRM-CABRIOEX/my-app"
                datos_excel_dir = os.path.join(base_path, "datos excel")
                
                # Verificar que el directorio existe
                if not os.path.exists(datos_excel_dir):
                    flash(f'Error: No existe el directorio {datos_excel_dir}', 'error')
                    return redirect(url_for('home_bp.lista_empleados'))
                
                # Guardar archivo temporal
                filename = secure_filename(file.filename)
                temp_path = os.path.join(datos_excel_dir, filename)
                
                print(f"DEBUG: Guardando archivo en: {temp_path}")
                file.save(temp_path)
                
                # Verificar que el archivo se guardó
                if not os.path.exists(temp_path):
                    flash(f'Error: No se pudo guardar el archivo en {temp_path}', 'error')
                    return redirect(url_for('home_bp.lista_empleados'))

                # Ruta al script
                script_path = os.path.join(datos_excel_dir, 'import_excel.py')
                
                print(f"DEBUG: Script ubicado en: {script_path}")
                print(f"DEBUG: Archivo CSV en: {temp_path}")
                
                # Verificar que el script existe
                if not os.path.exists(script_path):
                    flash(f'Error: No se encuentra el script en {script_path}', 'error')
                    return redirect(url_for('home_bp.lista_empleados'))
                
                # Ejecutar el script
                result = subprocess.run(
                    ['python3', script_path, temp_path], 
                    capture_output=True, 
                    text=True, 
                    check=True,
                    cwd=base_path  # Ejecutar desde el directorio base
                )
                
                flash('Datos importados desde el CSV correctamente.', 'success')
                print("✅ Salida del script:", result.stdout)
                if result.stderr:
                    print("⚠️ Errores del script:", result.stderr)

            except subprocess.CalledProcessError as e:
                error_msg = e.stderr if e.stderr else str(e)
                flash(f'Error al ejecutar el script: {error_msg}', 'error')
                print(f"❌ Error subprocess: {error_msg}")
            except Exception as e:
                flash(f'Error inesperado: {str(e)}', 'error')
                print(f"❌ Error general: {str(e)}")
            finally:
                # Limpiar archivo temporal
                if 'temp_path' in locals() and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                        print(f"🗑️ Archivo temporal eliminado: {temp_path}")
                    except Exception as e:
                        print(f"⚠️ No se pudo eliminar archivo temporal: {e}")

            return redirect(url_for('home_bp.lista_empleados'))
        else:
            flash('Por favor, suba un archivo con formato .csv', 'warning')
            return redirect(url_for('home_bp.lista_empleados'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('login_bp.inicio'))

#Activa pagina Registrar CLIENTE
@home_bp.route('/registrar-empleado', methods=['GET'])
def viewFormEmpleado():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('login_bp.inicio'))

#Registrar CLIENTE
@home_bp.route('/form-registrar-empleado', methods=['POST'])
def formEmpleado():
    if 'conectado' in session:
        resultado = procesar_form_empleado(request.form)
        if resultado:
            return redirect(url_for('home_bp.lista_empleados'))
        else:
            flash('El empleado NO fue registrado.', 'error')
            return render_template(f'{PATH_URL}/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('login_bp.inicio'))

#Activa pagina Registrar EQUIPO de un cliente
@home_bp.route('/registrar-equipo/<int:id_cliente>/<nombre>/<apellido>', methods=['GET'])
def viewFormEquipo(id_cliente, nombre, apellido):
    # Aquí recibes el id del empleado y puedes usarlo en el formulario
    return render_template(f'{PATH_URL}/form_equipo.html', id_cliente=id_cliente, nombre=nombre, apellido=apellido)

#Registrar EQUIPO de un cliente
@home_bp.route('/form-registrar-equipo', methods=['POST'])
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
            return redirect(url_for('login_bp.inicio'))    
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('login_bp.inicio'))

#Activa pagina Registrar de SERVICIO de un cliente
@home_bp.route('/registrar-servicio/<int:id_equipo>', methods=['GET'])
def viewFormServicio(id_equipo):
    # Aquí recibes el id del empleado y puedes usarlo en el formulario
    return render_template(f'{PATH_URL}/form_servicio.html', id_equipo=id_equipo)

#Registrar SERVICIO de un cliente
@home_bp.route('/form-registrar-servicio', methods=['POST'])
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
            return redirect(url_for('login_bp.inicio'))    
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('login_bp.inicio'))

# Lista de clientes
@home_bp.route('/lista-de-empleados', methods=['GET'])
def lista_empleados():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_empleados.html', empleados=sql_lista_empleadosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('login_bp.inicio'))

# Detalles de un CLIENTE
@home_bp.route("/detalles-empleado/", methods=['GET'])
@home_bp.route("/detalles-empleado/<int:idEmpleado>", methods=['GET'])
def detalleEmpleado(idEmpleado=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idEmpleado es None o no está presente en la URL
        if idEmpleado is None:
            return redirect(url_for('login_bp.inicio'))
        else:
            detalle_empleado = sql_detalles_empleadosBD(idEmpleado)
            equipos_cliente=sql_lista_equipo_clienteBD(idEmpleado)
            return render_template(f'{PATH_URL}/detalles_empleado.html', detalle_empleado=detalle_empleado, equipos_cliente=equipos_cliente)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('login_bp.inicio'))

# Detalles de un EQUIPO 
@home_bp.route("/detalles-equipo/", methods=['GET'])
@home_bp.route("/detalles-equipo/<int:idEquipo>", methods=['GET'])
def detalleEquipo(idEquipo=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idEquipo es None o no está presente en la URL
        if idEquipo is None:
            return redirect(url_for('login_bp.inicio'))
        else:
            detalle_equipo = sql_detalles_equipoBD(idEquipo)
            servcios_equipo=sql_lista_equipo_servicioBD(idEquipo)
            return render_template(f'{PATH_URL}/detalles_equipo.html', detalle_equipo=detalle_equipo, servcios_equipo=servcios_equipo)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('login_bp.inicio'))

# Detalles de un SERVICIO 
@home_bp.route("/detalles-servicio/", methods=['GET'])
@home_bp.route("/detalles-servicio/<int:idServicio>", methods=['GET'])
def detalleServicio(idServicio=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idServicio es None o no está presente en la URL
        if idServicio is None:
            return redirect(url_for('login_bp.inicio'))
        else:
            detalle_servicio = sql_detalles_servicioBD(idServicio)
            return render_template(f'{PATH_URL}/detalles_servicio.html', detalle_servicio=detalle_servicio)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('login_bp.inicio'))

# Buscadon de empleados
@home_bp.route("/buscando-empleado", methods=['POST'])
def viewBuscarEmpleadoBD():
    resultadoBusqueda = buscarEmpleadoBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_empleado.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})

# Editar CLIENTE
@home_bp.route("/editar-cliente/<int:id>", methods=['GET'])
def viewEditarCliente(id):
    if 'conectado' in session:
        respuestaCliente = buscarClienteUnico(id)
        if respuestaCliente:
            return render_template(f'{PATH_URL}/form_cliente_update.html', respuestaCliente=respuestaCliente)
        else:
            flash('El cliente no existe.', 'error')
            return redirect(url_for('login_bp.inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('login_bp.inicio'))

# Recibir formulario para actulizar informacion de CLIENTE
@home_bp.route('/actualizar-cliente', methods=['POST'])
def actualizarCliente():
    resultData = procesar_actualizacion_form_cliente(request)
    id_Clientes = request.form['id_Clientes']  # <-- obtienes el id del formulario
    if resultData:
        detalle_empleado = sql_detalles_empleadosBD(id_Clientes)
        equipos_cliente=sql_lista_equipo_clienteBD(id_Clientes)
        return render_template(f'{PATH_URL}/detalles_empleado.html', detalle_empleado=detalle_empleado, equipos_cliente=equipos_cliente)
    else:
        flash('Error al actualizar el cliente.', 'error')
        return redirect(url_for('home_bp.lista_empleados'))

# Editar EQUIPO
@home_bp.route("/editar-equipo/<int:id>", methods=['GET'])
def viewEditarEquipo(id):
    if 'conectado' in session:
        respuestaEquipo = buscarEquipoUnico(id)
        if respuestaEquipo:
            return render_template(f'{PATH_URL}/form_equipo_update.html', respuestaEquipo=respuestaEquipo)
        else:
            flash('El equipo no existe.', 'error')
            return redirect(url_for('login_bp.inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('login_bp.inicio'))

# Recibir formulario para actulizar informacion de EQUIPO
@home_bp.route('/actualizar-equipo', methods=['POST'])
def actualizarEquipo():
    resultDataEquipo = procesar_actualizacion_form_equipo(request)
    id_Equipos = request.form['id_Equipos']  # <-- obtienes el id del formulario
    if resultDataEquipo:
        detalle_equipo = sql_detalles_equipoBD(id_Equipos)
        servcios_equipo=sql_lista_equipo_servicioBD(id_Equipos)
        return render_template(f'{PATH_URL}/detalles_equipo.html', detalle_equipo=detalle_equipo, servcios_equipo=servcios_equipo)
    else:
        flash('Error al actualizar el equipo.', 'error')
        return redirect(url_for('home_bp.lista_empleados'))

# Editar SERVICIO
@home_bp.route("/editar-servicio/<int:id>", methods=['GET'])
def viewEditarServicio(id):
    if 'conectado' in session:
        respuestaServicio = buscarServicioUnico(id)
        if respuestaServicio:
            return render_template(f'{PATH_URL}/form_servicio_update.html', respuestaServicio=respuestaServicio)
        else:
            flash('El servicio no existe.', 'error')
            return redirect(url_for('login_bp.inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('login_bp.inicio'))

# Recibir formulario para actulizar informacion de SERVICIO
@home_bp.route('/actualizar-servicio', methods=['POST'])
def actualizarServicio():
    resultDataServicio = procesar_actualizacion_form_servicio(request)
    id_servicio = request.form['id_Servicios']  # <-- obtienes el id del formulario
    if resultDataServicio:
        detalle_servicio = sql_detalles_servicioBD(id_servicio)
        return render_template(f'{PATH_URL}/detalles_servicio.html', detalle_servicio=detalle_servicio)
    else:
        flash('Error al actualizar el servicio.', 'error')
        return redirect(url_for('home_bp.lista_empleados'))

@home_bp.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('login_bp.inicioCpanel'))


@home_bp.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('home_bp.usuarios'))
    else:
        flash('Error al actualizar el servicio.', 'error')
        return redirect(url_for('home_bp.lista_empleados'))
# Eliminar CLIENTE
@home_bp.route('/borrar-empleado/<string:id_Clientes>', methods=['GET'])
def borrarEmpleado(id_Clientes):
    resp = eliminarEmpleado(id_Clientes)
    if resp:
        flash('El Cliente fue eliminado correctamente', 'success')
        return redirect(url_for('home_bp.lista_empleados'))
    else:
        flash('Error al eliminar el cliente.', 'error')
        return redirect(url_for('home_bp.lista_empleados'))
# Eliminar EQUIPO
@home_bp.route('/borrar-equipo/<string:id_Equipos>/<string:id_Clientes>', methods=['GET'])
def borrarEquipo(id_Equipos,id_Clientes):
    resp = eliminarEquipo(id_Equipos)
    if resp:
        flash('El Equipo fue eliminado correctamente', 'success')
        detalle_empleado = sql_detalles_empleadosBD(id_Clientes)
        equipos_cliente=sql_lista_equipo_clienteBD(id_Clientes)
        return render_template(f'{PATH_URL}/detalles_empleado.html', detalle_empleado=detalle_empleado, equipos_cliente=equipos_cliente)
    else:
        flash('Error al eliminar el equipo.', 'error')
        return redirect(url_for('home_bp.lista_empleados'))
# Eliminar SERVICIO
@home_bp.route('/borrar-servicio/<string:id_Servicios>/<string:id_Equipos>', methods=['GET'])
def borrarServicio(id_Servicios,id_Equipos):
    resp = eliminarServicio(id_Servicios)
    if resp:
        flash('El Servicio fue eliminado correctamente', 'success')
        detalle_equipo = sql_detalles_equipoBD(id_Equipos)
        servcios_equipo=sql_lista_equipo_servicioBD(id_Equipos)
        return render_template(f'{PATH_URL}/detalles_equipo.html', detalle_equipo=detalle_equipo, servcios_equipo=servcios_equipo)
    else:
        flash('Error al eliminar el servicio.', 'error')
        return redirect(url_for('home_bp.lista_empleados'))
@home_bp.route("/descargar-informe-empleados/", methods=['GET'])
def reporteBD():
    if 'conectado' in session:
        return generarReporteExcel()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('login_bp.inicio'))

# ==================== RUTAS NUEVAS PARA EL NUEVO REDISEÑO DEL DASHBOARD ====================

# Nueva ruta de prueba para el dashboard rediseñado
@home_bp.route('/dashboard', methods=['GET'])
def dashboard():
    if 'conectado' in session:
        try:
            # Obtener datos para el nuevo dashboard
            estadisticas = obtener_estadisticas_dashboard()
            datos_marcas = obtener_datos_marcas()
            datos_garantias = obtener_datos_garantias()
            clientes_poblacion = obtener_clientes_por_poblacion()
            servicios_tipo = obtener_servicios_por_tipo()
            todas_poblaciones = obtener_todas_poblaciones()
            
            return render_template('public/dashboard/dashboard.html', 
                                 estadisticas=estadisticas,
                                 datos_marcas=datos_marcas,
                                 datos_garantias=datos_garantias,
                                 clientes_poblacion=clientes_poblacion,
                                 servicios_tipo=servicios_tipo,
                                 todas_poblaciones=todas_poblaciones)
        except Exception as e:
            print(f"Error en dashboard: {e}")
            flash('Error al cargar el dashboard.', 'error')
            return redirect(url_for('home_bp.dashboard'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('login_bp.inicio'))

@home_bp.route('/dashboard/api/datos-filtrados', methods=['POST'])
def api_datos_filtrados():
    if 'conectado' in session:
        año = request.json.get('año')
        mes = request.json.get('mes')
        poblacion = request.json.get('poblacion')
        
        datos_filtrados = obtener_datos_filtrados(año, mes, poblacion)
        
        return jsonify({
            'success': True,
            'datos': datos_filtrados
        })
    else:
        return jsonify({'success': False, 'error': 'No autorizado'})

@home_bp.route('/dashboard/api/servicios-mes', methods=['POST'])
def api_servicios_mes():
    if 'conectado' in session:
        año = request.json.get('año')
        servicios_mes = obtener_servicios_por_mes(año)
        
        return jsonify({
            'success': True,
            'datos': servicios_mes
        })
    else:
        return jsonify({'success': False, 'error': 'No autorizado'})