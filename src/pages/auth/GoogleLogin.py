import flet as ft
import requests

def ViewGoogleLogin(page):
    API_URL = "http://localhost:8000/auth/o/google-oauth2"
    REDIRECT_URI = "http://localhost:8000/google"

    def redirect_to_google_login():
        try:
            # Llamada al backend para obtener la URL de autenticación
            response = requests.get(f"{API_URL}/?redirect_uri={REDIRECT_URI}")
            response.raise_for_status()
            authorization_url = response.json().get("authorization_url")
            if authorization_url:
                # Abrir la URL en el navegador predeterminado
                page.launch_url(authorization_url)
            else:
                print("Error: No se pudo obtener la URL de autorización.")
        except requests.RequestException as err:
            print(f"Error al obtener la URL: {err}")

    # Botón para iniciar el flujo de Google OAuth
    return ft.Container(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Inicia sesión con Google para continuar",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),
                ft.ElevatedButton(
                    "Iniciar sesión con Google",
                    on_click=lambda _: redirect_to_google_login()
                )
            ],
        ),
        expand=True,
    )
