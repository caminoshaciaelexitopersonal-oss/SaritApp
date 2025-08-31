import os
from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Navigate to the login page
        login_path = os.path.abspath('SGA-CD-WEB.git/login.html')
        page.goto(f'file://{login_path}')

        # 2. Log in
        page.get_by_placeholder('Nombre de Usuario').fill('profesor_test')
        page.get_by_placeholder('Contraseña').fill('password')
        page.get_by_role('button', name='Ingresar').click()

        # 3. Wait for navigation and verify Light Mode
        expect(page).to_have_url('app.html', timeout=10000) # Increased timeout

        # Check that the body does not have data-theme="dark" initially
        expect(page.locator('body')).not_to_have_attribute('data-theme', 'dark')

        # Verify floating icon is visible
        expect(page.locator('#floating-agent-icon')).to_be_visible()

        # Take screenshot of Light Mode
        page.screenshot(path='jules-scratch/verification/light_mode.png')
        print("Screenshot of Light Mode saved.")

        # 4. Switch to Dark Mode
        theme_toggle = page.locator('#theme-toggle')
        theme_toggle.click()

        # 5. Verify Dark Mode is applied
        expect(page.locator('body')).to_have_attribute('data-theme', 'dark')

        # Take screenshot of Dark Mode
        page.screenshot(path='jules-scratch/verification/dark_mode.png')
        print("Screenshot of Dark Mode saved.")

        browser.close()

if __name__ == '__main__':
    run_verification()
