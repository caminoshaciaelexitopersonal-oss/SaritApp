// --- Definición de la Estructura de Navegación por Rol ---

const navLinks = {
    // Rol 1: Super Admin
    admin_general: [
        { text: 'Dashboard', view: 'dashboard', icon: 'fa-home' },
        { text: 'Gestión de Marca', view: 'gestion-de-marca', icon: 'fa-palette' },
        { text: 'Config. WhatsApp', view: 'configuracion-whatsapp', icon: 'fab fa-whatsapp' },
        { text: 'Gestión de Claves API', view: 'gestion-api-keys', icon: 'fa-key' },
        { text: 'Calendario de Contenidos', view: 'calendario-de-contenidos', icon: 'fa-calendar-alt' },
        { text: 'Gestionar Empresas', icon: 'fa-building' },
        { text: 'Roles y Permisos', icon: 'fa-shield-alt' },
        { text: 'Verificar Roles BD', icon: 'fa-database' },
        { text: 'Auditoría General', icon: 'fa-history' },
        { text: 'Gestión de Cobros', icon: 'fa-credit-card' },
        { text: 'Promociones', icon: 'fa-tags' },
        { text: 'Asistente de IA', icon: 'fa-robot' }
    ],
    // Rol 2: Admin de Empresa
    admin_empresa: [
        { text: 'Panel de Empresa', view: 'panel-empresa', icon: 'fa-tachometer-alt' },
        { text: 'Suscripción y Pagos', view: 'suscripcion', icon: 'fa-credit-card' },
        { text: 'Reportes', view: 'reportes-empresa', icon: 'fa-chart-bar' },
        { text: 'Auditoría', view: 'auditoria-empresa', icon: 'fa-history' },
        { text: 'Configuración', view: 'config-empresa', icon: 'fa-cog' }
    ],
    // Rol 3: Jefe de Área
    jefe_area: [
        { text: 'Panel de Área', view: 'panel-area', icon: 'fa-tachometer-alt' },
        { text: 'Reportes', view: 'reportes-area', icon: 'fa-chart-pie' },
        { text: 'Configuración', view: 'config-area', icon: 'fa-cog' }
    ],
    // Rol 4: Profesional de Área
    profesional_area: [
        { text: 'Dashboard', icon: 'fa-tachometer-alt' },
        { text: 'Supervisar Actividades', icon: 'fa-tasks' },
        { text: 'Gestionar Eventos', icon: 'fa-calendar-plus' },
        { text: 'Gestionar Disciplinas', icon: 'fa-edit' },
        { text: 'Reportes', icon: 'fa-chart-line' }
    ],
    // Rol 5: Técnico o Asistente de Área
    tecnico_area: [
        { text: 'Dashboard', icon: 'fa-tachometer-alt' },
        { text: 'Ver Actividades', icon: 'fa-eye' },
        { text: 'Gestionar Eventos', icon: 'fa-calendar-check' },
        { text: 'Ver Disciplinas', icon: 'fa-search' },
        { text: 'Reportes', icon: 'fa-file-alt' }
    ],
    // Rol 6: Coordinador
    coordinador: [
        { text: 'Planificación', view: 'planificacion', icon: 'fa-calendar-day' },
        { text: 'Verificar Programación', view: 'verificar-programacion', icon: 'fa-clipboard-check' },
        { text: 'Aprobaciones', view: 'aprobaciones', icon: 'fa-check-double' },
        { text: 'Gestionar Misiones', view: 'misiones', icon: 'fa-tasks' }
    ],
    // Rol 7: Profesor
    profesor: [
        { text: 'Gestionar Cursos', view: 'gestionar-cursos', icon: 'fa-chalkboard-teacher' },
        { text: 'Gestionar Alumnos', view: 'gestionar-alumnos', icon: 'fa-user-graduate' },
        { text: 'Calificaciones', view: 'calificaciones', icon: 'fa-marker' },
        { text: 'Gamificación', view: 'gamificacion', icon: 'fa-trophy' }
    ],
    // Rol 8: Alumno
    alumno: [
        { text: 'Mis Cursos', view: 'mis-cursos', icon: 'fa-book-reader' },
        { text: 'Mi Horario', view: 'mi-horario', icon: 'fa-clock' },
        { text: 'Mis Calificaciones', view: 'mis-calificaciones', icon: 'fa-star' },
        { text: 'Mi Progreso', view: 'mi-progreso', icon: 'fa-gamepad' },
        { text: 'Misiones', view: 'misiones', icon: 'fa-tasks' },
        { text: 'Mercado de Puntos', view: 'mercado', icon: 'fa-store' }
    ],
    // Rol 9: Padre o Acudiente
    padre_acudiente: [
        { text: 'Mis Alumnos', icon: 'fa-child' },
        { text: 'Inscripciones', icon: 'fa-file-signature' },
        { text: 'Autorizaciones', icon: 'fa-user-edit' },
        { text: 'Reportes de Progreso', icon: 'fa-chart-bar' }
    ],
    // Rol 10: Jefe de Almacén
    jefe_almacen: [
        { text: 'Dashboard Inventario', icon: 'fa-boxes' },
        { text: 'Registrar Movimientos', icon: 'fa-dolly-flatbed' },
        { text: 'Stock y Reposición', icon: 'fa-sort-amount-up' },
        { text: 'Hojas de Vida', icon: 'fa-file-invoice' },
        { text: 'Reportes de Inventario', icon: 'fa-file-excel' }
    ],
    // Rol 11: Almacenista (hereda de jefe_almacen, pero con menos permisos)
    almacenista: [
        { text: 'Ver Inventario', icon: 'fa-boxes' },
        { text: 'Registrar Movimientos', icon: 'fa-dolly-flatbed' }
    ],
    // Rol 12: Jefe de Escenarios
    jefe_escenarios: [
        { text: 'Calendario de Escenarios', icon: 'fa-calendar-alt' },
        { text: 'Asignar Espacios', icon: 'fa-map-marker-alt' },
        { text: 'Mantenimiento', icon: 'fa-tools' }
    ],
    // Rol por defecto si no se encuentra uno
    default: [
        { text: 'Mi Perfil', icon: 'fa-user' }
    ]
};

function renderNavigation(roleName) {
    const navContainer = document.getElementById('app-nav');
    if (!navContainer) return;

    const links = navLinks[roleName] || navLinks.default;

    let navHtml = '';
    links.forEach(link => {
        // Usar la propiedad 'view' si existe, si no, generar desde el texto
        const viewName = link.view || link.text.toLowerCase().replace(/ /g, '-');
        navHtml += `<a href="#" data-view="${viewName}">
                        <i class="fas ${link.icon}"></i>
                        <span>${link.text}</span>
                    </a>`;
    });

    navContainer.innerHTML = navHtml;
}
