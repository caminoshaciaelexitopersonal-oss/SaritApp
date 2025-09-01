// js/views/calendario_contenidos.js

async function renderCalendarioContenidosView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <div class="view-header">
            <h2><i class="fas fa-calendar-alt"></i> Calendario de Contenidos</h2>
            <button id="btn-schedule-new" class="btn-primary">Programar Nuevo Post</button>
        </div>
        <div id="calendar-container">
            <p>Cargando contenido programado...</p>
        </div>
    `;

    await loadScheduledPosts(token);

    document.getElementById('btn-schedule-new').addEventListener('click', () => {
        renderSchedulePostModal(token);
    });
}

async function loadScheduledPosts(token) {
    const container = document.getElementById('calendar-container');
    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/calendar`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('No se pudo obtener el contenido programado.');
        const posts = await response.json();

        if (posts.length === 0) {
            container.innerHTML = '<p>No hay posts programados.</p>';
            return;
        }

        const rows = posts.map(post => `
            <tr>
                <td>${new Date(post.publish_at).toLocaleString()}</td>
                <td>${post.platform}</td>
                <td><pre>${JSON.stringify(post.content_payload, null, 2)}</pre></td>
                <td><span class="status-${post.status.toLowerCase()}">${post.status}</span></td>
                <td>
                    <button class="btn-secondary btn-edit-post" data-id="${post.id}">Editar</button>
                    <button class="btn-danger btn-delete-post" data-id="${post.id}">Eliminar</button>
                </td>
            </tr>
        `).join('');

        container.innerHTML = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Fecha de Publicación</th>
                        <th>Plataforma</th>
                        <th>Contenido</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>${rows}</tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = `<p class="message-error">Error al cargar el calendario: ${error.message}</p>`;
    }

    // Add event listeners for the whole container
    container.addEventListener('click', async (e) => {
        const target = e.target;
        if (target.classList.contains('btn-delete-post')) {
            const postId = target.dataset.id;
            if (confirm(`¿Está seguro de que desea eliminar el post programado ID ${postId}?`)) {
                try {
                    const response = await fetch(`${config.apiBaseUrl}/api/v1/calendar/${postId}`, {
                        method: 'DELETE',
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (!response.ok) throw new Error('No se pudo eliminar el post.');
                    await loadScheduledPosts(token); // Refresh the list
                } catch (error) {
                    alert(`Error al eliminar: ${error.message}`);
                }
            }
        }
        // Placeholder for edit
        if (target.classList.contains('btn-edit-post')) {
            alert('La funcionalidad de editar se implementará próximamente.');
        }
    });
}

function renderSchedulePostModal(token) {
    // Simple modal implementation
    const modalHtml = `
        <div id="schedule-modal" class="modal">
            <div class="modal-content">
                <span class="close-button">&times;</span>
                <h3>Programar Nuevo Post</h3>
                <form id="schedule-form" class="form-container">
                    <div class="form-group">
                        <label for="platform-select">Plataforma</label>
                        <select id="platform-select" required>
                            <option value="instagram">Instagram</option>
                            <option value="facebook">Facebook</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="post-content">Texto del Post</label>
                        <textarea id="post-content" rows="5" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="publish-date">Fecha y Hora de Publicación</label>
                        <input type="datetime-local" id="publish-date" required>
                    </div>
                    <button type="submit" class="btn-primary">Programar</button>
                </form>
                <div id="modal-feedback" class="message-info" style="display:none; margin-top: 1rem;"></div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHtml);

    const modal = document.getElementById('schedule-modal');
    const closeButton = modal.querySelector('.close-button');

    const closeModal = () => {
        modal.remove();
    };

    closeButton.onclick = closeModal;
    window.onclick = (event) => {
        if (event.target == modal) {
            closeModal();
        }
    };

    modal.querySelector('#schedule-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const feedbackDiv = document.getElementById('modal-feedback');
        feedbackDiv.style.display = 'block';
        feedbackDiv.textContent = 'Programando post...';

        const payload = {
            platform: document.getElementById('platform-select').value,
            publish_at: new Date(document.getElementById('publish-date').value).toISOString(),
            content_payload: {
                text: document.getElementById('post-content').value
            }
        };

        try {
            const response = await fetch(`${config.apiBaseUrl}/api/v1/calendar`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(payload)
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error del servidor.');
            }
            feedbackDiv.className = 'message-success';
            feedbackDiv.textContent = '¡Post programado con éxito!';
            await loadScheduledPosts(token);
            setTimeout(closeModal, 1500);
        } catch (error) {
            feedbackDiv.className = 'message-error';
            feedbackDiv.textContent = `Error: ${error.message}`;
        }
    });
}

// --- Registrar la vista en el Router ---
if (typeof registerView === 'function') {
    registerView('admin_general', 'calendario-de-contenidos', renderCalendarioContenidosView);
} else {
    console.error("El sistema de registro de vistas no está disponible.");
}
