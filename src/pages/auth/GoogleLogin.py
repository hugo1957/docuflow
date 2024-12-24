import os
import flet as ft
from flet.auth import OAuthProvider

def main(page: ft.Page):
    provider = OAuthProvider(
        client_id=os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY"),
        client_secret=os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET"),
        authorization_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
        token_endpoint="https://oauth2.googleapis.com/token",
        user_endpoint="https://www.googleapis.com/oauth2/v2/userinfo",
        user_scopes=["profile", "email"],
        user_id_fn=lambda u: u["id"],  # define cómo se extrae el ID del JSON
        redirect_url="http://localhost:8550/oauth_callback",
    )

    # Luego el resto es análogo al ejemplo anterior:
    def on_login(e: ft.LoginEvent):
        if e.error:
            print("Error:", e.error)
            return
        print("User ID:", page.auth.user.id)
        print("Email:", page.auth.user["email"])
        # y así sucesivamente

    page.on_login = on_login
    page.add(ft.ElevatedButton("Iniciar sesión con Google", on_click=lambda _: page.login(provider)))
    ft.app(main, port=8550, view=ft.WEB_BROWSER)

ft.app(main, port=8550)
