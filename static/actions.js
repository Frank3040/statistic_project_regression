

// Función para realizar la acción y recordar la posición de desplazamiento
function realizarAccion() {
    // Guarda la posición de desplazamiento actual en localStorage
    localStorage.setItem('scrollPosition', window.scrollY);

    // Simula la acción de enviar el formulario
    // Puedes realizar aquí la lógica de la acción si es necesario
    // En este ejemplo, simplemente se muestra un mensaje en la consola
    console.log('Acción realizada');
    
    return true;  // Permite el envío real del formulario
}

// Restaura la posición de desplazamiento al cargar la página
window.onload = function() {
    const scrollPosition = localStorage.getItem('scrollPosition');
    if (scrollPosition !== null) {
        window.scrollTo(0, parseInt(scrollPosition, 10));
        localStorage.removeItem('scrollPosition');  // Limpiar después de restaurar
    }
};
