async function renderJefeAreaView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <div class="jefe-area-dashboard">
            <h2>Panel de Jefe de Área</h2>
            <div id="jefe-area-dashboard-content">
                <p>Cargando datos del área...</p>
            </div>
        </div>
    `;

    try {
        // Fetch staff and events concurrently
        const [staffResponse, eventsResponse] = await Promise.all([
            fetch(`${config.apiBaseUrl}/api/v1/jefe_area/staff`, {
                headers: { 'Authorization': `Bearer ${token}` }
            }),
            fetch(`${config.apiBaseUrl}/api/v1/jefe_area/events`, {
                headers: { 'Authorization': `Bearer ${token}` }
            })
        ]);

        if (!staffResponse.ok) throw new Error('No se pudo obtener la lista de personal.');
        if (!eventsResponse.ok) throw new Error('No se pudo obtener la lista de eventos.');

        const staff = await staffResponse.json();
        const events = await eventsResponse.json();

        // Render the tables
        const dashboardContent = document.getElementById('jefe-area-dashboard-content');
        dashboardContent.innerHTML = `
            <div class="admin-section">
                <h3><i class="fas fa-users"></i> Personal del Área</h3>
                <button class="btn-primary">Añadir Personal</button>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre Completo</th>
                            <th>Email</th>
                            <th>Rol</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${renderStaffRows(staff)}
                    </tbody>
                </table>
            </div>
            <div class="admin-section">
                <h3><i class="fas fa-calendar-alt"></i> Eventos del Área</h3>
                <button class="btn-primary">Crear Evento</button>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre del Evento</th>
                            <th>Tipo</th>
                            <th>Fecha</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${renderEventRows(events)}
                    </tbody>
                </table>
            </div>
        `;
    } catch (error) {
        console.error('Error rendering jefe_area view:', error);
        contentArea.innerHTML = `<p class="message-error">Error al cargar el panel de Jefe de Área: ${error.message}</p>`;
    }
}

function renderStaffRows(staff) {
    if (!staff || staff.length === 0) {
        return '<tr><td colspan="5">No se encontró personal en tu área.</td></tr>';
    }
    return staff.map(user => `
        <tr>
            <td>${user.id}</td>
            <td>${user.nombre_completo}</td>
            <td>${user.correo}</td>
            <td>${user.roles.join(', ')}</td>
            <td>
                <button class="btn-secondary">Editar</button>
            </td>
        </tr>
    `).join('');
}

function renderEventRows(events) {
    if (!events || events.length === 0) {
        return '<tr><td colspan="5">No se encontraron eventos en tu área.</td></tr>';
    }
    return events.map(event => `
        <tr>
            <td>${event.id}</td>
            <td>${event.nombre}</td>
            <td>${event.tipo}</td>
            <td>${new Date(event.fecha).toLocaleDateString()}</td>
            <td>
                <button class="btn-secondary">Editar</button>
            </td>
        </tr>
    `).join('');
}
