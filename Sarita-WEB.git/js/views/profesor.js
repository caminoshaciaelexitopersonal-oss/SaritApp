async function renderProfesorView(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <div class="profesor-dashboard">
            <h2>Panel del Profesor</h2>
            <div id="profesor-cursos-container">
                <h3>Mis Cursos</h3>
                <p>Cargando cursos...</p>
            </div>
            <div id="profesor-alumnos-container" style="margin-top: 2rem;">
                <!-- Los detalles de los alumnos se mostrarán aquí -->
            </div>
        </div>
    `;

    try {
        const response = await fetch(`${config.apiBaseUrl}/api/v1/profesor/courses`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error('No se pudo obtener la lista de cursos.');

        const courses = await response.json();
        const coursesContainer = document.getElementById('profesor-cursos-container');

        coursesContainer.innerHTML = `
            <h3>Mis Cursos</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre del Curso</th>
                        <th>Descripción</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    ${renderCourseRows(courses)}
                </tbody>
            </table>
        `;

        // Add event listeners after rendering
        setupProfesorViewListeners(token);

    } catch (error) {
        console.error('Error rendering profesor view:', error);
        contentArea.innerHTML = `<p class="message-error">Error al cargar el panel del profesor: ${error.message}</p>`;
    }
}

function renderCourseRows(courses) {
    if (!courses || courses.length === 0) {
        return '<tr><td colspan="4">No tienes cursos asignados.</td></tr>';
    }
    return courses.map(course => `
        <tr>
            <td>${course.id}</td>
            <td>${course.nombre}</td>
            <td>${course.descripcion || 'N/A'}</td>
            <td>
                <button class="btn-primary btn-ver-alumnos" data-course-id="${course.id}" data-course-name="${course.nombre}">Ver Alumnos</button>
            </td>
        </tr>
    `).join('');
}

function setupProfesorViewListeners(token) {
    const contentArea = document.getElementById('content-area');
    contentArea.addEventListener('click', async (e) => {
        if (e.target.classList.contains('btn-ver-alumnos')) {
            const courseId = e.target.dataset.courseId;
            const courseName = e.target.dataset.courseName;
            const alumnosContainer = document.getElementById('profesor-alumnos-container');
            alumnosContainer.innerHTML = `<p>Cargando alumnos para el curso "${courseName}"...</p>`;

            try {
                const response = await fetch(`${config.apiBaseUrl}/api/v1/profesor/courses/${courseId}/students`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });

                if (!response.ok) throw new Error('No se pudo obtener la lista de alumnos.');

                const students = await response.json();
                alumnosContainer.innerHTML = `
                    <h3>Alumnos en "${courseName}"</h3>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Nombre Completo</th>
                                <th>Email</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${renderStudentRows(students)}
                        </tbody>
                    </table>
                `;
            } catch (error) {
                alumnosContainer.innerHTML = `<p class="message-error">Error al cargar los alumnos: ${error.message}</p>`;
            }
        }
    });
}

function renderStudentRows(students) {
    if (!students || students.length === 0) {
        return '<tr><td colspan="3">No hay alumnos inscritos en este curso.</td></tr>';
    }
    return students.map(student => `
        <tr>
            <td>${student.id}</td>
            <td>${student.nombre_completo}</td>
            <td>${student.correo}</td>
        </tr>
    `).join('');
}
