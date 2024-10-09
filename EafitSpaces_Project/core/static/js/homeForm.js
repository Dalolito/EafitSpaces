

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
function submitForm(event) {
    event.preventDefault(); // Evita el envío predeterminado del formulario

    const form = document.getElementById("reservation_form");

    fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: {
            'X-CSRFToken': form.querySelector('input[name="csrfmiddlewaretoken"]').value
        }
    })
    .then(response => {
        if (response.ok) {
            // Oculta el formulario
            form.style.display = "none";
            document.getElementById("image_confirmation").style.display = "block"; // Muestra la imagen de confirmación
            document.getElementById("confirmation_message").style.display = "block"; // Muestra el mensaje de confirmación
            
            // Oculta la imagen de reserva y los recursos
            document.querySelector('.image_reservation').style.display = "none";
            document.querySelector('.information').style.display = "none";
            
            localStorage.setItem('image_confirmation_visible', 'true'); // Guarda el estado en localStorage
        } else {
            alert("There was a problem with the reservation. Please try again.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("There was a problem with the reservation. Please try again.");
    });
}

// Aplicar el estado guardado al cargar la página
window.onload = ajustarEstadoFormulario;











