document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('accessToken');
    const logoutBtn = document.getElementById('logout-btn');
    let currentUser = null;

    // -- 1. Proteger la ruta --
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    // -- 2. Configurar el botón de cierre de sesión --
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.clear(); // Limpiar todo al cerrar sesión
            window.location.href = 'login.html';
        });
    }

    // -- 3. Cargar datos del usuario y renderizar la aplicación --
    function initializeApp() {
        const userRoles = JSON.parse(localStorage.getItem('userRoles') || '[]');
        const userId = localStorage.getItem('userId');
        const userName = localStorage.getItem('userName'); // Cargar nombre

        if (!userRoles || !userId || !userName) {
            console.error('Información de usuario incompleta en localStorage.');
            localStorage.clear();
            window.location.href = 'login.html';
            return;
        }

        currentUser = {
            id: userId,
            name: userName,
            roles: userRoles,
            primaryRole: userRoles[0] || 'default'
        };

        renderUserInfo(currentUser);
        renderNavigation(currentUser.primaryRole);
        setupEventListeners(token, currentUser.primaryRole);
        translatePage();
        initializeNotifications();
        renderContentForView('dashboard', token, currentUser.primaryRole);
    }

    // -- 4. Configurar todos los listeners de eventos --
    function setupEventListeners(token, roleName) {
        const floatingAgentIcon = document.getElementById('floating-agent-icon');
        const closeChatBtn = document.getElementById('close-chat-btn');
        const chatForm = document.getElementById('chat-form');

        // Listeners para el chat del agente
        if (floatingAgentIcon) floatingAgentIcon.addEventListener('click', () => toggleChat(true));
        if (closeChatBtn) closeChatBtn.addEventListener('click', () => toggleChat(false));
        if (chatForm) {
            chatForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const input = document.getElementById('chat-input');
                if (input.value.trim()) {
                    sendChatMessage(input.value, token);
                    input.value = '';
                }
            });
        }

        // --- Lógica de Grabación de Voz ---
        const micBtn = document.getElementById('chat-mic-btn');
        let mediaRecorder;
        let audioChunks = [];
        let isRecording = false;

        if (micBtn) {
            micBtn.addEventListener('click', async () => {
                if (!isRecording) {
                    try {
                        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                        mediaRecorder = new MediaRecorder(stream);

                        mediaRecorder.ondataavailable = (event) => {
                            audioChunks.push(event.data);
                        };

                        mediaRecorder.onstop = async () => {
                            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                            audioChunks = [];
                            sendAudioMessage(audioBlob, token);
                            // Detener las pistas de medios para que el ícono del navegador desaparezca
                            stream.getTracks().forEach(track => track.stop());
                        };

                        mediaRecorder.start();
                        isRecording = true;
                        micBtn.style.color = 'red'; // Indicate recording
                        micBtn.querySelector('i').classList.add('fa-beat');
                        addMessageToLog('Grabando... habla ahora. Pulsa de nuevo para enviar.', 'agent');

                    } catch (err) {
                        console.error("Error al acceder al micrófono:", err);
                        addMessageToLog('Error: No se pudo acceder al micrófono.', 'agent');
                    }
                } else {
                    mediaRecorder.stop();
                    isRecording = false;
                    micBtn.style.color = ''; // Revert color
                    micBtn.querySelector('i').classList.remove('fa-beat');
                }
            });
        }

        // Listeners existentes
        const navContainer = document.getElementById('app-nav');
        const langSelect = document.getElementById('language-select');
        const themeToggle = document.getElementById('theme-toggle');

        if (navContainer) {
            navContainer.addEventListener('click', (e) => {
                const link = e.target.closest('a[data-view]');
                if (link) {
                    e.preventDefault();
                    const viewName = link.dataset.view;
                    if (viewName) {
                        console.log(`Navigating to view: ${viewName}`);
                        renderContentForView(viewName, token, roleName);
                    }
                }
            });
        }
        if (langSelect) langSelect.addEventListener('change', (e) => setLanguage(e.target.value));

        // Lógica del Theme Switcher
        function applyTheme(theme) {
            document.body.setAttribute('data-theme', theme);
            if (themeToggle) themeToggle.checked = theme === 'dark';
        }
        function toggleTheme() {
            const newTheme = document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            localStorage.setItem('theme', newTheme);
            applyTheme(newTheme);
        }
        if (themeToggle) themeToggle.addEventListener('change', toggleTheme);
        const savedTheme = localStorage.getItem('theme') || 'light';
        applyTheme(savedTheme);
    }

    // -- 5. Lógica para el Agente de IA y Chat --
    let chatInitiated = false;

    function toggleChat(show) {
        const chatContainer = document.getElementById('agent-chat-container');
        if (!chatContainer) return;

        if (show) {
            chatContainer.style.display = 'flex';
            if (!chatInitiated) {
                startAgentConversation(token);
                chatInitiated = true;
            }
        } else {
            chatContainer.style.display = 'none';
        }
    }

    function addMessageToLog(messageContent, sender) {
        const chatLog = document.getElementById('chat-log');
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-message ${sender}`;

        // Revisa si el contenido es un objeto con una imagen
        if (typeof messageContent === 'object' && messageContent.image_url) {
            // Renderiza el texto y la imagen
            const textP = document.createElement('p');
            textP.textContent = messageContent.text;
            msgDiv.appendChild(textP);

            const img = document.createElement('img');
            // La URL del backend será algo como /static/charts/uuid.png
            // El servidor de desarrollo está en http://127.0.0.1:8000
            img.src = `${config.apiBaseUrl}${messageContent.image_url}`;
            img.alt = 'Gráfico generado por IA';
            img.className = 'chat-image';
            msgDiv.appendChild(img);

        } else {
            // Si no, solo renderiza texto
            msgDiv.textContent = messageContent.text || messageContent;
        }

        chatLog.appendChild(msgDiv);
        chatLog.scrollTop = chatLog.scrollHeight; // Auto-scroll
    }

    async function startAgentConversation(authToken) {
        addMessageToLog('Conectando con el asistente...', 'agent');
        // El prompt inicial ahora está vacío para indicar que es el inicio
        await sendChatMessage("", authToken, true);
    }

    async function sendAudioMessage(audioBlob, authToken) {
        addMessageToLog('Enviando audio...', 'user');
        try {
            const formData = new FormData();
            formData.append('audio_file', audioBlob, 'grabacion.webm');
            const response = await fetch(`${config.apiBaseUrl}/api/v1/agent/invoke-voice`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${authToken}` },
                body: formData
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al procesar el audio.');
            }
            const structuredResponse = await response.json();
            addMessageToLog(structuredResponse, 'agent');
            speakText(structuredResponse.text);
        } catch (error) {
            addMessageToLog({ text: `Error: ${error.message}` }, 'agent');
        }
    }

    async function sendChatMessage(prompt, authToken, isInitial = false) {
        if (!isInitial) {
            addMessageToLog(prompt, 'user');
        }
        try {
            const response = await fetch(`${config.apiBaseUrl}/api/v1/agent/invoke`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${authToken}` },
                body: JSON.stringify({
                    prompt: prompt,
                    area: "Cultura", // Hardcodeado a Cultura para probar el agente con herramientas
                    thread_id: `user_${currentUser.id}`
                })
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error del servidor.');
            }
            const structuredResponse = await response.json(); // La respuesta ahora es {text, image_url}
            addMessageToLog(structuredResponse, 'agent');
            speakText(structuredResponse.text);
        } catch (error) {
            addMessageToLog({ text: `Error de conexión con el agente: ${error.message}` }, 'agent');
        }
    }

    // -- 6. Funciones de Renderizado y Utilidades --
    function renderUserInfo(user) {
        const userInfoDiv = document.getElementById('user-info');
        if (userInfoDiv) {
            userInfoDiv.innerHTML = `
                <p><strong>${user.name}</strong></p>
                <span>${user.roles.join(', ')}</span>
            `;
        }
    }

    function initializeNotifications() { /* ... (código existente) */ }

    // -- 7. Lógica de Text-to-Speech (TTS) y Vibración --
    function speakText(text) {
        if ('speechSynthesis' in window) {
            const floatingIcon = document.getElementById('floating-agent-icon');
            window.speechSynthesis.cancel();

            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'es-ES';
            utterance.volume = 1;
            utterance.rate = 1;
            utterance.pitch = 1;

            utterance.onstart = () => {
                if (floatingIcon) floatingIcon.classList.add('is-speaking');
            };

            utterance.onend = () => {
                if (floatingIcon) floatingIcon.classList.remove('is-speaking');
            };

            window.speechSynthesis.speak(utterance);
        } else {
            console.warn('La API de Web Speech no es soportada por este navegador.');
        }
    }

    // Iniciar la aplicación
    initializeApp();
});
