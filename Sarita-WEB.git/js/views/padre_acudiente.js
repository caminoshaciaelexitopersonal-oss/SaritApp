// js/views/padre_acudiente.js

// --- Funciones para la Vista del Padre o Acudiente ---

/**
 * Renderiza la vista de "Mis Alumnos" para el padre/acudiente.
 * Muestra una lista de los hijos a cargo y permite ver sus detalles.
 */
async function renderPadreAcudienteView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = '<h2><i class="fas fa-child"></i> Mis Alumnos</h2><p>Cargando información...</p>';

    try {
        // Se asume un endpoint /api/v1/padre/hijos que devuelve los alumnos asociados.
        const response = await fetch(`${config.apiBaseUrl}/api/v1/padre/hijos`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) {
            throw new Error('No se pudo obtener la lista de sus hijos/acudidos.');
        }

        const hijos = await response.json();

        let hijosCards = '<p>No tiene hijos/acudidos registrados en el sistema.</p>';
        if (hijos && hijos.length > 0) {
            hijosCards = hijos.map(hijo => `
                <div class="card">
                    <h3>${hijo.nombre_completo}</h3>
                    <p><strong>Curso:</strong> ${hijo.curso_actual || 'No asignado'}</p>
                    <button class="btn-primary btn-ver-progreso" data-alumno-id="${hijo.id}">Ver Progreso</button>
                </div>
            `).join('');
        }

        contentArea.innerHTML = `
            <div class="view-header">
                <h2><i class="fas fa-child"></i> Mis Alumnos</h2>
            </div>
            <div class="card-container" id="padre-alumnos-container">
                ${hijosCards}
            </div>
        `;

        // Añadir listener para los botones de "Ver Progreso"
        document.getElementById('padre-alumnos-container').addEventListener('click', async (e) => {
            if (e.target.classList.contains('btn-ver-progreso')) {
                const alumnoId = e.target.dataset.alumnoId;
                const alumnoNombre = e.target.closest('.card').querySelector('h3').textContent;

                openModal(`Progreso de ${alumnoNombre}`, '<p>Cargando progreso...</p>');

                try {
                    const response = await fetch(`${config.apiBaseUrl}/api/v1/alumnos/${alumnoId}/progreso`, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (!response.ok) {
                        throw new Error('No se pudo obtener el progreso del alumno.');
                    }
                    const progreso = await response.json();

                    const progresoHtml = `
                        <h4>Asistencia General: <span class="asistencia-${progreso.asistencia_status}">${progreso.asistencia_porcentaje}%</span></h4>

                        <h5>Calificaciones Recientes</h5>
                        <ul>
                            ${progreso.calificaciones_recientes.map(c => `<li>${c.materia}: <span class="nota">${c.nota}</span></li>`).join('')}
                        </ul>

                        <h5>Logros de Gamificación</h5>
                        <ul>
                            ${progreso.logros_gamificacion.map(l => `<li><i class="fas fa-trophy"></i> ${l.nombre}</li>`).join('')}
                        </ul>
                    `;

                    // Actualizar el cuerpo del modal con los datos reales
                    const modalBody = document.getElementById('modal-body');
                    if(modalBody) modalBody.innerHTML = progresoHtml;

                } catch (error) {
                    const modalBody = document.getElementById('modal-body');
                    if(modalBody) modalBody.innerHTML = `<p class="message-error">Error al cargar el progreso: ${error.message}</p>`;
                }
            }
        });

    } catch (error) {
        contentArea.innerHTML += `<p class="message-error">Error al cargar la información: ${error.message}</p>`;
    }
}

// --- Registrar la vista principal de Padre/Acudiente en el Router ---
if (typeof registerView === 'function') {
    registerView('padre_acudiente', 'mis-alumnos', renderPadreAcudienteView);
} else {
    console.error("El sistema de registro de vistas no está disponible.");
}
