
function openForm() {
    document.getElementById("popup_form").style.display = "block";
    document.getElementById("overlay").style.display = "block";
    localStorage.setItem('popup_form_visible', 'true');
}

// Función para cerrar el formulario y guardar el estado en localStorage
function closeForm() {
    document.getElementById("popup_form").style.display = "none";
    document.getElementById("overlay").style.display = "none";
    localStorage.setItem('popup_form_visible', 'false');
    window.location.href = "/resourcesAdmin";
}

// Función para ajustar el estado del formulario al cargar la página
function ajustarEstadoFormulario() {
    var popupVisible = localStorage.getItem('popup_form_visible');

    document.getElementById('popup_form').style.display = popupVisible === 'true' ? 'block' : 'none';
    document.getElementById('overlay').style.display = popupVisible === 'true' ? 'block' : 'none';

    document.getElementById('resources_form').style.display = imageVisible === 'true' ? 'none' : 'block';
    document.getElementById('confirmation_message').style.display = imageVisible === 'true' ? 'block' : 'none';
}


// Función para enviar el formulario y mostrar la imagen de confirmación
function submitForm() {
    document.getElementById("resources_form").style.display = "none";
    document.getElementById("confirmation_message").style.display = "block";
}


// Aplicar el estado guardado al cargar la página
window.onload = ajustarEstadoFormulario;

// Selecciona los elementos relevantes
const addBtn = document.getElementById('add-btn');
const closeBtn = document.getElementById('close-btn');
const formContainer = document.getElementById('add_resource_form');
const successMessage = document.getElementById('success-message');
const form = document.getElementById('resources_form');

// Función para alternar el formulario de agregar espacios
addBtn.addEventListener('click', () => {
    if (formContainer.style.display === 'block') {
        document.getElementById("overlay").style.display = "none";
        formContainer.style.display = 'none'; // Oculta el formulario si está abierto
    } else {
        document.getElementById("overlay").style.display = "block";
        formContainer.style.display = 'block'; // Muestra el formulario si está oculto
        formContainer.classList.add('show');
    }
});

// Función para cerrar el formulario
closeBtn.addEventListener('click', () => {
    document.getElementById("overlay").style.display = "none";
    formContainer.style.display = 'none';
});

// Función para mostrar el mensaje de éxito después de enviar el formulario
form.addEventListener('submit', (event) => {
    event.preventDefault(); // Evitar la recarga de la página para mostrar el mensaje

    // Muestra el mensaje de éxito
    successMessage.style.display = 'block';

    // Ocultar el formulario
    formContainer.style.display = 'none';

    // Ocultar el mensaje después de 3 segundos
    setTimeout(() => {
        successMessage.style.display = 'none';
    }, 3000);
});