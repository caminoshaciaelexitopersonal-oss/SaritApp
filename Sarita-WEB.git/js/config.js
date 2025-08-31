// Archivo de Configuración Central
// ---------------------------------
// Este archivo contiene la configuración principal para la aplicación web.
// Modifica la URL base de la API aquí para apuntar al backend correcto
// en diferentes entornos (desarrollo, pruebas, producción).

window.config = {
  // URL base para todas las llamadas a la API de SGA-CD-FASTAPI-BACKEND.
  // Para desarrollo local, usualmente es http://localhost:8000 o http://127.0.0.1:8000.
  // Asegúrate de que no termine con una barra inclinada ('/').
  apiBaseUrl: 'http://localhost:8000'
};
