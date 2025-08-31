// js/views/gestion_marca.js

async function renderGestionMarcaView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="view-header"><h2><i class="fas fa-palette"></i> Gestión de Marca</h2></div><p>Cargando perfil de marca...</p>`;

    try {
        // 1. Fetch current brand profile
        const response = await fetch(`${config.apiBaseUrl}/api/v1/brand-profile`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('No se pudo obtener el perfil de marca.');

        const profile = await response.json();
        const identity = profile.brand_identity || {};

        // 2. Render the form
        contentArea.innerHTML = `
            <div class="view-header">
                <h2><i class="fas fa-palette"></i> Gestión de Marca</h2>
            </div>
            <div class="form-container">
                <p>Define la identidad y el tono de voz de tu marca. El agente "Sarita" y otras herramientas de IA usarán esta información para generar contenido consistente.</p>
                <form id="brand-profile-form">
                    <div class="form-group">
                        <label for="tone-of-voice">Tono de Voz</label>
                        <textarea id="tone-of-voice" rows="6" placeholder="Ej: Amistoso, profesional, servicial, con un toque de humor. Evitar jerga demasiado técnica.">${profile.tone_of_voice || ''}</textarea>
                    </div>
                    <div class="form-group">
                        <label for="logo-url">URL del Logo</label>
                        <input type="url" id="logo-url" placeholder="https://ejemplo.com/logo.png" value="${identity.logo_url || ''}">
                    </div>
                    <div class="form-group">
                        <label for="primary-color">Color Primario</label>
                        <input type="color" id="primary-color" value="${identity.primary_color || '#FFFFFF'}">
                    </div>
                     <div class="form-group">
                        <label for="secondary-color">Color Secundario</label>
                        <input type="color" id="secondary-color" value="${identity.secondary_color || '#000000'}">
                    </div>
                    <button type="submit" class="btn-primary">Guardar Perfil de Marca</button>
                </form>
                <div id="brand-feedback" class="message-info" style="display:none; margin-top: 1rem;"></div>
            </div>
        `;

        // 3. Add submit listener
        document.getElementById('brand-profile-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const feedbackDiv = document.getElementById('brand-feedback');
            feedbackDiv.style.display = 'block';
            feedbackDiv.textContent = 'Guardando perfil...';

            const payload = {
                tone_of_voice: document.getElementById('tone-of-voice').value,
                brand_identity: {
                    logo_url: document.getElementById('logo-url').value,
                    primary_color: document.getElementById('primary-color').value,
                    secondary_color: document.getElementById('secondary-color').value,
                }
            };

            try {
                const postResponse = await fetch(`${config.apiBaseUrl}/api/v1/brand-profile`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                    body: JSON.stringify(payload)
                });
                if (!postResponse.ok) {
                    const errorData = await postResponse.json();
                    throw new Error(errorData.detail || 'Error del servidor.');
                }
                feedbackDiv.className = 'message-success';
                feedbackDiv.textContent = '¡Perfil de marca guardado con éxito!';
            } catch (error) {
                feedbackDiv.className = 'message-error';
                feedbackDiv.textContent = `Error: ${error.message}`;
            }
        });

    } catch (error) {
        contentArea.innerHTML = `<p class="message-error">Error al cargar la gestión de marca: ${error.message}</p>`;
    }
}

// --- Registrar la vista en el Router ---
if (typeof registerView === 'function') {
    registerView('admin_general', 'gestion-de-marca', renderGestionMarcaView);
} else {
    console.error("El sistema de registro de vistas no está disponible.");
}
