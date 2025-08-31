/* ==========================================================================
   Archivo de Vistas Principales SGA-CD
   Recreado por Jules para resolver un error de sintaxis fatal.
   Contiene solo la lógica esencial del router y las vistas que no
   están en módulos individuales (ej. la vista de admin_general).
   ========================================================================== */

/* --- Config defensiva --- */
const config = (typeof window !== 'undefined' && window.config) ? window.config : {
  apiBaseUrl: '/api'
};

/* ==========================================================================
   Lógica Mejorada para el Modal Genérico
   ========================================================================== */

/**
 * Abre el modal con un título y contenido específico.
 * Esta función es segura de usar porque busca los elementos del DOM cada vez que se llama.
 * @param {string} title - El título a mostrar en el header del modal.
 * @param {string} bodyContent - El contenido HTML a insertar en el cuerpo del modal.
 */
function openModal(title, bodyContent) {
    const modal = document.getElementById('generic-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');

    if (!modal || !modalTitle || !modalBody) {
        console.error("No se encontraron los elementos del modal en el DOM.");
        // Fallback de emergencia si el modal no existe.
        alert(`${title}\n\n${(bodyContent || '').replace(/<[^>]*>/g, '')}`);
        return;
    }

    modalTitle.textContent = title;
    modalBody.innerHTML = bodyContent;
    modal.style.display = 'flex'; // Usar flex para centrar, como en la app principal.
}

/**
 * Cierra el modal y limpia su contenido para evitar datos residuales.
 */
function closeModal() {
    const modal = document.getElementById('generic-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');

    if (modal) { modal.style.display = 'none'; }
    if (modalTitle) { modalTitle.textContent = ''; }
    if (modalBody) { modalBody.innerHTML = ''; }
}

/**
 * Configura los listeners para el modal.
 * Se debe llamar una vez que el DOM esté completamente cargado.
 */
function setupModalListeners() {
    const modal = document.getElementById('generic-modal');
    // El botón de cierre en app.html tiene id 'modal-close-btn' pero el css lo selecciona como .modal-close
    const closeModalButton = document.getElementById('modal-close-btn') || document.querySelector('.modal-close');

    if (closeModalButton) {
        closeModalButton.addEventListener('click', closeModal);
    }

    // Cierra el modal si se hace clic en el overlay (el fondo oscuro)
    if (modal) {
        modal.addEventListener('click', (event) => {
            if (event.target.id === 'generic-modal') {
                closeModal();
            }
        });
    }
}

// Aseguramos que los listeners se configuren solo cuando el DOM esté listo.
// Esto evita errores si el script se carga antes de que el HTML del modal exista.
document.addEventListener('DOMContentLoaded', setupModalListeners);


/* ==========================================================================
   Router principal de vistas
   ========================================================================== */
async function renderContentForView(viewName, token, roleName = 'default') {
  const contentArea = document.getElementById('content-area');
  if (!contentArea) {
    console.error("El área de contenido principal #content-area no fue encontrada.");
    return;
  }

  contentArea.innerHTML = '<h2>Cargando...</h2>';

  try {
    switch (viewName) {
      // Vistas para admin_general
      case 'verificar-roles-bd':
        contentArea.innerHTML = await getVerificarRolesView(token);
        setupVerificarRolesListeners(token);
        break;

      // Vistas de Gamificación Social
      case 'misiones':
        await renderMisionesView(token);
        break;

      case 'mercado':
        await renderMercadoView(token);
        break;

      // Se pueden añadir otros casos aquí si es necesario para vistas
      // que no tengan su propio archivo modular.
      default:
        setTimeout(() => {
            if(contentArea.innerHTML === '<h2>Cargando...</h2>') {
                 contentArea.innerHTML = `<h2>Vista no encontrada: ${viewName}</h2><p>La vista solicitada no fue encontrada o no está configurada en el router principal.</p>`;
            }
        }, 500);
        break;
    }
  } catch (error) {
    console.error(`Error al renderizar la vista ${viewName}:`, error);
    contentArea.innerHTML = `<p style="color: red;">Error al cargar el contenido: ${error.message}</p>`;
  }
}

/* ==========================================================================
   Funciones de la Vista para Admin General
   ========================================================================== */

async function fetchRoles(token) {
  try {
    const res = await fetch(`${config.apiBaseUrl}/api/v1/roles`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!res.ok) throw new Error('No se pudieron obtener roles');
    return await res.json();
  } catch (e) {
    console.error("Error en fetchRoles:", e);
    return []; // Devuelve un array vacío en caso de error para no romper la renderización
  }
}

async function getVerificarRolesView(token) {
  const roles = await fetchRoles(token);
  const rolesRequeridos = ['admin_general', 'admin_empresa', 'jefe_area', 'profesional_area', 'tecnico_area', 'coordinador', 'profesor', 'alumno', 'padre_acudiente', 'jefe_almacen', 'almacenista', 'jefe_escenarios'];

  const faltantes = rolesRequeridos.filter(r => !(roles || []).some(x => x.nombre === r));

  const rows = (roles || []).map(r => `
    <tr>
      <td>${r.id ?? '—'}</td>
      <td>${r.nombre ?? 'N/A'}</td>
      <td>${r.descripcion ?? '—'}</td>
    </tr>
  `).join('');

  const faltHtml = faltantes.length
    ? `<div class="missing-roles">${faltantes.map(n => `<button class="btn-primary btn-crear-rol" data-rol-nombre="${n}">Crear rol: ${n}</button>`).join(' ')}</div>`
    : '<p class="message-success">¡Excelente! Todos los roles requeridos existen en la base de datos.</p>';

  return `
    <div class="view-header">
        <h2><i class="fas fa-user-shield"></i> Verificar Roles en la BD</h2>
    </div>
    <table class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Descripción</th>
        </tr>
      </thead>
      <tbody>
        ${rows || '<tr><td colspan="3">No se encontraron roles.</td></tr>'}
      </tbody>
    </table>
    <div class="actions-footer">
        <h3>Roles Faltantes</h3>
        ${faltHtml}
    </div>
  `;
}

function setupVerificarRolesListeners(token) {
  const contentArea = document.getElementById('content-area');
  if (!contentArea) return;

  contentArea.addEventListener('click', async (e) => {
    if (e.target.classList.contains('btn-crear-rol')) {
      const rolNombre = e.target.dataset.rolNombre;

      const modalBodyContent = `
        <form id="crear-rol-form">
          <p>Estás a punto de crear el rol que falta:</p>
          <input type="text" id="rol-nombre-input" class="form-input" value="${rolNombre}" readonly>
          <textarea id="rol-descripcion-input" class="form-textarea" placeholder="Añade una descripción para el rol..." required></textarea>
          <div class="form-actions">
            <button type="submit" class="btn-primary">Confirmar Creación</button>
          </div>
        </form>
        <div id="modal-feedback" class="modal-feedback"></div>
      `;

      openModal(`Crear Rol: ${rolNombre}`, modalBodyContent);

      const form = document.getElementById('crear-rol-form');
      form.addEventListener('submit', async (submitEvent) => {
        submitEvent.preventDefault();
        const feedbackDiv = document.getElementById('modal-feedback');
        feedbackDiv.textContent = 'Creando rol...';
        feedbackDiv.className = 'modal-feedback message-info';

        try {
          const response = await fetch(`${config.apiBaseUrl}/api/v1/roles`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
              nombre: rolNombre,
              descripcion: document.getElementById('rol-descripcion-input').value
            })
          });

          const result = await response.json();

          if (response.ok) {
            feedbackDiv.className = 'modal-feedback message-success';
            feedbackDiv.textContent = '¡Rol creado exitosamente! La vista se refrescará.';
            setTimeout(() => {
              closeModal();
              renderContentForView('verificar-roles-bd', token);
            }, 1200);
          } else {
            throw new Error(result.detail || 'Error desconocido del servidor');
          }
        } catch (error) {
          feedbackDiv.className = 'modal-feedback message-error';
          feedbackDiv.textContent = `Error: ${error.message}`;
        }
      });
    }
  });
}

/* ==========================================================================
   Placeholder / Helper Views (mocks)
   ========================================================================== */

// Estas funciones son placeholders y deben reemplazarse por implementaciones reales
// si las vistas 'misiones' o 'mercado' están desarrolladas en módulos separados.

async function renderMisionesView(token) {
  const contentArea = document.getElementById('content-area');
  if (!contentArea) return;
  contentArea.innerHTML = `<h2>Misiónes (Proximamente)</h2><p>Contenido de misiones aún no modularizado.</p>`;
}

async function renderMercadoView(token) {
  const contentArea = document.getElementById('content-area');
  if (!contentArea) return;
  contentArea.innerHTML = `<h2>Mercado (Proximamente)</h2><p>Contenido de mercado aún no modularizado.</p>`;
}