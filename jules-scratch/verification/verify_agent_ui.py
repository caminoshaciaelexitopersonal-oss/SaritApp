import os
from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Navigate to the login page
        login_path = os.path.abspath('SGA-CD-WEB.git/login.html')
        page.goto(f'file://{login_path}')

        # 2. Log in using placeholders as locators
        page.get_by_placeholder('Nombre de Usuario').fill('profesor_test')
        page.get_by_placeholder('Contraseña').fill('password')
        page.get_by_role('button', name='Ingresar').click()

        # 3. Wait for navigation to the app page and verify elements
        # The argument to to_have_url should be a string or a regex.
        # Playwright will treat a string as a substring to search for.
        expect(page).to_have_url('app.html')

        # Verify user info is displayed
        user_info = page.locator('#user-info')
        # We check for a role we know the 'profesor_test' user has.
        expect(user_info).to_contain_text('Roles: profesor')

        # 4. Interact with the Agent UI
        agent_interface = page.locator('#agent-interface')
        expect(agent_interface).to_be_visible()

        # Type an order
        order_text = 'Genera un reporte de asistencia para el curso de Biología.'
        page.get_by_placeholder('Escribe tu orden aquí...').fill(order_text)

        # Click the submit button
        page.get_by_role('button', name='Enviar Orden').click()

        # 5. Wait for and verify the response
        response_area = page.locator('#agent-response-area')
        # The API is mocked, so we expect the placeholder response
        expect(response_area).to_contain_text('Respuesta del Agente')
        expect(response_area).to_contain_text('Agent logic not yet implemented.')

        # 6. Take a screenshot
        screenshot_path = os.path.abspath('jules-scratch/verification/verification.png')
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == '__main__':
    run_verification()
