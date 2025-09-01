// js/views/almacenista.js

// --- Vistas para el Rol de Almacenista ---

/**
 * Renderiza la vista para Ver Inventario.
 */
async function renderVerInventarioView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="view-header"><h2><i class="fas fa-boxes"></i> Ver Inventario</h2></div><p>Cargando inventario...</p>`;
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
            </tr>
        `).join('') || '<tr><td colspan="5">No hay elementos en el inventario.</td></tr>';

        contentArea.innerHTML = `
            <div class="view-header">
                <h2><i class="fas fa-boxes"></i> Inventario Actual</h2>
            </div>
            <table class="data-table">
                <thead><tr><th>ID</th><th>Nombre</th><th>Categoría</th><th>Stock</th><th>Estado</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        `;
    } catch (error) {
        contentArea.innerHTML = `<p class="message-error">Error al cargar el inventario: ${error.message}</p>`;
    }
}

/**
 * Renderiza la vista para Registrar Movimientos de inventario.
 */
async function renderAlmacenistaRegistrarMovimientosView(token) {
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
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
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


// --- Registrar las vistas de Almacenista en el Router ---
if (typeof registerView === 'function') {
    registerView('almacenista', 'ver-inventario', renderVerInventarioView);
    registerView('almacenista', 'registrar-movimientos', renderAlmacenistaRegistrarMovimientosView);
} else {
    console.error("El sistema de registro de vistas no está disponible.");
}
