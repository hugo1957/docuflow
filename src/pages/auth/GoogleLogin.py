import flet as ft
from flet.auth import OAuthProvider


def ViewGoogleLogin():
    """
    Configura el proveedor de autenticación de Google.
    """
    return OAuthProvider(
        client_id="684509096725-pm1gdgb80i3fck9k5gd1kq7l7daf47a7.apps.googleusercontent.com",
        client_secret="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",
        authorization_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
        token_endpoint="https://oauth2.googleapis.com/token",
        user_endpoint="https://www.googleapis.com/oauth2/v2/userinfo",
        user_scopes=["profile", "email"],
        user_id_fn=lambda u: u["id"],  # Extrae el ID único del usuario.
        redirect_url="http://localhost:8550/oauth_callback",
    )


def on_login(e: ft.LoginEvent):
    """
    Manejador del evento `on_login` para procesar el resultado del login.
    """
    if e.error:
        print(f"Error en el login: {e.error}")
        return

    # Información del usuario autenticado
    print("Autenticación exitosa")
    print("Token de acceso:", e.token.access_token)
    print("Usuario ID:", e.user.id)
    print("Email:", e.user.get("email", "No proporcionado"))
    print("Nombre:", e.user.get("name", "No proporcionado"))

