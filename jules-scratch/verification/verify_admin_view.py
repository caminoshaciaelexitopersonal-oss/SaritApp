import os
import re
import json
from playwright.sync_api import sync_playwright, expect

# Mock data to be returned by the simulated API
MOCK_USERS = [
    {"id": 1, "nombre_completo": "Test User One", "correo": "user1@test.com", "roles": ["profesor"]},
    {"id": 2, "nombre_completo": "Test User Two", "correo": "user2@test.com", "roles": ["alumno"]}
]
MOCK_AREAS = [
    {"id": 1, "nombre": "Área de Cultura", "descripcion": "Actividades culturales"},
    {"id": 2, "nombre": "Área de Deportes", "descripcion": "Actividades deportivas"}
]
# A fake JWT token. The payload is what matters for the frontend JS.
# Payload: {"sub": "1", "roles": ["admin_empresa"], "inquilino_id": 1, "nombre_completo": "Admin Test"}
FAKE_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZXMiOlsiYWRtaW5fZW1wcmVzYSJdLCJpbnF1aWxpbm9faWQiOjEsIm5vbWJyZV9jb21wbGV0byI6IkFkbWluIFRlc3QifQ.fake_signature"

def handle_route(route):
    """Function to intercept and mock API calls."""
    if "api/v1/auth/login" in route.request.url:
        print(f"Mocking login request to: {route.request.url}")
        route.fulfill(
            status=200,
            headers={"Content-Type": "application/json"},
            body=json.dumps({
                "access_token": FAKE_ACCESS_TOKEN,
                "token_type": "bearer"
            })
        )
    elif "api/v1/admin/users/by-empresa" in route.request.url:
        print(f"Mocking users request to: {route.request.url}")
        route.fulfill(
            status=200,
            headers={"Content-Type": "application/json"},
            body=json.dumps(MOCK_USERS)
        )
    elif "api/v1/admin/areas" in route.request.url:
        print(f"Mocking areas request to: {route.request.url}")
        route.fulfill(
            status=200,
            headers={"Content-Type": "application/json"},
            body=json.dumps(MOCK_AREAS)
        )
    else:
        # For any other request, continue as normal
        route.continue_()

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Set up the mocking before navigating
        page.route(re.compile("api/v1/"), handle_route)

        # 1. Navigate to the login page served by a local server
        page.goto('http://localhost:8080/login.html')

        # 2. Log in as the company admin
        page.get_by_placeholder('Nombre de Usuario').fill('admin_empresa_test')
        page.get_by_placeholder('Contraseña').fill('password')
        page.get_by_role('button', name='Ingresar').click()

        # 3. Wait for navigation. Because of the mock, this should be very fast.
        expect(page).to_have_url(re.compile("app.html"), timeout=10000)

        # 4. Wait for the main app to render the user info, indicating it's ready.
        expect(page.locator('#user-info')).to_contain_text('Admin Test')

        # 5. Click the link to load the view.
        page.get_by_role('link', name='Panel de Empresa').click()

        # 6. Verify that the dashboard content has loaded with MOCK data
        content_area = page.locator('#content-area')

        # Check for the headers of both tables
        expect(content_area.get_by_role('heading', name='Usuarios de la Empresa')).to_be_visible()
        expect(content_area.get_by_role('heading', name='Áreas de la Empresa')).to_be_visible()

        # Check for specific mock data in the tables
        expect(content_area.get_by_role('cell', name='Test User One')).to_be_visible()
        expect(content_area.get_by_role('cell', name='Área de Cultura')).to_be_visible()

        print("SUCCESS: Admin dashboard view loaded successfully with mocked data.")

        # 6. Take a screenshot
        page.screenshot(path='jules-scratch/verification/admin_dashboard_mocked.png')
        print("Screenshot of mocked admin dashboard saved.")

        browser.close()

if __name__ == '__main__':
    run_verification()
