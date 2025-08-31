// js/views/admin_general.js

// --- Vistas para el Rol de Administrador General ---

/**
 * Renderiza el dashboard principal para el Administrador General.
 */
async function renderAdminGeneralDashboardView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <div class="view-header">
            <h2><i class="fas fa-shield-alt"></i> Panel del Administrador General</h2>
        </div>
        <p>Bienvenido, Super Administrador. Desde aquí podrá gestionar la configuración global de la plataforma.</p>
        <p>Seleccione una opción del menú para comenzar.</p>
    `;
}

/**
 * Renderiza la vista para configurar la integración con WhatsApp.
 */
async function renderConfiguracionWhatsAppView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <div class="view-header">
            <h2><i class="fab fa-whatsapp"></i> Configuración de Integración con WhatsApp</h2>
        </div>
        <div class="form-container">
            <p>Aquí puede configurar las credenciales para conectar el sistema con la API de WhatsApp Business.</p>
            <form id="whatsapp-config-form">
                <div class="form-group">
                    <label for="whatsapp-api-token">API Token</label>
                    <input type="password" id="whatsapp-api-token" placeholder="Su token de acceso permanente">
                </div>
                <div class="form-group">
                    <label for="whatsapp-phone-id">Phone Number ID</label>
                    <input type="text" id="whatsapp-phone-id" placeholder="El ID de su número de teléfono de WhatsApp">
                </div>
                <div class="form-group">
                    <label for="whatsapp-verify-token">Verify Token</label>
                    <input type="text" id="whatsapp-verify-token" value="sga-cd-whatsapp-secret" readonly>
                    <small>Este token debe ser configurado en su panel de Meta for Developers.</small>
                </div>
                <button type="submit" class="btn-primary">Guardar Configuración</button>
            </form>
            <div id="config-feedback" class="message-info" style="display:none; margin-top: 1rem;"></div>
        </div>
    `;

    document.getElementById('whatsapp-config-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const feedbackDiv = document.getElementById('config-feedback');
        const submitButton = e.target.querySelector('button');
        submitButton.disabled = true;
        feedbackDiv.style.display = 'block';
        feedbackDiv.textContent = 'Guardando configuración...';

        const payload = {
            api_token: document.getElementById('whatsapp-api-token').value,
            phone_number_id: document.getElementById('whatsapp-phone-id').value
        };

        try {
            const response = await fetch(`${config.apiBaseUrl}/api/v1/admin_general/settings/whatsapp`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error desconocido del servidor.');
            }

            feedbackDiv.className = 'message-success';
            feedbackDiv.textContent = '¡Configuración guardada con éxito!';
        } catch (error) {
            feedbackDiv.className = 'message-error';
            feedbackDiv.textContent = `Error: ${error.message}`;
        } finally {
            submitButton.disabled = false;
        }
    });
}


/**
 * Renderiza la vista para gestionar las claves de API de los LLMs y YouTube.
 */
async function renderApiKeysView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <div class="view-header">
            <h2><i class="fas fa-key"></i> Gestión de Claves de API</h2>
        </div>
        <div id="api-keys-form-container" class="form-container">
            <p>Cargando configuración...</p>
        </div>
    `;

    // 1. Fetch current settings
    let currentSettings = { openai_api_key: '', google_api_key: '', youtube_refresh_token: '' };
    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/admin_general/settings/api_keys`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            currentSettings = await response.json();
        }
    } catch (e) {
        console.error("Error fetching API keys:", e);
    }

    // 2. Render the form
    const formContainer = document.getElementById('api-keys-form-container');
    formContainer.innerHTML = `
        <p>Añada las claves de API para los servicios externos que desea utilizar.</p>
        <form id="api-keys-config-form">
            <div class="form-group">
                <label for="openai-api-key">OpenAI API Key</label>
                <input type="password" id="openai-api-key" placeholder="sk-..." value="${currentSettings.openai_api_key || ''}">
            </div>
            <div class="form-group">
                <label for="google-api-key">Google API Key</label>
                <input type="password" id="google-api-key" placeholder="AIza..." value="${currentSettings.google_api_key || ''}">
            </div>

            <hr>

            <div class="form-group">
                <label>Google Workspace Integration</label>
                <div id="google-connection-status" class="api-status">Cargando estado...</div>
                <button type="button" id="google-connect-btn" class="btn-secondary">Conectar con Google</button>
            </div>

            <hr>

            <div class="form-group">
                <label>Facebook / Instagram Video Publishing</label>
                <div id="meta-connection-status" class="api-status">Cargando estado...</div>
                <button type="button" id="meta-connect-btn" class="btn-secondary">Conectar con Facebook/Instagram</button>
            </div>

            <hr>

            <div class="form-group">
                <label for="youtube-refresh-token">YouTube Refresh Token</label>
                <input type="password" id="youtube-refresh-token" placeholder="Token de actualización de Google OAuth" value="${currentSettings.youtube_refresh_token || ''}">
                <small>Este token se obtiene ejecutando el script 'generate_youtube_refresh_token.py' en el backend.</small>
            </div>
            <button type="submit" class="btn-primary">Guardar Claves</button>
        </form>
        <div id="api-keys-feedback" class="message-info" style="display:none; margin-top: 1rem;"></div>
    `;

    // 3. Fetch and display Meta connection status
    const statusDiv = document.getElementById('meta-connection-status');
    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/auth/meta/status`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            const statusData = await response.json();
            if (statusData.connected) {
                statusDiv.innerHTML = `Conectado a la página de FB <strong>${statusData.page_name}</strong> y a la cuenta de IG <strong>${statusData.ig_username}</strong>.`;
                statusDiv.className = 'api-status status-ok';
            } else {
                statusDiv.innerHTML = 'No Conectado. Haga clic en el botón para conectar su cuenta.';
                statusDiv.className = 'api-status status-error';
            }
        } else {
             statusDiv.innerHTML = 'No se pudo verificar el estado de la conexión.';
             statusDiv.className = 'api-status status-error';
        }
    } catch (e) {
        console.error("Error fetching meta status:", e);
        statusDiv.innerHTML = 'Error al verificar el estado.';
        statusDiv.className = 'api-status status-error';
    }


    // 4. Fetch and display Google connection status
    const googleStatusDiv = document.getElementById('google-connection-status');
    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/auth/google/status`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            const statusData = await response.json();
            if (statusData.connected) {
                googleStatusDiv.innerHTML = `Conectado a Google Workspace.`;
                googleStatusDiv.className = 'api-status status-ok';
            } else {
                googleStatusDiv.innerHTML = 'No Conectado. Haga clic en el botón para conectar su cuenta.';
                googleStatusDiv.className = 'api-status status-error';
            }
        } else {
             googleStatusDiv.innerHTML = 'No se pudo verificar el estado de la conexión.';
             googleStatusDiv.className = 'api-status status-error';
        }
    } catch (e) {
        console.error("Error fetching google status:", e);
        googleStatusDiv.innerHTML = 'Error al verificar el estado.';
        googleStatusDiv.className = 'api-status status-error';
    }


    // 5. Add connect button listeners
    document.getElementById('meta-connect-btn').addEventListener('click', () => {
        window.location.href = `${config.apiBaseUrl}/api/v1/auth/meta/login`;
    });

    document.getElementById('google-connect-btn').addEventListener('click', () => {
        window.location.href = `${config.apiBaseUrl}/api/v1/auth/google/login`;
    });

    // 6. Add submit listener
    document.getElementById('api-keys-config-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const feedbackDiv = document.getElementById('api-keys-feedback');
        const submitButton = e.target.querySelector('button');
        submitButton.disabled = true;
        feedbackDiv.style.display = 'block';
        feedbackDiv.textContent = 'Guardando claves...';

        const payload = {
            openai_api_key: document.getElementById('openai-api-key').value,
            google_api_key: document.getElementById('google-api-key').value,
            youtube_refresh_token: document.getElementById('youtube-refresh-token').value
        };

        try {
            const response = await fetch(`${config.apiBaseUrl}/api/v1/admin_general/settings/api_keys`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(payload)
            });
            if (!response.ok) throw new Error((await response.json()).detail || 'Error del servidor.');
            feedbackDiv.className = 'message-success';
            feedbackDiv.textContent = '¡Claves guardadas con éxito!';
        } catch (error) {
            feedbackDiv.className = 'message-error';
            feedbackDiv.textContent = `Error: ${error.message}`;
        } finally {
            submitButton.disabled = false;
        }
    });
}


// --- Registrar las vistas de Administrador General en el Router ---
if (typeof registerView === 'function') {
    registerView('admin_general', 'dashboard', renderAdminGeneralDashboardView);
    registerView('admin_general', 'configuracion-whatsapp', renderConfiguracionWhatsAppView);
    registerView('admin_general', 'gestion-api-keys', renderApiKeysView);
} else {
    console.error("El sistema de registro de vistas no está disponible.");
}
