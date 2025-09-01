document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const messageDiv = document.getElementById('login-mensaje');

    // Redirigir si el usuario ya está logueado
    if (localStorage.getItem('accessToken')) {
        window.location.href = 'app.html';
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            if (!username || !password) {
                showMessage('Por favor, ingresa usuario y contraseña.', 'error');
                return;
            }

            showMessage('Iniciando sesión...', 'info');

            try {
                // El endpoint correcto es /api/v1/auth/login
                const response = await fetch(`${config.apiBaseUrl}/api/v1/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
                });

                const data = await response.json();

                if (response.ok) {
                    if (data.access_token) {
                        // Guardar el token
                        localStorage.setItem('accessToken', data.access_token);
                        localStorage.setItem('refreshToken', data.refresh_token);

                        // Decodificar el token para obtener los roles del usuario
                        try {
                            const payloadBase64 = data.access_token.split('.')[1];
                            const decodedPayload = JSON.parse(atob(payloadBase64));

                            // Guardar la información del usuario en localStorage
                            localStorage.setItem('userRoles', JSON.stringify(decodedPayload.roles || []));
                            localStorage.setItem('userId', decodedPayload.sub);
                            localStorage.setItem('userInquilinoId', decodedPayload.inquilino_id);
                            localStorage.setItem('userName', decodedPayload.nombre_completo || '');

                            console.log('Roles de usuario:', decodedPayload.roles);
                            console.log('Nombre de usuario:', decodedPayload.nombre_completo);

                        } catch (e) {
                            console.error('Error decodificando el token:', e);
                            showMessage('Error al procesar la información del usuario.', 'error');
                            return;
                        }

                        showMessage('Inicio de sesión exitoso. Redirigiendo...', 'success');
                        setTimeout(() => {
                            window.location.href = 'app.html';
                        }, 1500);
                    } else {
                        showMessage('Respuesta inesperada del servidor.', 'error');
                    }
                } else {
                    showMessage(data.detail || 'Credenciales inválidas.', 'error');
                }

            } catch (error) {
                console.error('Error de inicio de sesión:', error);
                showMessage('No se pudo conectar con el servidor.', 'error');
            }
        });
    }

    function showMessage(message, type) {
        if (messageDiv) {
            messageDiv.textContent = message;
            messageDiv.className = `message-${type}`;
        }
    }
});
