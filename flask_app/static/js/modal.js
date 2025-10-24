const abrir = (foto) => {
      let modal = document.getElementById('modal');
      let imagen = document.getElementById('imagen-modal');
      imagen.src = foto.src;
      modal.style.display = 'flex';
    }

const cerrarModal = () => {
      document.getElementById('modal').style.display = 'none';
    }
  