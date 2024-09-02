function openForm() {
    document.getElementById("popup_form").style.display = "block";
    document.getElementById("overlay").style.display = "block";
    document.getElementById("image_confirmation").style.display = "none";
    localStorage.setItem('popup_form_visible', 'true');
    localStorage.setItem('image_confirmation_visible', 'false');
}

// Función para cerrar el formulario y guardar el estado en localStorage
function closeForm() {
    document.getElementById("popup_form").style.display = "none";
    document.getElementById("overlay").style.display = "none";
    document.getElementById("image_confirmation").style.display = "none";
    localStorage.setItem('popup_form_visible', 'false');

    window.location.href = "/";
}

// Función para ajustar el estado del formulario al cargar la página
function ajustarEstadoFormulario() {
    var estado = localStorage.getItem('popup_form_visible');
    var formulario = document.getElementById('popup_form');
    var overlay = document.getElementById('overlay');
    if (estado === 'true') {
        formulario.style.display = 'block';
        overlay.style.display = 'block';
    } else {
        formulario.style.display = 'none';
        overlay.style.display = 'none';
    }

    var estado = localStorage.getItem('image_confirmation_visible');
    var formulario = document.getElementById('reservation_form');
    var confirmation = document.getElementById('image_confirmation');
    if (estado == 'true') {
        formulario.style.display = 'none';
        confirmation.style.display = 'block';
    } else {
        formulario.style.display = 'block';
        confirmation.style.display = 'none';
    }
}

// Función para enviar el formulario y mostrar la imagen de confirmación
function submitForm() {
    document.getElementById("reservation_form").style.display = "none";
    document.getElementById("image_confirmation").style.display = "block";
    localStorage.setItem('image_confirmation_visible', 'true');
}

// Aplicar el estado guardado al cargar la página
window.onload = ajustarEstadoFormulario;