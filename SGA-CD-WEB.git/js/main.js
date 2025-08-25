document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Load All Dynamic Content from the API ---
    async function loadAndRenderContent() {
        try {
            const response = await fetch('/api/website/content');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const content = await response.json();

            // Render each section with the fetched data
            renderSlider(content.slider);
            renderVideo(content.contact.video_url);
            renderFeatures(content.features);
            renderPartners(content.partners);
            renderFaq(content.faq);
            renderPlans(content.plans);
            renderLaunchOffer(content.contact.launch_offer_text);
            renderFooter(content.contact);

            // --- 2. Initialize Animations AFTER content is rendered ---
            initializeAnimations();

        } catch (error) {
            console.error("Failed to load website content:", error);
            // Optionally, display an error message to the user on the page
            const main = document.querySelector('main');
            main.innerHTML = '<p style="text-align: center; color: red;">No se pudo cargar el contenido del sitio. Por favor, intente de nuevo más tarde.</p>';
        }
    }

    // --- RENDER FUNCTIONS ---
    function renderSlider(sliderItems) {
        const sliderContainer = document.getElementById('hero-slider');
        if (!sliderContainer || sliderItems.length === 0) return;

        sliderItems.forEach(item => {
            const slide = document.createElement('div');
            slide.className = 'slide'; // Add styles for this class
            if (item.tipo === 'image') {
                slide.innerHTML = `<img src="${item.url}" alt="${item.titulo || ''}" />`;
            } else if (item.tipo === 'video') {
                slide.innerHTML = `<video autoplay muted loop playsinline><source src="${item.url}" type="video/mp4"></video>`;
            }

            if(item.titulo || item.subtitulo) {
                const overlay = document.createElement('div');
                overlay.className = 'slide-overlay';
                overlay.innerHTML = `
                    <h2>${item.titulo || ''}</h2>
                    <p>${item.subtitulo || ''}</p>
                `;
                slide.appendChild(overlay);
            }
            sliderContainer.appendChild(slide);
        });
        // Basic slider logic (e.g., fade between slides) can be added here
    }

    function renderFeatures(features) {
        const grid = document.getElementById('features-grid');
        if (!grid) return;
        grid.innerHTML = ''; // Clear existing
        features.forEach(feature => {
            const card = document.createElement('div');
            card.className = 'feature-card';
            card.innerHTML = `
                ${feature.icono ? `<i class="${feature.icono}"></i>` : ''}
                <h3>${feature.titulo}</h3>
                <p>${feature.descripcion}</p>
            `;
            grid.appendChild(card);
        });
    }

    function renderVideo(videoUrl) {
        const container = document.getElementById('video-container');
        if (!container || !videoUrl) return;

        let videoId = '';
        if (videoUrl.includes('youtube.com/watch?v=')) {
            videoId = videoUrl.split('v=')[1].split('&')[0];
        } else if (videoUrl.includes('youtu.be/')) {
            videoId = videoUrl.split('youtu.be/')[1].split('?')[0];
        }

        if (videoId) {
            container.innerHTML = `
                <iframe
                    src="https://www.youtube.com/embed/${videoId}"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen>
                </iframe>`;
        }
    }

    function renderPartners(partners) {
        const clientsGrid = document.getElementById('clients-grid');
        const testersGrid = document.getElementById('testers-grid');
        if (!clientsGrid || !testersGrid) return;

        clientsGrid.innerHTML = '';
        testersGrid.innerHTML = '';

        partners.forEach(partner => {
            const partnerLogo = document.createElement('div');
            partnerLogo.className = 'partner-logo';
            let innerHTML = `<img src="${partner.logo_url}" alt="${partner.nombre}">`;
            if (partner.website_url) {
                innerHTML = `<a href="${partner.website_url}" target="_blank" rel="noopener noreferrer">${innerHTML}</a>`;
            }
            partnerLogo.innerHTML = innerHTML;

            if (partner.tipo === 'cliente') {
                clientsGrid.appendChild(partnerLogo);
            } else if (partner.tipo === 'prueba') {
                testersGrid.appendChild(partnerLogo);
            }
        });
    }

    function renderPlans(plans) {
        const grid = document.getElementById('pricing-grid');
        if (!grid) return;
        grid.innerHTML = '';

        plans.forEach(plan => {
            const card = document.createElement('div');
            card.className = 'plan-card' + (plan.recomendado ? ' recommended' : '');

            let featuresHtml = '';
            if (plan.caracteristicas) {
                try {
                    const features = JSON.parse(plan.caracteristicas);
                    featuresHtml = features.map(f => `<li>${f}</li>`).join('');
                } catch (e) {
                    console.error("Could not parse plan features JSON:", e);
                }
            }

            card.innerHTML = `
                ${plan.recomendado ? '<div class="recommended-badge">Recomendado</div>' : ''}
                <h3>${plan.nombre}</h3>
                <p class="price">${plan.precio_mensual ? `$${plan.precio_mensual}/mes` : 'Gratis'}</p>
                ${plan.precio_anual ? `<p>o $${plan.precio_anual}/año</p>` : ''}
                <p>${plan.descripcion || ''}</p>
                <ul>${featuresHtml}</ul>
                <a href="register.html" class="plan-button">Empezar</a>
            `;
            grid.appendChild(card);
        });
    }

    function renderLaunchOffer(offerText) {
        const container = document.getElementById('launch-offer-container');
        if (!container || !offerText) return;
        container.innerHTML = `<p>${offerText}</p>`;
    }

    function renderFaq(faqs) {
        const container = document.getElementById('faq-container');
        if (!container) return;
        container.innerHTML = '';

        // If the backend provides faqs, use them. Otherwise, use the new defaults.
        const faqData = faqs.length > 0 ? faqs : [
            { pregunta: "¿Qué es SGA-CD?", respuesta: "Es un Sistema de Gestión Académica enfocado en centros de formación cultural y deportiva, que centraliza la administración de alumnos, clases, escenarios y más." },
            { pregunta: "¿Cómo funciona la oferta de lanzamiento?", respuesta: "Recomienda a 10 usuarios de la app o 10 empresas para el sistema de escritorio y obtendrás 6 meses de servicio totalmente gratis." },
            { pregunta: "¿Qué métodos de pago aceptan?", respuesta: "Aceptamos todas las tarjetas de crédito principales y pagos a través de PSE para Colombia." },
            { pregunta: "¿El sistema es seguro?", respuesta: "Sí, la seguridad es nuestra prioridad. Usamos encriptación para toda la información sensible y seguimos las mejores prácticas de la industria." },
            { pregunta: "¿Puedo cancelar mi suscripción en cualquier momento?", respuesta: "Sí, puedes cancelar tu suscripción cuando quieras desde el panel de administración de tu empresa." },
            { pregunta: "¿Ofrecen soporte técnico?", respuesta: "Sí, todos nuestros planes incluyen soporte técnico por correo electrónico, y los planes de pago tienen soporte prioritario." },
            { pregunta: "¿El sistema se puede personalizar?", respuesta: "Ofrecemos varias opciones de personalización. Para requerimientos más específicos, contacta a nuestro equipo de ventas." },
            { pregunta: "¿Cómo se gestionan los datos de los alumnos?", respuesta: "Todos los datos se gestionan de forma segura y privada por cada empresa (inquilino). Tú tienes el control total sobre la información de tus usuarios." },
            { pregunta: "¿La aplicación móvil está disponible para iOS y Android?", respuesta: "Actualmente nuestra aplicación está disponible en la Google Play Store para Android. Estamos trabajando en la versión para iOS." },
            { pregunta: "¿Qué pasa cuando mi período de prueba termina?", respuesta: "Se te invitará a elegir uno de nuestros planes de pago para continuar usando el servicio sin interrupciones." }
        ];

        faqData.forEach(faq => {
            const faqItem = document.createElement('div');
            faqItem.className = 'faq-item';
            faqItem.innerHTML = `
                <button class="faq-question">${faq.pregunta}</button>
                <div class="faq-answer">
                    <p>${faq.respuesta}</p>
                </div>
            `;
            container.appendChild(faqItem);
        });
        // Add event listeners for accordion functionality
        container.querySelectorAll('.faq-question').forEach(button => {
            button.addEventListener('click', () => {
                const answer = button.nextElementSibling;
                button.classList.toggle('active');
                if (answer.style.maxHeight) {
                    answer.style.maxHeight = null;
                } else {
                    answer.style.maxHeight = answer.scrollHeight + "px";
                }
            });
        });
    }

    function renderFooter(contact) {
        const companyContainer = document.getElementById('company-info');
        const contactContainer = document.getElementById('contact-info');
        const socialContainer = document.getElementById('social-media');
        const footer = document.getElementById('main-footer');

        if (companyContainer) {
            companyContainer.innerHTML = `
                <h4>${contact.nombre_empresa || 'SGA-CD'}</h4>
                <h5>Misión</h5>
                <p>${contact.mission || ''}</p>
                <h5>Visión</h5>
                <p>${contact.vision || ''}</p>
            `;
        }
        if (contactContainer) {
            contactContainer.innerHTML = `
                <h4>Contacto</h4>
                <p>${contact.direccion || ''}</p>
                <p>Email: <a href="mailto:${contact.email_contacto}">${contact.email_contacto || ''}</a></p>
                <p>Tel: ${contact.telefono_contacto || ''}</p>
            `;
        }
        if (socialContainer) {
            socialContainer.innerHTML = `
                <h4>Redes</h4>
                ${contact.url_facebook ? `<a href="${contact.url_facebook}" target="_blank">Facebook</a>` : ''}
                ${contact.url_twitter ? `<a href="${contact.url_twitter}" target="_blank">Twitter</a>` : ''}
                ${contact.url_instagram ? `<a href="${contact.url_instagram}" target="_blank">Instagram</a>` : ''}
                ${contact.url_linkedin ? `<a href="${contact.url_linkedin}" target="_blank">LinkedIn</a>` : ''}
            `;
        }
        if (footer) {
            const year = new Date().getFullYear();
            const copy = document.createElement('p');
            copy.className = 'footer-copy';
            copy.innerHTML = `&copy; ${year} ${contact.nombre_empresa || 'SGA-CD'}. Todos los derechos reservados.`;
            footer.appendChild(copy);
        }
    }

    // --- 3. Initialize Other Page Logic ---
    function initializeAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, {
            threshold: 0.1
        });
        const cards = document.querySelectorAll('.feature-card, .plan-card');
        cards.forEach(card => observer.observe(card));
    }

    function initializeAIAgent() {
        const toggleButton = document.getElementById('ai-agent-toggle');
        const chatbox = document.getElementById('ai-agent-chatbox');
        const messagesContainer = document.getElementById('chatbox-messages');
        const sendButton = document.getElementById('chatbox-send');
        const inputField = document.getElementById('chatbox-input');

        if (!toggleButton) return;

        toggleButton.addEventListener('click', () => {
            chatbox.classList.toggle('hidden');
            if (!chatbox.classList.contains('hidden') && messagesContainer.children.length === 0) {
                addMessage('agent', '¡Hola! Soy el asistente virtual. ¿Cómo puedo ayudarte a conocer nuestra plataforma?');
            }
        });

        sendButton.addEventListener('click', sendMessage);
        inputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });

        function sendMessage() {
            const messageText = inputField.value.trim();
            if (messageText === '') return;
            addMessage('user', messageText);
            inputField.value = '';
            sendMessageToAgent(messageText);
        }

        function addMessage(sender, text) {
            const messageElement = document.createElement('div');
            messageElement.classList.add('chat-message', `${sender}-message`);
            messageElement.textContent = text;
            messagesContainer.appendChild(messageElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        async function sendMessageToAgent(message) {
            const API_ENDPOINT = '/api/sales_agent';
            addMessage('agent', '...');
            try {
                const response = await fetch(API_ENDPOINT, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: message }),
                });
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                const data = await response.json();
                messagesContainer.removeChild(messagesContainer.lastChild);
                addMessage('agent', data.reply);
            } catch (error) {
                console.error('Error sending message to agent:', error);
                messagesContainer.removeChild(messagesContainer.lastChild);
                addMessage('agent', 'Lo siento, estoy teniendo problemas para conectarme.');
            }
        }
    }

    function initializeServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/service-worker.js')
            .then(reg => console.log('Service Worker registered', reg))
            .catch(err => console.log('Service Worker registration failed', err));
        }
    }

    // --- App Initialization ---
    loadAndRenderContent();
    initializeAIAgent();
    initializeServiceWorker();
});
