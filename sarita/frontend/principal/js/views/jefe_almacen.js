// js/views/jefe_almacen.js

// --- Vistas para el Rol de Jefe de Almacén ---

/**
 * Renderiza el dashboard principal de inventario.
 */
async function renderDashboardInventarioView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="view-header"><h2><i class="fas fa-boxes"></i> Dashboard de Inventario</h2></div><p>Cargando inventario...</p>`;
    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/inventory/items`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('No se pudo obtener el inventario.');
        const items = await response.json();

        const rows = items.map(item => `
            <tr>
                <td>${item.id}</td>
                <td>${item.nombre}</td>
                <td>${item.categoria}</td>
                <td>${item.stock}</td>
                <td><span class="status-${item.estado.toLowerCase()}">${item.estado}</span></td>
                <td>
                    <button class="btn-secondary btn-hoja-vida" data-id="${item.id}">Ver Hoja de Vida</button>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="6">No hay elementos en el inventario.</td></tr>';

        contentArea.innerHTML = `
            <div class="view-header">
                <h2><i class="fas fa-boxes"></i> Inventario General</h2>
                <button class="btn-primary">Añadir Nuevo Elemento</button>
            </div>
            <table class="data-table">
                <thead><tr><th>ID</th><th>Nombre</th><th>Categoría</th><th>Stock</th><th>Estado</th><th>Acciones</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        `;
    } catch (error) {
        contentArea.innerHTML = `<p class="message-error">Error al cargar el inventario: ${error.message}</p>`;
    }
}

/**
 * Renderiza el formulario para registrar movimientos de inventario.
 */
async function renderRegistrarMovimientosView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <div class="view-header"><h2><i class="fas fa-dolly-flatbed"></i> Registrar Movimientos</h2></div>
        <form id="movimiento-form" class="form-container">
            <select id="movimiento-tipo" required>
                <option value="entrada">Entrada</option>
                <option value="salida">Salida</option>
            </select>
            <input type="number" id="movimiento-item-id" placeholder="ID del Elemento" required>
            <input type="number" id="movimiento-cantidad" placeholder="Cantidad" required>
            <textarea id="movimiento-justificacion" placeholder="Justificación del movimiento..."></textarea>
            <button type="submit" class="btn-primary">Registrar Movimiento</button>
        </form>
        <div id="movimiento-feedback" class="message-info" style="display:none;"></div>
    `;

    document.getElementById('movimiento-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const feedbackDiv = document.getElementById('movimiento-feedback');
        const submitButton = e.target.querySelector('button');
        submitButton.disabled = true;
        feedbackDiv.style.display = 'block';
        feedbackDiv.textContent = 'Registrando movimiento...';

        const payload = {
            item_id: parseInt(document.getElementById('movimiento-item-id').value, 10),
            cantidad: parseInt(document.getElementById('movimiento-cantidad').value, 10),
            tipo: document.getElementById('movimiento-tipo').value,
            justificacion: document.getElementById('movimiento-justificacion').value
        };

        try {
            const response = await fetch(`${config.apiBaseUrl}/api/v1/inventory/movimientos`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(payload)
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error desconocido del servidor.');
            }
            feedbackDiv.className = 'message-success';
            feedbackDiv.textContent = 'Movimiento registrado con éxito.';
            e.target.reset();
        } catch (error) {
            feedbackDiv.className = 'message-error';
            feedbackDiv.textContent = `Error: ${error.message}`;
        } finally {
            submitButton.disabled = false;
        }
    });
}

/**
 * Renderiza la vista de Stock y Reposición.
 */
async function renderStockReposicionView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="view-header"><h2><i class="fas fa-sort-amount-up"></i> Stock y Reposición</h2></div><p>Cargando items con bajo stock...</p>`;

    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/inventory/items?stock_level=low`, { // Asumimos filtro de API
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('No se pudo obtener el inventario.');
        const items = await response.json();

        const rows = items.map(item => `
            <tr>
                <td>${item.id}</td>
                <td>${item.nombre}</td>
                <td>${item.stock}</td>
                <td><button class="btn-primary">Ordenar Reposición</button></td>
            </tr>
        `).join('') || '<tr><td colspan="4">No hay elementos con bajo stock.</td></tr>';

        contentArea.innerHTML = `
            <div class="view-header"><h2><i class="fas fa-sort-amount-up"></i> Stock y Reposición</h2></div>
            <p>A continuación se muestran los elementos con niveles de stock bajos.</p>
            <table class="data-table">
                <thead><tr><th>ID</th><th>Nombre</th><th>Stock Actual</th><th>Acciones</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        `;
    } catch (error) {
        contentArea.innerHTML = `<p class="message-error">Error al cargar el stock: ${error.message}</p>`;
    }
}


/**
 * Renderiza la vista de Hojas de Vida de Elementos.
 */
async function renderHojasDeVidaView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="view-header"><h2><i class="fas fa-file-invoice"></i> Hojas de Vida de Elementos</h2></div><p>Cargando elementos...</p>`;

    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/inventory/items`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('No se pudo obtener el inventario.');
        const items = await response.json();

        const rows = items.map(item => `
            <tr>
                <td>${item.id}</td>
                <td>${item.nombre}</td>
                <td>${item.categoria}</td>
                <td><button class="btn-secondary">Ver Hoja de Vida</button></td>
            </tr>
        `).join('') || '<tr><td colspan="4">No hay elementos en el inventario.</td></tr>';

        contentArea.innerHTML = `
            <div class="view-header"><h2><i class="fas fa-file-invoice"></i> Hojas de Vida de Elementos</h2></div>
            <table class="data-table">
                <thead><tr><th>ID</th><th>Nombre</th><th>Categoría</th><th>Acciones</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        `;
    } catch (error) {
        contentArea.innerHTML = `<p class="message-error">Error al cargar los elementos: ${error.message}</p>`;
    }
}


/**
 * Renderiza la vista de Reportes de Inventario.
 */
async function renderReportesInventarioView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <div class="view-header"><h2><i class="fas fa-file-excel"></i> Reportes de Inventario</h2></div>
        <div class="form-container">
            <h3>Generar Nuevo Reporte</h3>
            <select id="report-type">
                <option value="valoracion">Reporte de Valoración</option>
                <option value="rotacion">Reporte de Rotación</option>
                <option value="completo">Inventario Completo</option>
            </select>
            <button type="button" id="generate-report-btn" class="btn-primary">Generar y Descargar</button>
            <button type="button" id="export-sheets-btn" class="btn-secondary">Exportar a Google Sheets</button>
        </div>
        <div id="report-feedback" class="message-info" style="display:none; margin-top: 1rem;"></div>
        <p class="message-info">La generación de reportes local se implementará en una futura actualización.</p>
    `;

    document.getElementById('export-sheets-btn').addEventListener('click', async () => {
        const feedbackDiv = document.getElementById('report-feedback');
        feedbackDiv.style.display = 'block';
        feedbackDiv.className = 'message-info';
        feedbackDiv.textContent = 'Exportando a Google Sheets...';

        // Sample data since report generation is not implemented
        const sampleData = [
            ["ID del Elemento", "Nombre", "Categoría", "Stock", "Estado"],
            ["101", "Balón de Fútbol", "Deportes", "50", "Disponible"],
            ["102", "Zapatillas de Ballet", "Danza", "25", "Bajo Stock"],
            ["201", "Pintura Acrílica", "Artes Plásticas", "120", "Disponible"],
            ["301", "Guitarra Acústica", "Música", "15", "Disponible"]
        ];

        try {
            const response = await fetch(`${config.apiBaseUrl}/api/v1/auth/google/export_sheets`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify({
                    sheet_name: `Reporte de Inventario - ${new Date().toLocaleString()}`,
                    data: sampleData
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error del servidor.');
            }

            const result = await response.json();
            feedbackDiv.className = 'message-success';
            feedbackDiv.innerHTML = `¡Exportación exitosa! <a href="${result.link}" target="_blank">Ver en Google Sheets</a>`;

        } catch (error) {
            feedbackDiv.className = 'message-error';
            feedbackDiv.textContent = `Error al exportar: ${error.message}`;
        }
    });
}

// --- Registrar las vistas de Jefe de Almacén en el Router ---
if (typeof registerView === 'function') {
    registerView('jefe_almacen', 'dashboard-inventario', renderDashboardInventarioView);
    registerView('jefe_almacen', 'registrar-movimientos', renderRegistrarMovimientosView);
    registerView('jefe_almacen', 'stock-y-reposicion', renderStockReposicionView);
    registerView('jefe_almacen', 'hojas-de-vida', renderHojasDeVidaView);
    registerView('jefe_almacen', 'reportes-de-inventario', renderReportesInventarioView);
} else {
    console.error("El sistema de registro de vistas no está disponible.");
}
