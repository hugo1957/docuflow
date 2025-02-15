import os
import flet as ft
from flet.auth import OAuthProvider

def ViewAppleLogin(page):
    provider = OAuthProvider(
        client_id=os.getenv("APPLE_CLIENT_ID"),
        client_secret=os.getenv("APPLE_CLIENT_SECRET"),
        authorization_endpoint="https://appleid.apple.com/auth/authorize",
        token_endpoint="https://appleid.apple.com/auth/token",
        user_endpoint=None,  # Apple no proporciona un endpoint para obtener información del usuario
        user_scopes=["name", "email"],
        user_id_fn=lambda u: u["sub"],  # 'sub' es el identificador único del usuario en el id_token
        redirect_url="https://tu-dominio.com/oauth_callback",
    )

    def on_login(e: ft.LoginEvent):
        if e.error:
            print("Error:", e.error)
            return
        print("User ID:", page.auth.user.id)
        print("Email:", page.auth.user.get("email", "No proporcionado"))
        # Procesa la información adicional según sea necesario

    page.on_login = on_login

    return provider
