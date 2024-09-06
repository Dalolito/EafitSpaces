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
    var popupVisible = localStorage.getItem('popup_form_visible');
    var imageVisible = localStorage.getItem('image_confirmation_visible');

    document.getElementById('popup_form').style.display = popupVisible === 'true' ? 'block' : 'none';
    document.getElementById('overlay').style.display = popupVisible === 'true' ? 'block' : 'none';

    document.getElementById('reservation_form').style.display = imageVisible === 'true' ? 'none' : 'block';
    document.getElementById('image_confirmation').style.display = imageVisible === 'true' ? 'block' : 'none';
    document.getElementById('confirmation_message').style.display = imageVisible === 'true' ? 'block' : 'none';
}


// Función para enviar el formulario y mostrar la imagen de confirmación
function submitForm() {
    document.getElementById("reservation_form").style.display = "none";
    document.getElementById("image_confirmation").style.display = "block";
    document.getElementById("confirmation_message").style.display = "block";
    localStorage.setItem('image_confirmation_visible', 'true');
}


// Aplicar el estado guardado al cargar la página
window.onload = ajustarEstadoFormulario;