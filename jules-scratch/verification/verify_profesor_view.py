import os
import re
import json
from playwright.sync_api import sync_playwright, expect

# Mock data
MOCK_COURSES = [
    {"id": 20, "nombre": "Introducción a la Programación", "descripcion": "Curso de Python"},
    {"id": 21, "nombre": "Cálculo Avanzado", "descripcion": "Matemáticas II"}
]
MOCK_STUDENTS_FOR_COURSE_20 = [
    {"id": 201, "nombre_completo": "El Chavo del Ocho", "correo": "chavo@test.com"},
    {"id": 202, "nombre_completo": "Quico", "correo": "quico@test.com"}
]
# A fake JWT token for profesor
# Payload: {"sub": "3", "roles": ["profesor"], "inquilino_id": 1, "nombre_completo": "Profesor Test"}
FAKE_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwicm9sZXMiOlsicHJvZmVzb3IiXSwiaW5xdWlsaW5vX2lkIjoxLCJub21icmVfY29tcGxldG8iOiJQcm9mZXNvclRlc3QifQ.fake_signature_profesor"

def handle_route(route):
    """Function to intercept and mock API calls."""
    if "api/v1/auth/login" in route.request.url:
        print(f"Mocking login request to: {route.request.url}")
        route.fulfill(status=200, headers={"Content-Type": "application/json"}, body=json.dumps({"access_token": FAKE_ACCESS_TOKEN, "token_type": "bearer"}))
    elif "api/v1/profesor/courses/20/students" in route.request.url:
        print(f"Mocking students request to: {route.request.url}")
        route.fulfill(status=200, headers={"Content-Type": "application/json"}, body=json.dumps(MOCK_STUDENTS_FOR_COURSE_20))
    elif "api/v1/profesor/courses" in route.request.url:
        print(f"Mocking courses request to: {route.request.url}")
        route.fulfill(status=200, headers={"Content-Type": "application/json"}, body=json.dumps(MOCK_COURSES))
    else:
        route.continue_()

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Set up mocking
        page.route(re.compile("api/v1/"), handle_route)

        # 1. Navigate to the login page
        page.goto('http://localhost:8080/login.html')

        # 2. Log in as the professor
        page.get_by_placeholder('Nombre de Usuario').fill('profesor_test')
        page.get_by_placeholder('Contraseña').fill('password')
        page.get_by_role('button', name='Ingresar').click()

        # 3. Wait for navigation and check for user info
        expect(page).to_have_url(re.compile("app.html"), timeout=10000)
        expect(page.locator('#user-info')).to_contain_text('ProfesorTest')

        # 4. Trigger the profesor view manually since there's no dedicated nav link in the base UI
        page.evaluate("renderProfesorView(localStorage.getItem('accessToken'))")

        # 5. Verify that the courses table has loaded with MOCK data
        content_area = page.locator('#profesor-cursos-container')
        expect(content_area.get_by_role('heading', name='Mis Cursos')).to_be_visible()
        expect(content_area.get_by_role('cell', name='Introducción a la Programación')).to_be_visible()

        # 6. Click the button to view students for the first course
        page.get_by_role('button', name='Ver Alumnos').first.click()

        # 7. Verify that the students table has loaded with MOCK data
        alumnos_container = page.locator('#profesor-alumnos-container')
        expect(alumnos_container.get_by_role('heading', name='Alumnos en "Introducción a la Programación"')).to_be_visible()
        expect(alumnos_container.get_by_role('cell', name='El Chavo del Ocho')).to_be_visible()

        print("SUCCESS: Profesor dashboard view loaded and interacted with successfully using mocked data.")

        # 8. Take a screenshot
        page.screenshot(path='jules-scratch/verification/profesor_dashboard_mocked.png')
        print("Screenshot of mocked profesor dashboard saved.")

        browser.close()

if __name__ == '__main__':
    run_verification()
