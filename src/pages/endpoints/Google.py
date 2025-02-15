import aiohttp
from flet.auth.providers import GoogleOAuthProvider

API_URL = "http://localhost:8000"

# Configurar el proveedor de autenticación de Google
google_provider = GoogleOAuthProvider(
    client_id="684509096725-pm1gdgb80i3fck9k5gd1kq7l7daf47a7.apps.googleusercontent.com",
    client_secret="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",
    redirect_url="http://localhost:8550/oauth_callback",
)

async def google_login(page):
    """
    Maneja el flujo de login con Google usando Flet.
    """
    try:
        # Realiza el login con GoogleOAuthProvider
        auth_result = await google_provider.login(page)
        
        if auth_result.error:
            print(f"Error en el login de Google: {auth_result.error}")
            return

        # Obtiene el token de acceso de Google
        google_access_token = auth_result.access_token

        # Enviar el token al backend para registro o login
        await register_or_login_google(page, google_access_token)

    except Exception as e:
        print(f"Error durante el flujo de login de Google: {e}")


async def register_or_login_google(page, google_access_token):
    """
    Envía el token de Google al backend para registrar o loguear al usuario.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_URL}/api/user/auth/google-register-or-login/",
                json={"token": google_access_token},
                timeout=10,
            ) as r:
                if r.status == 200:
                    data = await r.json()
                    # Guarda los tokens en el almacenamiento del cliente
                    await page.client_storage.set_async("creativeferrets.tienda.access_token", data["tokens"]["access"])
                    await page.client_storage.set_async("creativeferrets.tienda.refresh_token", data["tokens"]["refresh"])
                    print("Login exitoso, redirigiendo al home.")
                    page.go("/home")
                else:
                    print(f"Error en el backend al registrar o loguear: {await r.text()}")
    except Exception as e:
        print(f"Error conectando con el backend: {e}")
