const validateName = (name) => {
  if(!name) return false;
  let lengthValid = name.trim().length >= 4;
  
  return lengthValid;
}

const validateEmail = (email) => {
  if (!email) return false;
  let lengthValid = email.length > 15;

  // validamos el formato
  let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
  let formatValid = re.test(email);

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
  if (!phoneNumber) return false;
  // validación de longitud
  let lengthValid = phoneNumber.length >= 8;

  // validación de formato
  let re = /^[0-9]+$/;
  let formatValid = re.test(phoneNumber);

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && formatValid;
};

const validateFiles = (files) => {
  if (!files) return false;

  // validación del número de archivos
  let lengthValid = 1 <= files.length && files.length <= 3;

  // validación del tipo de archivo
  let typeValid = true;

  for (const file of files) {
    // el tipo de archivo debe ser "image/<foo>" o "application/pdf"
    let fileFamily = file.type.split("/")[0];
    typeValid &&= fileFamily == "image" || file.type == "application/pdf";
  }

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && typeValid;
};

const validateSelect = (select) => {
  if(!select) return false;
  return true
}

const validateForm = () => {
  // obtener elementos del DOM usando el nombre del formulario.
  let myForm = document.forms["myForm"];

  let region = myForm["select-region"].value;
  let comuna = myForm["select-comuna"].value;
  let sector = myForm["sector"].value;

  let nombre = myForm["nombre"].value;
  let email = myForm["email"].value;
  let celular = myForm["tel"].value;
  let red = myForm["select-red"].value;
  let contacto = myForm["contacto"].value;
  
  let mascota = myForm["select-mascota"].value;
  let cantidad = myForm["cantidad"].value;
  let edad = myForm["edad"].value;
  let unidadMedida = myForm["select-unidad"].value;
  let fecha = myForm["fecha"].value;
  let descripcion = myForm["descripcion"].value;
  let files = myForm["contacto"].files;

  // variables auxiliares de validación y función.
  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };

  // lógica de validación
  if (!validateSelect(region)) {
    setInvalidInput("Región");
  }
  if (!validateSelect(comuna)) {
    setInvalidInput("Comuna");
  }
  if (!validateSector(sector)) {
    setInvalidInput("Sector");
  }
  if (!validateNombre(nombre)) {
    setInvalidInput("Nombre");
  }
  if (!validateEmail(email)) {
    setInvalidInput("Email");
  }
  if (!validateCelular(celular)) {
    setInvalidInput("Celular");
  }
  if (!validateRed(red)) {
    setInvalidInput("Red social");
  }
  if (!validateContacto(contacto)) {
    setInvalidInput("Contacto");
  }
  if (!validateMascota(mascota)) {
    setInvalidInput("Tipo de mascota");
  }
  if (!validateInt(cantidad)) {
    setInvalidInput("Cantidad de mascotas");
  }
  if (!validateInt(Edad)) {
    setInvalidInput("Edad de mascotas");
  }
  if (!validateSelect(unidadMedida)) {
    setInvalidInput("Unidad de medida de edad");
  }
  if (!validateFecha(fecha)) {
    setInvalidInput("Fecha");
  }
  if (!validateFiles(files)) {
    setInvalidInput("Fotos");
  }

  if (!validateName(name)) {
    setInvalidInput("Nombre");
  }
  if (!validateEmail(email)) {
    setInvalidInput("Email");
  }
  if (!validatePhoneNumber(phoneNumber)) {
    setInvalidInput("Número");
  }
  if (!validateFiles(files)) {
    setInvalidInput("Fotos");
  }
  if (!validateSelect(department)) {
    setInvalidInput("Departamento");
  }
  if (!validateSelect(curso)) {
    setInvalidInput("Curso");
  }

  // finalmente mostrar la validación
  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");
  let formContainer = document.querySelector(".main-container");

  if (!isValid) {
    validationListElem.textContent = "";
    // agregar elementos inválidos al elemento val-list.
    for (input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    }
    // establecer val-msg
    validationMessageElem.innerText = "Los siguientes campos son inválidos:";

    // aplicar estilos de error
    validationBox.style.backgroundColor = "#ffdddd";
    validationBox.style.borderLeftColor = "#f44336";

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
  } else {
    // Ocultar el formulario
    myForm.style.display = "none";

    // establecer mensaje de éxito
    validationMessageElem.innerText = "¡Formulario válido! ¿Deseas enviarlo o volver?";
    validationListElem.textContent = "";

    // aplicar estilos de éxito
    validationBox.style.backgroundColor = "#ddffdd";
    validationBox.style.borderLeftColor = "#4CAF50";

    // Agregar botones para enviar el formulario o volver
    let submitButton = document.createElement("button");
    submitButton.innerText = "Enviar";
    submitButton.style.marginRight = "10px";
    submitButton.addEventListener("click", () => {
      // myForm.submit();
      // no tenemos un backend al cual enviarle los datos
    });

    let backButton = document.createElement("button");
    backButton.innerText = "Volver";
    backButton.addEventListener("click", () => {
      // Mostrar el formulario nuevamente
      myForm.style.display = "block";
      validationBox.hidden = true;
    });

    validationListElem.appendChild(submitButton);
    validationListElem.appendChild(backButton);

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
  }
};


let submitBtn = document.getElementById("submit-btn");
submitBtn.addEventListener("click", validateForm);
