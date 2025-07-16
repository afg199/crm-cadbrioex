from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_home import *

PATH_URL = "public/empleados"

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

# Buscando de CLIENTE
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

# Busqueda Avanzada
@app.route("/busqueda-avanzada/", methods=['GET'])
def busquedaAvanzada():
    if 'conectado' in session:
      filtro_nombres = obtener_nombres_filtro()
      filtro_apellidos = obtener_apellidos_filtro()
      filtro_poblaciones = obtener_poblaciones_filtro()
      filtro_marca = obtener_marca_filtro()
      filtro_garantia = obtener_garantia_filtro()
      filtro_anios = obtener_filtro_anios()
      filtro_servicio = obtener_servicio_filtro()
      filtro_anio_servicio = obtener_filtro_anios_servicio()
      fitro_mes_servicio = obtener_filtro_mes_servicio()
      
      empleados = sql_lista_empleados_con_equipos()
      return render_template(f'{PATH_URL}/busqueda_avanzada.html', empleados=empleados , filtro_nombres=filtro_nombres, 
                             filtro_apellidos=filtro_apellidos, filtro_poblaciones=filtro_poblaciones, filtro_marca=filtro_marca, 
                             filtro_garantia=filtro_garantia, filtro_anios=filtro_anios, filtro_servicio=filtro_servicio,
                             filtro_anio_servicio=filtro_anio_servicio, fitro_mes_servicio=fitro_mes_servicio)
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Buscando de AVANZADA con filtros
@app.route("/buscandor-avanzado", methods=['POST'])
def viewBuscarEmpleadoAvanzado():
   # Normalizador de texto (quita espacios y homogeniza)
    def limpiar(valor):
        return valor.strip().lower() if valor else ""
    # Diccionario auxiliar para mantener el formato bonito
    def extraer_unicos_normalizados(lista):
        vistos = {}
        for valor in lista:
            clave = limpiar(valor)
            if clave and clave not in vistos:
                vistos[clave] = valor.strip().capitalize()
        return sorted(vistos.values())

    data = request.json
    nombre = data.get('nombre', '')
    apellido = data.get('apellido', '')
    poblacion = data.get('poblacion', '')
    marca = data.get('marca', '')
    garantia = data.get('garantia', '')
    anio = data.get('anio', '')
    servicio = data.get('servicio', '')
    anioserv = data.get('anioserv', '')
    messerv = data.get('messerv', '')

    resultadoBusqueda = buscarAvanzadoBD(nombre, apellido, poblacion, marca, garantia, anio, servicio, anioserv, messerv)

    if resultadoBusqueda:
        nuevos_nombres = extraer_unicos_normalizados([r["nombre"] for r in resultadoBusqueda if r["nombre"]])
        nuevos_apellidos = extraer_unicos_normalizados([r["apellido"] for r in resultadoBusqueda if r["apellido"]])
        nuevas_poblaciones = extraer_unicos_normalizados([r["poblacion"] for r in resultadoBusqueda if r["poblacion"]])
        nuevas_marcas = extraer_unicos_normalizados([e["marca"] for r in resultadoBusqueda for e in r.get("equipos", []) if e.get("marca")])
        nuevas_garantias = extraer_unicos_normalizados([e["garantia"] for r in resultadoBusqueda for e in r.get("equipos", []) if e.get("garantia")])
        nuevas_anios = extraer_unicos_normalizados([e["fecha_compra"][:4] for r in resultadoBusqueda for e in r.get("equipos", []) if e.get("fecha_compra")])
        nuevos_servicios = extraer_unicos_normalizados([ s["tipo_servicio"] for r in resultadoBusqueda for e in r.get("equipos", []) for s in e.get("servicios", [])if s.get("tipo_servicio")])
        nuevos_anios_servicio = extraer_unicos_normalizados([ s["fecha_servicio"][:4] for r in resultadoBusqueda for e in r.get("equipos", []) for s in e.get("servicios", []) if s.get("fecha_servicio")])
        nuevos_meses_servicio = extraer_unicos_normalizados([ s["fecha_servicio"][5:7] for r in resultadoBusqueda for e in r.get("equipos", []) for s in e.get("servicios", []) if s.get("fecha_servicio")])

        html_render = render_template(f'{PATH_URL}/resultado_busqueda_avanzada.html', dataBusqueda=resultadoBusqueda)
        return jsonify({
            'html': html_render,
            "nombres": nuevos_nombres,
            "apellidos": nuevos_apellidos,
            "poblaciones": nuevas_poblaciones,
            "marcas": nuevas_marcas,
            'garantias': nuevas_garantias,
            'anios': nuevas_anios,
            'servicios': nuevos_servicios,
            'anios_servicio': nuevos_anios_servicio,
            'meses_servicio': nuevos_meses_servicio
        })
    else:
        return jsonify({'fin': 0})