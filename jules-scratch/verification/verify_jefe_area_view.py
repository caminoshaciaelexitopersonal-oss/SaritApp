import os
import re
import json
from playwright.sync_api import sync_playwright, expect

# Mock data
MOCK_STAFF = [
    {"id": 10, "nombre_completo": "Profesor Jirafales", "correo": "profesor@test.com", "roles": ["profesor"]},
    {"id": 11, "nombre_completo": "Coordinador Varela", "correo": "coordinador@test.com", "roles": ["coordinador"]}
]
MOCK_EVENTS = [
    {"id": 100, "nombre": "Festival de Teatro", "tipo": "Cultural", "fecha": "2025-10-15T00:00:00"},
    {"id": 101, "nombre": "Torneo de Fútbol", "tipo": "Deportivo", "fecha": "2025-11-20T00:00:00"}
]
# A fake JWT token for jefe_area
# Payload: {"sub": "2", "roles": ["jefe_area"], "inquilino_id": 1, "nombre_completo": "Jefe de Area Test"}
FAKE_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwicm9sZXMiOlsiamVmZV9hcmVhIl0sImlucXVpbGlub19pZCI6MSwibm9tYnJlX2NvbXBsZXRvIjoiSmVmZSBkZSBBcmVhIFRlc3QifQ.fake_signature_jefe"

def handle_route(route):
    """Function to intercept and mock API calls."""
    if "api/v1/auth/login" in route.request.url:
        print(f"Mocking login request to: {route.request.url}")
        route.fulfill(status=200, headers={"Content-Type": "application/json"}, body=json.dumps({"access_token": FAKE_ACCESS_TOKEN, "token_type": "bearer"}))
    elif "api/v1/jefe_area/staff" in route.request.url:
        print(f"Mocking staff request to: {route.request.url}")
        route.fulfill(status=200, headers={"Content-Type": "application/json"}, body=json.dumps(MOCK_STAFF))
    elif "api/v1/jefe_area/events" in route.request.url:
        print(f"Mocking events request to: {route.request.url}")
        route.fulfill(status=200, headers={"Content-Type": "application/json"}, body=json.dumps(MOCK_EVENTS))
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

        # 2. Log in as the area manager
        page.get_by_placeholder('Nombre de Usuario').fill('jefe_area_test')
        page.get_by_placeholder('Contraseña').fill('password')
        page.get_by_role('button', name='Ingresar').click()

        # 3. Wait for navigation and check for user info
        expect(page).to_have_url(re.compile("app.html"), timeout=10000)
        expect(page.locator('#user-info')).to_contain_text('Jefe de Area Test')

        # 4. Click the link to load the view
        page.get_by_role('link', name='Panel de Área').click()

        # 5. Verify that the dashboard content has loaded with MOCK data
        content_area = page.locator('#content-area')
        expect(content_area.get_by_role('heading', name='Personal del Área')).to_be_visible()
        expect(content_area.get_by_role('heading', name='Eventos del Área')).to_be_visible()

        # Check for specific mock data
        expect(content_area.get_by_role('cell', name='Profesor Jirafales')).to_be_visible()
        expect(content_area.get_by_role('cell', name='Festival de Teatro')).to_be_visible()

        print("SUCCESS: Jefe de Área dashboard view loaded successfully with mocked data.")

        # 6. Take a screenshot
        page.screenshot(path='jules-scratch/verification/jefe_area_dashboard_mocked.png')
        print("Screenshot of mocked jefe_area dashboard saved.")

        browser.close()

if __name__ == '__main__':
    run_verification()
