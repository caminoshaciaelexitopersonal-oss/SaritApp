import os
import time
from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Navigate to the registration page
        register_path = os.path.abspath('SGA-CD-WEB.git/register.html')
        page.goto(f'file://{register_path}')

        # 2. Fill out the registration form
        # Use a unique company name to avoid conflicts if the test is run multiple times
        company_name = f"TestCorp_{int(time.time())}"
        page.get_by_placeholder('Nombre de tu Empresa').fill(company_name)
        page.get_by_placeholder('Tu Nombre Completo').fill('Test Admin')
        page.get_by_placeholder('Tu Correo Electrónico').fill(f'admin_{int(time.time())}@testcorp.com')
        page.get_by_placeholder('Elige una Contraseña').fill('password123')

        # 3. Submit the form
        page.get_by_role('button', name='Comenzar Prueba Gratuita').click()

        # 4. Verify success message
        success_message = page.locator('#form-mensaje')
        expect(success_message).to_have_class('message-success')
        expect(success_message).to_contain_text('¡Organización registrada con éxito!')

        # 5. Verify redirection to login page
        # The script waits for 3 seconds before redirecting, so we need to wait
        expect(page).to_have_url('login.html', timeout=5000)

        print("Registration flow test completed successfully.")

        # Take a screenshot of the final login page after redirection
        page.screenshot(path='jules-scratch/verification/registration_redirect.png')
        print("Screenshot of login page after redirection saved.")

        browser.close()

if __name__ == '__main__':
    run_verification()
