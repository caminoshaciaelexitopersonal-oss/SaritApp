// js/views/tecnico_area.js

// --- Vistas para el Rol de Técnico o Asistente de Área ---

/**
 * Renderiza el dashboard principal para el Técnico de Área.
 */
async function renderTecnicoAreaDashboardView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <div class="view-header">
            <h2><i class="fas fa-user-cog"></i> Panel del Técnico de Área</h2>
        </div>
        <p>Seleccione una opción del menú para comenzar a gestionar las actividades y recursos del área.</p>
    `;
}

/**
 * Renderiza la vista para Gestionar Eventos (con permisos de crear y editar).
 */
async function renderTecnicoGestionarEventosView(token) {
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
            <p>Como Técnico de Área, puede crear y editar eventos. La eliminación requiere aprobación de un Jefe de Área.</p>
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
 * Renderiza la vista para Gestionar Disciplinas (con permisos de crear y editar).
 */
async function renderTecnicoGestionarDisciplinasView(token) {
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


/**
 * Renderiza la vista para Asistir en Gestión de Usuarios. (Placeholder)
 */
async function renderAsistirGestionUsuariosView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <div class="view-header">
            <h2><i class="fas fa-users-cog"></i> Asistir en Gestión de Usuarios</h2>
        </div>
        <p>Aquí podrá asistir en la gestión de usuarios, con permisos limitados.</p>
        <p class="message-info">Esta funcionalidad se implementará en una futura actualización.</p>
    `;
}

/**
 * Renderiza la vista para ver Reportes Operativos. (Placeholder)
 */
async function renderReportesOperativosView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <div class="view-header">
            <h2><i class="fas fa-chart-line"></i> Reportes Operativos</h2>
        </div>
        <p>Aquí podrá consultar reportes operativos del área.</p>
        <p class="message-info">Esta funcionalidad se implementará en una futura actualización.</p>
    `;
}


// --- Registrar las vistas de Técnico de Área en el Router ---
if (typeof registerView === 'function') {
    registerView('tecnico_area', 'dashboard', renderTecnicoAreaDashboardView);
    registerView('tecnico_area', 'gestionar-eventos', renderTecnicoGestionarEventosView);
    registerView('tecnico_area', 'gestionar-disciplinas', renderTecnicoGestionarDisciplinasView);
    registerView('tecnico_area', 'asistir-gestion-usuarios', renderAsistirGestionUsuariosView);
    registerView('tecnico_area', 'reportes-operativos', renderReportesOperativosView);
} else {
    console.error("El sistema de registro de vistas no está disponible.");
}
