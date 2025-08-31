import asyncio
from playwright.async_api import async_playwright, Page, expect
import os
import json

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Listen for console logs for debugging
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))

        # --- Mock API Responses ---
        mock_misiones_response = [
            {
                "id": 1,
                "nombre": "Misión de Bienvenida",
                "descripcion": "Completa tu perfil y asiste a tu primera clase.",
                "puntos_recompensa": 50,
                "medalla_recompensa_key": "bienvenida",
            },
            {
                "id": 2,
                "nombre": "Asistencia Perfecta (Semanal)",
                "descripcion": "Asiste a todas tus clases durante una semana.",
                "puntos_recompensa": 100,
                "medalla_recompensa_key": None,
            }
        ]

        async def handle_route(route):
            if "api/v1/misiones" in route.request.url:
                print(f"Intercepted API call to: {route.request.url}")
                await route.fulfill(json=mock_misiones_response)
            else:
                await route.continue_()

        await page.route("**/api/v1/*", handle_route)

        # --- Mock Login ---
        # Navigate to the page once to set up the context
        await page.goto(f"file://{os.path.abspath('SGA-CD-WEB.git/app.html')}")

        # Create a fake user object and token
        fake_user = {"username": "alumno_test", "nombre_completo": "Juan Alumno", "roles": ["alumno"], "id": 123}
        fake_token = "fake-jwt-token-for-testing"

        # Use page.evaluate to set localStorage items
        await page.evaluate(f"""
            localStorage.setItem('authToken', '{fake_token}');
            localStorage.setItem('userInfo', JSON.stringify({json.dumps(fake_user)}));
        """)

        print("Mock login complete. User info and token set in localStorage.")

        # Reload the page to apply the logged-in state
        await page.reload()

        # --- Test Navigation and View ---
        print("Navigating to Misiones view...")

        # Click the "Misiones" link in the navigation
        misiones_link = page.get_by_role("link", name="Misiones")
        await expect(misiones_link).to_be_visible(timeout=5000)
        await misiones_link.click()

        print("Checking for rendered mission cards...")

        # Assert that the heading for the missions view is visible
        heading = page.get_by_role("heading", name="Misiones Disponibles")
        await expect(heading).to_be_visible(timeout=5000)
        print("Missions view heading found.")

        # Assert that a card for our mock mission is visible
        mission_card = page.get_by_text("Misión de Bienvenida")
        await expect(mission_card).to_be_visible()
        print("Mock mission card found.")

        # Assert that the reward points are visible
        reward_points = page.get_by_text("+50 Puntos")
        await expect(reward_points).to_be_visible()
        print("Reward points found.")

        # Take a screenshot
        screenshot_path = "jules-scratch/verification/gamification_misiones_view.png"
        await page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
