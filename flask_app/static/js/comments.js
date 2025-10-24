const validateName = (name) => {
  if(!name) return false;
  let lengthValid = name.length >= 3 && name.length <= 80;
  
  return lengthValid;
}

const validateTexto = (texto) => {
  if(!texto) return false;
  let lengthValid = texto.length >= 5;
  
  return lengthValid;
}

async function agregarComentario(id) {
    let form = document.forms["form"];

    let nombre = form["nombre"].value;
    let texto = form["texto"].value;

    let invalidInputs = [];
    let isValid = true;
    const setInvalidInput = (inputName) => {
        invalidInputs.push(inputName);
        isValid &&= false;
    };
    if (!validateName(nombre)) {
        setInvalidInput("Nombre");
    }
    if (!validateTexto(texto)) {
        setInvalidInput("Texto");
    }

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
        validationBox.hidden = true;
        fetch(`${window.origin}/comentarios/${id}`, {
                method: "POST",
                body: JSON.stringify({ nombre: nombre, texto: texto  }),
                credentials: "include",
                cache: "no-cache",
                headers: {
                "Content-Type": "application/json",
              },
            })
              .then((response) => {
                if (!response.ok) {
                    throw new Error("Respuesta erronea");
                }
                form.reset();
                cargarComentarios(id);                
            })
              .catch((error) => {
                console.error(
                "Hubo un problema al agregar el comentario:",
                error
                );
            });
    }
} 

async function cargarComentarios(id) {
    fetch(`${window.origin}/comentarios/${id}`)
      .then((response) => response.json())
      .then((data) => {
        let commentBox = document.getElementById("comentarios");
        commentBox.innerHTML = '<p class="titulo-comentario">Comentarios</p>';
        if (Object.keys(data).length == 0) {
          commentBox.innerHTML += "No hay comentarios";
        }
        for (comentario of data){
            let div = document.createElement("div");
            div.className = "comentario";

            let autor = document.createElement("p");
            autor.className = "comentario-autor";
            autor.innerHTML = comentario.nombre;

            let fecha = document.createElement("p");
            fecha.className = "comentario-fecha";
            fecha.innerHTML = comentario.fecha;

            let texto = document.createElement("p");
            texto.className = "comentario-texto";
            texto.innerHTML = comentario.texto;

            div.appendChild(autor);
            div.appendChild(fecha);
            div.appendChild(texto);
            commentBox.append(div)
        }
      })
      .catch((error) => {
        console.error("Hubo un error al obtener los comentarios:", error);
      });
}

