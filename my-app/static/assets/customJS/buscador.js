async function buscadorTable(tableId) {
  let input, busqueda, url;
  url = "/buscando-empleado";

  input = document.getElementById("search");
  busqueda = input.value.toUpperCase();

  const dataPeticion = { busqueda };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(url, dataPeticion, { headers });
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    if (response.data.fin === 0) {
      $(`#${tableId} tbody`).html("");
      $(`#${tableId} tbody`).html(`
      <tr>
        <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No resultados para la busqueda: <strong style="text-align:center;color: #222;">${busqueda}</strong></td>
      </tr>`);
      return false;
    }

    if (response.data) {
      $(`#${tableId} tbody`).html("");
      let miData = response.data;
      $(`#${tableId} tbody`).append(miData);
    }
  } catch (error) {
    console.error(error);
  }
}

async function buscadorAvanzadoTable(tableId) {
  const nombre = $('#nombre_filtro').val();
  const apellido = $('#apellido_filtro').val();
  const poblacion = $('#poblacion_filtro').val();
  const marca = $('#marca_filtro').val();
  const garantia = $('#garantia_filtro').val();
  const anio = $('#anio_filtro').val();
  const servicio = $('#servicio_filtro').val();
  const anioserv = $('#anioserv_filtro').val();
  const messerv = $('#messerv_filtro').val();

  console.log("Filtros seleccionados:");
  console.log({ nombre, apellido, poblacion, marca, garantia, anio, servicio, anioserv, messerv });

  const url = "/buscandor-avanzado";
  const dataPeticion = { nombre, apellido, poblacion, marca, garantia, anio, servicio, anioserv, messerv };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(url, dataPeticion, { headers });

    if (response.data && response.data.html) {
      $(`#${tableId} tbody`).html(response.data.html);

      actualizarSelect('#nombre_filtro', response.data.nombres, nombre);
      actualizarSelect('#apellido_filtro', response.data.apellidos, apellido);
      actualizarSelect('#poblacion_filtro', response.data.poblaciones, poblacion);
      actualizarSelect('#marca_filtro', response.data.marcas, marca);
      actualizarSelect('#garantia_filtro', response.data.garantias, garantia);
      actualizarSelect('#anio_filtro', response.data.anios, anio);
      actualizarSelect('#servicio_filtro', response.data.servicios, servicio);
      actualizarSelect('#anioserv_filtro', response.data.anios_servicio, anioserv);
      actualizarSelect('#messerv_filtro', response.data.meses_servicio, messerv);

    } else if (response.data.fin === 0) {
      $(`#${tableId} tbody`).html(`
        <tr>
          <td colspan="100%" style="text-align:center;color: red;font-weight: bold;">
            No resultados para la búsqueda
          </td>
        </tr>
      `);
    }

  } catch (error) {
    console.error(error);
  }
}


// Función para actualizar el contenido de un select sin perder el valor actual
function actualizarSelect(selector, nuevosValores, valorSeleccionado) {
  const $select = $(selector);
  const placeholder = $select.find('option:first').text();

  $select.empty();
  $select.append(`<option value="">${placeholder}</option>`);

  nuevosValores.forEach(valor => {
    $select.append(`<option value="${valor}">${valor}</option>`);
  });

  if (valorSeleccionado) {
    $select.val(valorSeleccionado).trigger('change.select2');
  }
}