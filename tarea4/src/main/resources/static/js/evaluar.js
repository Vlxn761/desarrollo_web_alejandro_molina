function mostrarOpciones(id) {
    document.getElementById(`a-${id}`).style.display = "none";
    document.getElementById(`form-${id}`).style.display = "inline";
}

function evaluar(id, nota) {
    fetch("/post-nota", {
        method: "POST",
        body: JSON.stringify({
            id: id,
            nota: nota
        }),
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
        document.getElementById(`form-${id}`).style.display = "none";
        document.getElementById(`a-${id}`).style.display = "inline";
        window.location.reload();
    })
    .catch(error => {
         console.error(
            "Hubo un problema al evaluar el aviso:",
            error
         );
    });
}
