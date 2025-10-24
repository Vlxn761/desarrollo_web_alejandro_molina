const validateSelect = (select) => {
  if(!select) return false;
  return true
}

const validateName = (name) => {
  if(!name) return false;
  let lengthValid = name.trim().length >= 3 && name.trim().length <= 200;
  
  return lengthValid;
}

const validateSector = (sector) => {
  let lengthValid = sector.length <= 100;
  
  return lengthValid;
}

const validateEmail = (email) => {
  if (!email) return false;
  let lengthValid = email.length <= 100 ;

  let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
  let formatValid = re.test(email);

  return lengthValid && formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
  if (!phoneNumber) return true;

  let re = /^\+\d{3}\.\d{8}$/;
  let formatValid = re.test(phoneNumber);

  return formatValid;
};


const validateContact = (bloque) => {
  let bloques = bloque.querySelectorAll("div");

  for (const bloqueContacto of bloques) {
    let select = bloqueContacto.querySelector("select");
    let largoInput = bloqueContacto.querySelector("input").value.length;  

    if (validateSelect(select.value)) {
      if (largoInput < 4 || largoInput > 50) return false;
    }
  } 
  return true;
};

const validateInt = (num) => {
  if(!num) return false;

  let numValid = num >= 1;

  let re = /^[1-9]\d*$/;
  let typeValid = re.test(num);
  
  return numValid && typeValid;
};

const validateFiles = (files) => {
  if (!files) return false;

  let lengthValid = 1 <= files.length && files.length <= 3;

  return lengthValid;
};

const validateDate = (fecha) => {
  if (!fecha) return false;

  let fechaInput = new Date(fecha); 
  let fechaPrellenada = new Date();
  fechaPrellenada.setHours(fechaPrellenada.getHours() + 3);

  return fechaInput >= fechaPrellenada;
};

const validatePhotos = (fotos) => {
  let lengthValid = true;

  // Hay al menos una foto
  for (const foto of fotos) {
    lengthValid &&= !validateFiles(foto.files); 
  }

  return !lengthValid;
};

const validateForm = () => {
  let myForm = document.forms["myForm"];

  let region = myForm["select-region"].value;
  let comuna = myForm["select-comuna"].value;
  let sector = myForm["sector"].value;

  let nombre = myForm["nombre"].value;
  let email = myForm["email"].value;
  let celular = myForm["tel"].value;
  let contacto = document.getElementById("redes")
  
  let mascota = myForm["select-mascota"].value;
  let cantidad = myForm["cantidad"].value;
  let edad = myForm["edad"].value;
  let unidadMedida = myForm["select-unidad"].value;
  let fecha = myForm["fecha"].value;
  let fotos = document.getElementById("imagenes").querySelectorAll("input");

  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };

  if (!validateSelect(region)) {
    setInvalidInput("Región");
  }
  if (!validateSelect(comuna)) {
    setInvalidInput("Comuna");
  }
  if (!validateSector(sector)) {
    setInvalidInput("Sector");
  }
  if (!validateName(nombre)) {
    setInvalidInput("Nombre");
  }
  if (!validateEmail(email)) {
    setInvalidInput("Email");
  }
  if (!validatePhoneNumber(celular)) {
    setInvalidInput("Celular");
  }
  if (!validateContact(contacto)) {
    setInvalidInput("Contacto");
  }
  if (!validateSelect(mascota)) {
    setInvalidInput("Tipo de mascota");
  }
  if (!validateInt(cantidad)) {
    setInvalidInput("Cantidad de mascotas");
  }
  if (!validateInt(edad)) {
    setInvalidInput("Edad de mascotas");
  }
  if (!validateSelect(unidadMedida)) {
    setInvalidInput("Unidad de medida de edad");
  }
  if (!validateDate(fecha)) {
    setInvalidInput("Fecha");
  }
  if (!validatePhotos(fotos)) {
    setInvalidInput("Fotos");
  }

  // del aux 3
  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");

  if (!isValid) {
    validationListElem.textContent = "";
    
    for (input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    }
    
    validationMessageElem.innerText = "Los siguientes campos son inválidos:";

    validationBox.style.backgroundColor = "#ffdddd";
    validationBox.style.borderLeftColor = "#f44336";

    validationBox.hidden = false;
  } else {
    myForm.style.display = "none";

    validationMessageElem.innerText = "¡Formulario válido! ¿Deseas enviarlo o volver?";
    validationListElem.textContent = "";

    validationBox.style.backgroundColor = "#ddffdd";
    validationBox.style.borderLeftColor = "#4CAF50";

    let submitButton = document.createElement("button");
    submitButton.innerText = "Enviar";
    submitButton.style.marginRight = "10px";

    let backButton = document.createElement("button");
    backButton.innerText = "Volver";
    backButton.addEventListener("click", () => {
      myForm.style.display = "block";
      validationBox.hidden = true;
    });

    submitButton.addEventListener("click", () => myForm.submit());

    validationListElem.appendChild(submitButton);
    validationListElem.appendChild(backButton);

    validationBox.hidden = false;
  }
};


let submitBtn = document.getElementById("envio");
submitBtn.addEventListener("click", validateForm);