// js/views/jefe_escenarios.js

// --- Vistas para el Rol de Jefe de Escenarios ---

/**
 * Renderiza la vista del Calendario y Gestión de Escenarios.
 */
async function renderCalendarioEscenariosView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="view-header"><h2><i class="fas fa-calendar-alt"></i> Calendario y Gestión de Escenarios</h2></div><p>Cargando escenarios...</p>`;
    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/escenarios`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('No se pudo obtener la lista de escenarios.');

        const escenarios = await response.json();
        let escenarioRows = escenarios.map(e => `
            <tr>
                <td>${e.id}</td>
                <td>${e.nombre}</td>
                <td>${e.tipo}</td>
                <td>${e.capacidad || 'N/A'}</td>
                <td><span class="status-${e.estado.toLowerCase()}">${e.estado}</span></td>
                <td>
                    <button class="btn-secondary btn-ver-horario" data-id="${e.id}">Ver Horario</button>
                    <button class="btn-secondary btn-editar-escenario" data-id="${e.id}">Editar</button>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="6">No se encontraron escenarios.</td></tr>';

        contentArea.innerHTML = `
            <div class="view-header">
                <h2><i class="fas fa-calendar-alt"></i> Calendario y Gestión de Escenarios</h2>
                <div>
                    <button class="btn-primary" id="btn-add-escenario">Añadir Nuevo Escenario</button>
                    <button class="btn-secondary" id="btn-sync-google-calendar">Sincronizar con Google Calendar</button>
                </div>
            </div>
            <div id="calendar-feedback" class="message-info" style="display:none; margin-top: 1rem;"></div>
            <table class="data-table">
                <thead><tr><th>ID</th><th>Nombre</th><th>Tipo</th><th>Capacidad</th><th>Estado</th><th>Acciones</th></tr></thead>
                <tbody id="escenarios-tbody">${escenarioRows}</tbody>
            </table>`;

        document.getElementById('escenarios-tbody').addEventListener('click', (e) => {
            if (e.target.classList.contains('btn-ver-horario')) {
                alert(`Funcionalidad 'Ver Horario' para escenario ID: ${e.target.dataset.id} pendiente de implementación.`);
            }
            if (e.target.classList.contains('btn-editar-escenario')) {
                alert(`Funcionalidad 'Editar' para escenario ID: ${e.target.dataset.id} pendiente de implementación.`);
            }
        });
         document.getElementById('btn-add-escenario').addEventListener('click', (e) => {
            alert(`Funcionalidad 'Añadir Nuevo Escenario' pendiente de implementación.`);
        });

        document.getElementById('btn-sync-google-calendar').addEventListener('click', async () => {
            const feedbackDiv = document.getElementById('calendar-feedback');
            feedbackDiv.style.display = 'block';
            feedbackDiv.className = 'message-info';
            feedbackDiv.textContent = 'Sincronizando con Google Calendar...';

            // Sample event data
            const now = new Date();
            const start = new Date(now.getTime() + 60 * 60 * 1000); // 1 hour from now
            const end = new Date(start.getTime() + 60 * 60 * 1000); // 1 hour duration

            const sampleEvent = {
                summary: 'Mantenimiento Cancha Principal',
                start_datetime: start.toISOString(),
                end_datetime: end.toISOString(),
                attendees: []
            };

            try {
                const response = await fetch(`${config.apiBaseUrl}/api/v1/auth/google/create_event`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                    body: JSON.stringify(sampleEvent)
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Error del servidor.');
                }

                const result = await response.json();
                feedbackDiv.className = 'message-success';
                feedbackDiv.innerHTML = `¡Evento creado con éxito! <a href="${result.link}" target="_blank">Ver en Google Calendar</a>`;

            } catch (error) {
                feedbackDiv.className = 'message-error';
                feedbackDiv.textContent = `Error al crear evento: ${error.message}`;
            }
        });

    } catch (error) {
        contentArea.innerHTML = `<p class="message-error">Error al cargar los escenarios: ${error.message}</p>`;
    }
}

/**
 * Renderiza la vista para Asignar Espacios.
 */
async function renderAsignarEspaciosView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <div class="view-header"><h2><i class="fas fa-map-marker-alt"></i> Asignar Espacios</h2></div>
        <form id="asignar-form" class="form-container">
            <input type="number" id="asignar-escenario-id" placeholder="ID del Escenario" required>
            <input type="text" id="asignar-evento-nombre" placeholder="Nombre del Evento/Clase" required>
            <input type="date" id="asignar-fecha" required>
            <input type="time" id="asignar-hora-inicio" required>
            <input type="time" id="asignar-hora-fin" required>
            <button type="submit" class="btn-primary">Asignar Espacio</button>
        </form>
        <div id="asignar-feedback" class="message-info" style="display:none;"></div>
    `;

    document.getElementById('asignar-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const feedbackDiv = document.getElementById('asignar-feedback');
        feedbackDiv.style.display = 'block';
        feedbackDiv.textContent = 'Procesando asignación...';

        const payload = {
            escenario_id: parseInt(document.getElementById('asignar-escenario-id').value, 10),
            nombre_evento: document.getElementById('asignar-evento-nombre').value,
            fecha: document.getElementById('asignar-fecha').value,
            hora_inicio: document.getElementById('asignar-hora-inicio').value,
            hora_fin: document.getElementById('asignar-hora-fin').value,
        };

        try {
            const response = await fetch(`${config.apiBaseUrl}/api/v1/escenarios/asignar`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error desconocido.');
            }

            feedbackDiv.className = 'message-success';
            feedbackDiv.textContent = '¡Espacio asignado con éxito!';
            e.target.reset();
        } catch (error) {
            feedbackDiv.className = 'message-error';
            feedbackDiv.textContent = `Error: ${error.message}`;
        }
    });
}

/**
 * Renderiza la vista para Mantenimiento de Escenarios.
 */
async function renderMantenimientoEscenariosView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="view-header"><h2><i class="fas fa-tools"></i> Mantenimiento de Escenarios</h2></div><p>Cargando historial...</p>`;
    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/escenarios/mantenimiento`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('No se pudo obtener el historial de mantenimiento.');
        const mantenimientos = await response.json();

        const rows = mantenimientos.map(item => `
            <tr>
                <td>${item.escenario_nombre}</td>
                <td>${new Date(item.fecha).toLocaleDateString()}</td>
                <td>${item.descripcion}</td>
                <td><span class="status-${item.estado.toLowerCase()}">${item.estado}</span></td>
            </tr>
        `).join('') || '<tr><td colspan="4">No hay registros de mantenimiento.</td></tr>';

        contentArea.innerHTML = `
            <div class="view-header">
                <h2><i class="fas fa-tools"></i> Mantenimiento de Escenarios</h2>
                <button class="btn-primary" id="btn-registrar-mantenimiento">Registrar Nuevo Mantenimiento</button>
            </div>
            <table class="data-table">
                <thead><tr><th>Escenario</th><th>Fecha</th><th>Descripción</th><th>Estado</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        `;

        document.getElementById('btn-registrar-mantenimiento').addEventListener('click', () => {
            alert('Funcionalidad para registrar mantenimiento pendiente de implementación.');
        });

    } catch (error) {
        contentArea.innerHTML = `<p class="message-error">Error al cargar el historial: ${error.message}</p>`;
    }
}

// --- Registrar las vistas de Jefe de Escenarios en el Router ---
if (typeof registerView === 'function') {
    registerView('jefe_escenarios', 'calendario-de-escenarios', renderCalendarioEscenariosView);
    registerView('jefe_escenarios', 'asignar-espacios', renderAsignarEspaciosView);
    registerView('jefe_escenarios', 'mantenimiento', renderMantenimientoEscenariosView);
} else {
    console.error("El sistema de registro de vistas no está disponible.");
}
