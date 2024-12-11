import requests
import flet as ft
API_URL = "http://localhost:8000"

def login_user(page, phone):
    try:
        response = requests.post(
            f"{API_URL}/api/user/auth/register-or-login/",
            json={"phone_number": phone},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()

        # Almacena el número de teléfono en client_storage
        page.client_storage.set("creativeferrets.tienda.phone_number", phone)

        return True
    except requests.exceptions.RequestException:
        return False



def verify_token(page, code):
    phone = page.client_storage.get("creativeferrets.tienda.phone_number")
    if not phone:
        snack_bar = ft.SnackBar(
            ft.Text("Número de teléfono no encontrado. Por favor, vuelve a iniciar sesión."),
            bgcolor=ft.Colors.RED_500,
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        return False

    try:
        response = requests.post(
            f"{API_URL}/api/user/auth/verify-sms-code/",
            json={"code": code, "phone_number": phone},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()

        data = response.json()
        access_token = data.get("access")
        refresh_token = data.get("refresh")

        if access_token:
            page.client_storage.set("creativeferrets.tienda.access_token", access_token)
            page.client_storage.set("creativeferrets.tienda.refresh_token", refresh_token)
            return True
    except requests.exceptions.RequestException as e:
        print(f"Error al verificar el token: {e}")
        return False



def resend_code(page, phone):
    try:
        response = requests.post(
           f"{API_URL}/api/user/auth/resend-code/",
            json={"phone_number": phone},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False
    
def refresh_token(page):
    refresh_token = page.client_storage.get("creativeferrets.tienda.refresh_token")
    if refresh_token:
        response = requests.post(
            f"{API_URL}/auth/jwt/refresh/",
            json={"refresh": refresh_token},
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        response.raise_for_status()
        data = response.json()
        new_access_token = data.get("access")
        if new_access_token:
            page.client_storage.set("creativeferrets.tienda.access_token", new_access_token)


def load_user(page):
    access_token = page.client_storage.get("creativeferrets.tienda.access_token")
    if access_token:
        response = requests.get(
            f"{API_URL}/auth/users/me/",
            headers={
                "Authorization": f"JWT {access_token}",
                "Accept": "application/json"
            }
        )
        response.raise_for_status()
        user_data = response.json()
        page.client_storage.set("creativeferrets.tienda.user", user_data)
        
def logout_user(page):
    page.client_storage.remove("creativeferrets.tienda.access_token")
    page.client_storage.remove("creativeferrets.tienda.refresh_token")
    page.client_storage.remove("creativeferrets.tienda.phone_number")
    page.client_storage.remove("creativeferrets.tienda.user")
    page.go("/")

