import os
import re
import json
from playwright.sync_api import sync_playwright, expect

# Mock data
MOCK_ROLES = [
    {"nombre": "admin_general", "descripcion": "Test Desc"},
    {"nombre": "admin_empresa", "descripcion": "Test Desc"},
    {"nombre": "jefe_area", "descripcion": "Test Desc"},
    {"nombre": "profesor", "descripcion": "Test Desc"},
    # Intentionally leave some roles out to test the "Faltante" (Missing) status
]
# A fake JWT token for admin_general
# Payload: {"sub": "4", "roles": ["admin_general"], "inquilino_id": 1, "nombre_completo": "Admin General Test"}
FAKE_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0Iiwicm9sZXMiOlsiYWRtaW5fZ2VuZXJhbCJdLCJpbnF1aWxpbm9faWQiOjEsIm5vbWJyZV9jb21wbGV0byI6IkFkbWluIEdlbmVyYWwgVGVzdCJ9.fake_signature_admin_general"

def handle_route(route):
    """Function to intercept and mock API calls."""
    if "api/v1/auth/login" in route.request.url:
        # print(f"Mocking login request to: {route.request.url}")
        route.fulfill(status=200, headers={"Content-Type": "application/json"}, body=json.dumps({"access_token": FAKE_ACCESS_TOKEN, "token_type": "bearer"}))
    elif "api/v1/roles" in route.request.url:
        # print(f"Mocking roles request to: {route.request.url}")
        route.fulfill(status=200, headers={"Content-Type": "application/json"}, body=json.dumps(MOCK_ROLES))
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

        # 2. Log in as the super admin
        page.get_by_placeholder('Nombre de Usuario').fill('admin_general')
        page.get_by_placeholder('Contraseña').fill('password')
        page.get_by_role('button', name='Ingresar').click()

        # 3. Wait for navigation and check for user info
        expect(page).to_have_url(re.compile("app.html"), timeout=10000)
        expect(page.locator('#user-info')).to_contain_text('Admin General Test')

        # 4. Click the link to load the 'Verificar Roles BD' view
        page.get_by_role('link', name='Verificar Roles BD').click()

        # 5. Verify that the view content has loaded with MOCK data
        content_area = page.locator('#content-area')
        expect(content_area.get_by_role('heading', name='Verificación de Roles en Base de Datos')).to_be_visible()

        # Check for a role that should be "Encontrado" (Found)
        expect(content_area.get_by_role('row').filter(has_text="admin_empresa")).to_contain_text("Encontrado")

        # Check for a role that should be "Faltante" (Missing)
        expect(content_area.get_by_role('row').filter(has_text="alumno")).to_contain_text("Faltante")

        # Check that the "Crear Rol" button is visible for the missing role
        expect(content_area.get_by_role('row').filter(has_text="alumno").get_by_role('button', name='Crear Rol')).to_be_visible()

        print("SUCCESS: Admin General 'Verificar Roles' view loaded and verified successfully with mocked data.")

        # 6. Take a screenshot
        page.screenshot(path='jules-scratch/verification/admin_general_view_mocked.png')
        print("Screenshot of mocked admin_general view saved.")

        browser.close()

if __name__ == '__main__':
    run_verification()
