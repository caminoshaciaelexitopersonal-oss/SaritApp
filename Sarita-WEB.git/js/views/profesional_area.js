// js/views/profesional_area.js

// --- Vistas para el Rol de Profesional de Área ---

/**
 * Renderiza el dashboard principal para el Profesional de Área.
 */
async function renderProfesionalAreaDashboardView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <div class="view-header">
            <h2><i class="fas fa-user-tie"></i> Panel del Profesional de Área</h2>
        </div>
        <p>Seleccione una opción del menú para comenzar a gestionar las actividades y recursos del área.</p>
    `;
}

/**
 * Renderiza la vista para Supervisar Actividades.
 */
async function renderSupervisarActividadesView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="view-header"><h2><i class="fas fa-tasks"></i> Supervisar Actividades</h2></div><p>Cargando actividades en curso...</p>`;

    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/eventos?estado=en-curso`, { // Asumimos un filtro por estado
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('No se pudo obtener la lista de actividades en curso.');
        const actividades = await response.json();

        const rows = actividades.map(item => `
            <tr>
                <td>${item.nombre}</td>
                <td>${item.tipo}</td>
                <td>${item.responsable || 'N/A'}</td>
                <td><span class="status-${item.estado.toLowerCase()}">${item.estado}</span></td>
            </tr>
        `).join('') || '<tr><td colspan="4">No hay actividades en curso para supervisar.</td></tr>';

        contentArea.innerHTML = `
            <div class="view-header">
                <h2><i class="fas fa-tasks"></i> Supervisar Actividades</h2>
            </div>
            <p>Panel para supervisar las actividades en curso del área.</p>
            <table class="data-table">
                <thead><tr><th>Actividad/Evento</th><th>Tipo</th><th>Responsable</th><th>Estado</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        `;
    } catch (error) {
        contentArea.innerHTML = `<p class="message-error">Error al cargar las actividades: ${error.message}</p>`;
    }
}


/**
 * Renderiza la vista para Gestionar Eventos.
 */
async function renderGestionarEventosView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="view-header"><h2><i class="fas fa-calendar-plus"></i> Gestionar Eventos</h2></div><p>Cargando eventos...</p>`;

    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/eventos`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('No se pudo obtener la lista de eventos.');
        const eventos = await response.json();

        const rows = eventos.map(item => `
            <tr>
                <td>${item.nombre}</td>
                <td>${item.tipo}</td>
                <td>${new Date(item.fecha).toLocaleDateString()}</td>
                <td><span class="status-${item.estado.toLowerCase()}">${item.estado}</span></td>
                <td>
                    <button class="btn-secondary btn-editar" data-id="${item.id}">Editar</button>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="5">No hay eventos para gestionar.</td></tr>';

        contentArea.innerHTML = `
            <div class="view-header">
                <h2><i class="fas fa-calendar-plus"></i> Gestionar Eventos</h2>
                <button class="btn-primary">Crear Nuevo Evento</button>
            </div>
            <p>Como Profesional de Área, puede crear y editar eventos. La eliminación requiere aprobación de un Jefe de Área.</p>
            <table class="data-table">
                <thead><tr><th>Nombre</th><th>Tipo</th><th>Fecha</th><th>Estado</th><th>Acciones</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        `;
    } catch (error) {
        contentArea.innerHTML = `<p class="message-error">Error al cargar los eventos: ${error.message}</p>`;
    }
}

/**
 * Renderiza la vista para Gestionar Disciplinas.
 */
async function renderGestionarDisciplinasView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="view-header"><h2><i class="fas fa-edit"></i> Gestionar Disciplinas</h2></div><p>Cargando disciplinas...</p>`;

    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/disciplinas`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('No se pudo obtener la lista de disciplinas.');
        const disciplinas = await response.json();

        const rows = disciplinas.map(item => `
            <tr>
                <td>${item.nombre}</td>
                <td>${item.area}</td>
                <td>
                    <button class="btn-secondary btn-editar" data-id="${item.id}">Editar</button>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="3">No hay disciplinas para gestionar.</td></tr>';

        contentArea.innerHTML = `
            <div class="view-header">
                <h2><i class="fas fa-edit"></i> Gestionar Disciplinas</h2>
                <button class="btn-primary">Crear Nueva Disciplina</button>
            </div>
            <table class="data-table">
                <thead><tr><th>Nombre</th><th>Área</th><th>Acciones</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        `;
    } catch (error) {
        contentArea.innerHTML = `<p class="message-error">Error al cargar las disciplinas: ${error.message}</p>`;
    }
}

// --- Registrar las vistas de Profesional de Área en el Router ---
if (typeof registerView === 'function') {
    registerView('profesional_area', 'dashboard', renderProfesionalAreaDashboardView);
    registerView('profesional_area', 'supervisar-actividades', renderSupervisarActividadesView);
    registerView('profesional_area', 'gestionar-eventos', renderGestionarEventosView);
    registerView('profesional_area', 'gestionar-disciplinas', renderGestionarDisciplinasView);
} else {
    console.error("El sistema de registro de vistas no está disponible.");
}
