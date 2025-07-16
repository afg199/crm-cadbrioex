const loaderOut = document.querySelector("#loader-out");
function fadeOut(element) {
  let opacity = 1;
  const timer = setInterval(function () {
    if (opacity <= 0.1) {
      clearInterval(timer);
      element.style.display = "none";
    }
    element.style.opacity = opacity;
    opacity -= opacity * 0.1;
  }, 50);
}
fadeOut(loaderOut);

function eliminarEmpleado(id_empleado) {
  if (confirm("¿Estas seguro que deseas Eliminar este Cliente?")) {
    let url = `/borrar-empleado/${id_empleado}`;
    if (url) {
      window.location.href = url;
    }
  }
}

function eliminarEquipo(id_Equipos, id_Clientes) {
  if (confirm("¿Estas seguro que deseas Eliminar este Equipo?")) {
    let url = `/borrar-equipo/${id_Equipos}/${id_Clientes}`;
    if (url) {
      window.location.href = url;
    }
  }
}

function eliminarServicio(id_Servicios, id_Equipos) {
  if (confirm("¿Estas seguro que deseas Eliminar este Servicio?")) {
    let url = `/borrar-servicio/${id_Servicios}/${id_Equipos}`;
    if (url) {
      window.location.href = url;
    }
  }
}
