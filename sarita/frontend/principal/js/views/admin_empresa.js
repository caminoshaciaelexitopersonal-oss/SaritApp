// js/views/admin_empresa.js

function renderUserRows(users) {
    if (!users || users.length === 0) return '<tr><td colspan="5">No se encontraron usuarios.</td></tr>';
    return users.map(user => `<tr><td>${user.id}</td><td>${user.nombre_completo}</td><td>${user.correo}</td><td>${user.roles.join(', ')}</td><td><button class="btn-secondary">Editar</button><button class="btn-danger">Eliminar</button></td></tr>`).join('');
}

function renderAreaRows(areas) {
    if (!areas || areas.length === 0) return '<tr><td colspan="4">No se encontraron áreas.</td></tr>';
    return areas.map(area => `<tr><td>${area.id}</td><td>${area.nombre}</td><td>${area.descripcion || 'N/A'}</td><td><button class="btn-secondary">Editar</button><button class="btn-danger">Eliminar</button></td></tr>`).join('');
}

async function renderAdminEmpresaView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <div class="admin-dashboard">
            <h2>Panel de Administración de la Empresa</h2>
            <div id="admin-dashboard-content">
                <p>Cargando datos...</p>
            </div>
        </div>
    `;

    try {
        const [usersResponse, areasResponse] = await Promise.all([
            fetch(`${config.apiBaseUrl}/api/v1/admin/users/by-empresa`, { headers: { 'Authorization': `Bearer ${token}` } }),
            fetch(`${config.apiBaseUrl}/api/v1/admin/areas`, { headers: { 'Authorization': `Bearer ${token}` } })
        ]);

        if (!usersResponse.ok) throw new Error('No se pudo obtener la lista de usuarios.');
        if (!areasResponse.ok) throw new Error('No se pudo obtener la lista de áreas.');

        const users = await usersResponse.json();
        const areas = await areasResponse.json();

        const dashboardContent = document.getElementById('admin-dashboard-content');
        dashboardContent.innerHTML = `
            <div class="admin-section">
                <h3><i class="fas fa-users"></i> Usuarios de la Empresa</h3>
                <button class="btn-primary">Añadir Usuario</button>
                <table class="data-table">
                    <thead><tr><th>ID</th><th>Nombre Completo</th><th>Email</th><th>Roles</th><th>Acciones</th></tr></thead>
                    <tbody>${renderUserRows(users)}</tbody>
                </table>
            </div>
            <div class="admin-section">
                <h3><i class="fas fa-sitemap"></i> Áreas de la Empresa</h3>
                <button class="btn-primary">Crear Área</button>
                <table class="data-table">
                    <thead><tr><th>ID</th><th>Nombre del Área</th><th>Descripción</th><th>Acciones</th></tr></thead>
                    <tbody>${renderAreaRows(areas)}</tbody>
                </table>
            </div>
        `;
    } catch (error) {
        contentArea.innerHTML = `<p class="message-error">Error al cargar el panel de administración: ${error.message}</p>`;
    }
}

async function renderSuscripcionView(token) {
    const contentArea = document.getElementById('content-area');
    const STRIPE_PUBLISHABLE_KEY = config.STRIPE_PUBLISHABLE_KEY || "pk_test_placeholder";
    contentArea.innerHTML = `
        <div class="view-header"><h2><i class="fas fa-credit-card"></i> Suscripción y Pagos</h2></div>
        <div class="subscription-container"><div class="card">
            <h3>Plan Básico</h3><p class="price">$10.00 <span>/ mes</span></p>
            <ul><li>Feature 1</li><li>Feature 2</li></ul>
            <div id="payment-form-container">
                <p><strong>Opción 1: Pagar con Tarjeta (Stripe)</strong></p>
                <div id="payment-element"></div>
                <button id="submit-payment-btn" class="btn-primary">Pagar con Tarjeta</button>
                <div id="payment-message" class="message-info" style="display:none;"></div>
                <hr><p><strong>Opción 2: Checkout Mercado Pago</strong></p>
                <button id="submit-mercadopago-btn" class="btn-secondary">Pagar con Mercado Pago</button>
                <hr><p><strong>Opción 3: PSE</strong></p>
                <button id="submit-wompi-btn" class="btn-secondary">Pagar con PSE (Wompi)</button>
                <button id="submit-mp-pse-btn" class="btn-secondary">Pagar con PSE (Mercado Pago)</button>
            </div>
        </div></div>`;

    const messageContainer = document.getElementById('payment-message');

    // Stripe Logic
    const stripe = Stripe(STRIPE_PUBLISHABLE_KEY);
    let elements;
    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/billing/stripe/create-payment-intent`, {
            method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify({ amount: 10.00, currency: 'usd' })
        });
        if (!response.ok) throw new Error('No se pudo crear la intención de pago.');
        const { client_secret: clientSecret } = await response.json();
        elements = stripe.elements({ clientSecret });
        elements.create("payment").mount("#payment-element");
    } catch (error) {
        messageContainer.innerHTML = `<p class="message-error">No se pudo inicializar el pago con Stripe: ${error.message}</p>`;
        messageContainer.style.display = 'block';
    }
    document.getElementById('submit-payment-btn').addEventListener('click', async (e) => {
        const { error } = await stripe.confirmPayment({ elements, confirmParams: { return_url: window.location.href } });
        if (error) {
             messageContainer.textContent = error.message;
             messageContainer.style.display = 'block';
        }
    });

    // Mercado Pago Logic
    document.getElementById('submit-mercadopago-btn').addEventListener('click', async (e) => {
        try {
            const response = await fetch(`${config.apiBaseUrl}/api/v1/billing/mercadopago/create-preference`, {
                method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify({ amount: 10.00, currency: 'usd' })
            });
            if (!response.ok) throw new Error((await response.json()).detail);
            const { redirect_url } = await response.json();
            window.location.href = redirect_url;
        } catch (error) {
            messageContainer.textContent = error.message;
            messageContainer.style.display = 'block';
        }
    });

    // Mercado Pago PSE Logic
    document.getElementById('submit-mp-pse-btn').addEventListener('click', async (e) => {
        try {
            const response = await fetch(`${config.apiBaseUrl}/api/v1/billing/mercadopago/create-pse-preference`, {
                method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify({ amount: 10.00, currency: 'usd' })
            });
            if (!response.ok) throw new Error((await response.json()).detail);
            const { redirect_url } = await response.json();
            window.location.href = redirect_url;
        } catch (error) {
            messageContainer.textContent = error.message;
            messageContainer.style.display = 'block';
        }
    });

    // Wompi PSE Logic
    document.getElementById('submit-wompi-btn').addEventListener('click', async (e) => {
        try {
            const response = await fetch(`${config.apiBaseUrl}/api/v1/billing/wompi/create-transaction`, {
                method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify({ amount: 10.00, currency: 'cop' })
            });
            if (!response.ok) throw new Error((await response.json()).detail);
            const { redirect_url } = await response.json();
            window.location.href = redirect_url;
        } catch (error) {
            messageContainer.textContent = error.message;
            messageContainer.style.display = 'block';
        }
    });
}

// Register the views for this role
if (typeof registerView === 'function') {
    registerView('admin_empresa', 'panel-empresa', renderAdminEmpresaView);
    registerView('admin_empresa', 'suscripcion', renderSuscripcionView);
}
