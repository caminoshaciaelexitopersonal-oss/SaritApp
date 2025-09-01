// js/views/coordinador.js

// --- Vistas para el Rol de Coordinador ---

/**
 * Renderiza la vista de Planificación de Actividades.
 */
async function renderPlanificacionView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="view-header"><h2><i class="fas fa-calendar-day"></i> Planificación de Actividades</h2></div><p>Cargando programación...</p>`;

    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/coordinador/programacion`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('No se pudo obtener la programación.');
        const programacion = await response.json();

        const rows = programacion.map(item => `
            <tr>
                <td>${item.profesor}</td>
                <td>${item.materia}</td>
                <td>${item.dias}</td>
                <td>${item.horas}</td>
                <td><span class="status-${item.estado.toLowerCase()}">${item.estado}</span></td>
            </tr>
        `).join('') || '<tr><td colspan="5">No hay actividades programadas.</td></tr>';

        contentArea.innerHTML = `
            <div class="view-header"><h2><i class="fas fa-calendar-day"></i> Planificación de Actividades</h2></div>
            <table class="data-table">
                <thead><tr><th>Profesor</th><th>Materia</th><th>Días</th><th>Horario</th><th>Estado</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        `;
    } catch (error) {
        contentArea.innerHTML = `<p class="message-error">Error al cargar la planificación: ${error.message}</p>`;
    }
}

/**
 * Renderiza la vista para Verificar Programación.
 */
async function renderVerificarProgramacionView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="view-header"><h2><i class="fas fa-clipboard-check"></i> Verificar Cumplimiento</h2></div><p>Cargando programación para verificación...</p>`;

    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/coordinador/programacion`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('No se pudo obtener la programación.');
        const programacion = await response.json();

        const rows = programacion.map(item => `
            <tr>
                <td>${item.profesor}</td>
                <td>${item.materia}</td>
                <td><span class="status-${item.estado.toLowerCase()}">${item.estado}</span></td>
                <td><input type="checkbox" ${item.estado === 'Completado' ? 'checked' : ''} /></td>
            </tr>
        `).join('') || '<tr><td colspan="4">No hay actividades programadas para verificar.</td></tr>';

        contentArea.innerHTML = `
            <div class="view-header"><h2><i class="fas fa-clipboard-check"></i> Verificar Cumplimiento de Programación</h2></div>
            <table class="data-table">
                <thead><tr><th>Profesor</th><th>Materia</th><th>Estado</th><th>Verificado</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        `;
    } catch (error) {
        contentArea.innerHTML = `<p class="message-error">Error al cargar la vista de verificación: ${error.message}</p>`;
    }
}


/**
 * Maneja la acción de aprobar o rechazar una solicitud.
 */
async function handleAprobacionAction(id, action, token) {
    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/coordinador/aprobaciones/${id}/${action}`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || `No se pudo ${action} la solicitud.`);
        }
        return true;
    } catch (error) {
        alert(`Error al procesar la solicitud: ${error.message}`);
        return false;
    }
}

/**
 * Renderiza la vista del Panel de Aprobaciones.
 */
async function renderAprobacionesView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="view-header"><h2><i class="fas fa-check-double"></i> Panel de Aprobaciones</h2></div><p>Cargando items pendientes...</p>`;

    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/coordinador/aprobaciones`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('No se pudo obtener la lista de aprobaciones.');
        const aprobaciones = await response.json();

        const rows = aprobaciones.map(item => `
            <tr data-id="${item.id}">
                <td>${item.tipo}</td>
                <td>${item.descripcion}</td>
                <td>${item.solicitado_por}</td>
                <td>
                    <button class="btn-primary btn-aprobar" data-action="approve">Aprobar</button>
                    <button class="btn-danger btn-rechazar" data-action="reject">Rechazar</button>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="4">No hay items pendientes de aprobación.</td></tr>';

        contentArea.innerHTML = `
            <div class="view-header"><h2><i class="fas fa-check-double"></i> Panel de Aprobaciones</h2></div>
            <table class="data-table">
                <thead><tr><th>Tipo</th><th>Descripción</th><th>Solicitado Por</th><th>Acciones</th></tr></thead>
                <tbody id="aprobaciones-tbody">${rows}</tbody>
            </table>
        `;

        document.getElementById('aprobaciones-tbody').addEventListener('click', async (e) => {
            if (e.target.tagName === 'BUTTON') {
                const button = e.target;
                const action = button.dataset.action;
                const row = button.closest('tr');
                const id = row.dataset.id;

                button.disabled = true;
                button.textContent = 'Procesando...';

                const success = await handleAprobacionAction(id, action, token);
                if (success) {
                    row.remove(); // Elimina la fila de la tabla si la acción fue exitosa
                } else {
                    button.disabled = false;
                    button.textContent = action === 'approve' ? 'Aprobar' : 'Rechazar';
                }
            }
        });

    } catch (error) {
        contentArea.innerHTML = `<p class="message-error">Error al cargar las aprobaciones: ${error.message}</p>`;
    }
}

async function renderGestionarMisionesView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="view-header"><h2><i class="fas fa-tasks"></i> Gestionar Misiones de Gamificación</h2></div><p>Cargando misiones...</p>`;

    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/gamificacion/misiones`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('No se pudieron cargar las misiones.');
        const misiones = await response.json();

        const rows = misiones.map(m => `
            <tr>
                <td>${m.nombre}</td>
                <td>${m.puntos_recompensa}</td>
                <td>${m.es_grupal ? 'Sí' : 'No'}</td>
                <td>${m.fecha_limite ? new Date(m.fecha_limite).toLocaleDateString() : 'N/A'}</td>
            </tr>
        `).join('') || '<tr><td colspan="4">No hay misiones creadas.</td></tr>';

        contentArea.innerHTML = `
            <div class="view-header"><h2><i class="fas fa-tasks"></i> Gestionar Misiones</h2></div>
            <div class="form-container">
                <h3>Crear Nueva Misión</h3>
                <form id="crear-mision-form">
                    <input type="text" id="mision-nombre" placeholder="Nombre de la misión" required>
                    <textarea id="mision-descripcion" placeholder="Descripción de la misión"></textarea>
                    <input type="number" id="mision-puntos" placeholder="Puntos de recompensa" value="0">
                    <label><input type="checkbox" id="mision-es-grupal"> ¿Es una misión grupal?</label>
                    <button type="submit" class="btn-primary">Crear Misión</button>
                </form>
            </div>
            <div class="data-table-container">
                <h3>Misiones Existentes</h3>
                <table class="data-table">
                    <thead><tr><th>Nombre</th><th>Puntos</th><th>Grupal</th><th>Fecha Límite</th></tr></thead>
                    <tbody>${rows}</tbody>
                </table>
            </div>
        `;

        // Add listener for the form
        document.getElementById('crear-mision-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const newMission = {
                nombre: document.getElementById('mision-nombre').value,
                descripcion: document.getElementById('mision-descripcion').value,
                puntos_recompensa: parseInt(document.getElementById('mision-puntos').value, 10),
                es_grupal: document.getElementById('mision-es-grupal').checked,
                inquilino_id: 1 // Placeholder
            };

            const createResponse = await fetch(`${config.apiBaseUrl}/api/v1/gamificacion/misiones`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(newMission)
            });

            if (createResponse.ok) {
                alert('¡Misión creada con éxito!');
                renderContentForView('gestionar-misiones', token, 'coordinador'); // Refresh the view
            } else {
                const errorData = await createResponse.json();
                alert(`Error al crear la misión: ${errorData.detail}`);
            }
        });

    } catch (error) {
        contentArea.innerHTML = `<p class="message-error">Error al cargar la gestión de misiones: ${error.message}</p>`;
    }
}

// --- Registrar las vistas de Coordinador en el Router ---
if (typeof registerView === 'function') {
    registerView('coordinador', 'planificacion', renderPlanificacionView);
    registerView('coordinador', 'verificar-programacion', renderVerificarProgramacionView);
    registerView('coordinador', 'aprobaciones', renderAprobacionesView);
    registerView('coordinador', 'gestionar-misiones', renderGestionarMisionesView);
} else {
    console.error("El sistema de registro de vistas no está disponible.");
}
