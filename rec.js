
var botonazo;
var i;
var UserSeleccionado;
var ActividSeleccionado;
UserSeleccionado = "Elige cuadrilla";
// document.getElementById("cuad1").option = 1;
//  document.getElementById("actividad1").option = 1;
document.getElementById("fechax").value = "2021-01-01";
function selec1(seleccion) {
  UserSeleccionado = seleccion;
};

function activ1(seleccion2) {
  ActividSeleccionado = seleccion2;
};
//*****************************************

var boton2 = document.getElementById('calcularG');
boton2.onclick = function() {
  botonazo = 2;
  var urlActiv;
  var largoTabla2 = document.getElementById('Table').rows.length;
  if (largoTabla2 > 0) {
    for (i = 0; i <= largoTabla2; i++) {
      $('#r' + i).remove();
    }
  }
  var fechax = document.getElementById('fechax');
  var fechaselec  = fechax.value;
  if (ActividSeleccionado=="Reclamos") {
        urlActiv = "estadisRec.php";
  }
  if (ActividSeleccionado=="Conexiones") {
        urlActiv = "estadisConx.php";
  }
  $.when(
    $.ajax({
      url: urlActiv,
      method: "GET",
      dataType: 'json',
      data: {
        "fecha": fechaselec
      }
        })).then(function(data) {
    reciboTabla2(data);
  });

};


function reciboTabla2(respuesta2) {
  var DatosJson2 = JSON.parse(JSON.stringify(respuesta2));
  var k2;

    $("#Table").append('<tr id ="r0" ><td>cuadrilla </td>' + '<td>cantidad</td>');
    for (i = 0; i < DatosJson2.length; i++) {
      k2 = i + 1;
      $("#Table").append('<tr id ="r' + k2 + '">' +
        '<td align="center" style="dislay: none;">' + DatosJson2[i].cuadrilla + '</td>' +
        '<td align="center" style="dislay: none;">' + DatosJson2[i].cantidad + '</td>' +
        '</tr>');
    }
};


//*****************************************

var boton3 = document.getElementById('calcularpc');
boton3.onclick = function() {
  var urlActiv2
  var largoTabla2 = document.getElementById('Table').rows.length;
  var fechuca = document.getElementById('fechax').value;
  if (largoTabla2 > 0) {
    for (i = 0; i <= largoTabla2; i++) {
      $('#r' + i).remove();
    }
  }
  if (ActividSeleccionado=="Reclamos") {
        urlActiv2 = "listaRec.php";
  }
  if (ActividSeleccionado=="Conexiones") {
        urlActiv2 = "listaConx.php";
  }
  $.when(
    $.ajax({
      url: urlActiv2,
      method: "GET",
      dataType: 'json',
      data: {
        "cuadrilla": UserSeleccionado,
        "fechuca":   fechuca
      }
    })).then(function(data1) {
      if (ActividSeleccionado=="Reclamos") {
          reciboTabla3(data1);
      }
        if (ActividSeleccionado=="Conexiones") {
          reciboTabla4(data1);
      }

  });

};


function reciboTabla3(respuesta3) {
  var DatosJson2 = JSON.parse(JSON.stringify(respuesta3));
  var k2;
      $("#Table").append('<tr id ="r0" ><td>Hora</td>' +  '<td>cuadrilla</td>' + '<td>nroCuenta</td>'  + '<td>nombre</td>'+ '<td>calle</td>' + '<td>nroCalle</td>'  + '<td>nroDepto</td>'  + '<td>tipo de Reclamo</td>' + '<td>Cerrado como</td> ');
      for (i = 0; i < DatosJson2.length; i++) {
        k2 = i + 1;
        $("#Table").append('<tr id ="r' + k2 + '">' +
          '<td align="center" style="dislay: none;">' + DatosJson2[i].FechaHora + '</td>' +
          '<td align="center" style="dislay: none;">' + DatosJson2[i].cuadrilla + '</td>' +
          '<td align="center" style="dislay: none;">' + DatosJson2[i].nroCuenta + '</td>' +
         '<td align="center" style="dislay: none;">' + DatosJson2[i].nombre + '</td>' +
         '<td align="center" style="dislay: none;">' + DatosJson2[i].calle + '</td>' +
         '<td align="center" style="dislay: none;">' + DatosJson2[i].nroCalle + '</td>' +
         '<td align="center" style="dislay: none;">' + DatosJson2[i].nroDepto + '</td>' +
         '<td align="center" style="dislay: none;">' + DatosJson2[i].tipoReclamo + '</td>' +
         '<td align="center" style="dislay: none;">' + DatosJson2[i].confirmacion + '</td>' +
       '</tr>');
 }
};

function reciboTabla4(respuesta4) {
  var DatosJson2 = JSON.parse(JSON.stringify(respuesta4));
  var k3;

       $("#Table").append('<tr id ="r0" ><td>Hora</td>' +  '<td>cuadrilla</td>' + '<td>nroCuenta</td>'  + '<td>nombre</td>'+ '<td>calle</td>' + '<td>nroCalle</td>'  + '<td>nroDepto</td>'  + '<td>tipo de trabajo</td>' + '<td>estado</td> ');
       for (i = 0; i < DatosJson2.length; i++) {
         k3 = i + 1;
         $("#Table").append('<tr id ="r' + k3 + '">' +
           '<td align="center" style="dislay: none;">' + DatosJson2[i].FechaHora + '</td>' +
           '<td align="center" style="dislay: none;">' + DatosJson2[i].cuadrilla + '</td>' +
           '<td align="center" style="dislay: none;">' + DatosJson2[i].nroUsuario + '</td>' +
          '<td align="center" style="dislay: none;">' + DatosJson2[i].nombre + '</td>' +
          '<td align="center" style="dislay: none;">' + DatosJson2[i].calle + '</td>' +
          '<td align="center" style="dislay: none;">' + DatosJson2[i].nroCalle + '</td>' +
          '<td align="center" style="dislay: none;">' + DatosJson2[i].nroDepto + '</td>' +
          '<td align="center" style="dislay: none;">' + DatosJson2[i].tipoTrabajo + '</td>' +
          '<td align="center" style="dislay: none;">' + DatosJson2[i].estado + '</td>' +
        '</tr>');
  }
};