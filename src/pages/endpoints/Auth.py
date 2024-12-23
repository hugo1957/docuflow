import aiohttp
import requests
import flet as ft
API_URL = "http://localhost:8000"


async def login_user(page, phone):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_URL}/api/user/auth/register-or-login/",
                json={"phone_number": phone},
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    page.client_storage.set(
                        "creativeferrets.tienda.phone_number", phone)
                    return True
                else:
                    return False
    except aiohttp.ClientError:
        return False


async def verify_token(page, code):
    phone = page.client_storage.get("creativeferrets.tienda.phone_number")
    if not phone:
        snack_bar = ft.SnackBar(
            ft.Text(
                "Número de teléfono no encontrado. Por favor, vuelve a iniciar sesión."),
            bgcolor=ft.Colors.RED_500,
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        return False

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_URL}/api/user/auth/verify-sms-code/",
                json={"code": code, "phone_number": phone},
                headers={"Content-Type": "application/json"},
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    access_token = data.get("access")
                    refresh_token = data.get("refresh")

                    if access_token:
                        page.client_storage.set(
                            "creativeferrets.tienda.access_token", access_token)
                        page.client_storage.set(
                            "creativeferrets.tienda.refresh_token", refresh_token)
                        return True
    except aiohttp.ClientError as e:
        print(f"Error al verificar el token: {e}")
        return False


async def resend_code(page, phone):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_URL}/api/user/auth/resend-code/",
                json={"phone_number": phone},
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    return True
    except aiohttp.ClientError:
        return False


def refresh_token(page):
    refresh_token = page.client_storage.get(
        "creativeferrets.tienda.refresh_token")
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
            page.client_storage.set(
                "creativeferrets.tienda.access_token", new_access_token)


async def load_user(page):
    access_token = page.client_storage.get(
        "creativeferrets.tienda.access_token")
    if access_token:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{API_URL}/auth/users/me/",
                    headers={
                        "Authorization": f"JWT {access_token}",
                        "Accept": "application/json"
                    }
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        page.client_storage.set(
                            "creativeferrets.tienda.user", data)
                        return data
        except aiohttp.ClientError as e:
            print(f"Error al cargar el usuario: {e}")
            return None
    return None


async def fetch_user_data(page, user_id):
  access_token = page.client_storage.get("creativeferrets.tienda.access_token")
  if access_token:
    try:
      async with aiohttp.ClientSession() as session:
        async with session.get(
          f"{API_URL}/api/user/user/{user_id}/",
          headers={
            "Authorization": f"JWT {access_token}",
            "Accept": "application/json"
          }
        ) as response:
          if response.status == 200:
            return await response.json()
    except aiohttp.ClientError as e:
      print(f"Error al cargar los datos del usuario: {e}")
      return None
  return None


async def update_user_data(page, user_id, updated_data):
  access_token = page.client_storage.get("creativeferrets.tienda.access_token")
  if access_token:
    try:
      async with aiohttp.ClientSession() as session:
        async with session.put(
          f"{API_URL}/api/user/user/edit/{user_id}/",
          json=updated_data,
          headers={
            "Authorization": f"JWT {access_token}",
            "Content-Type": "application/json",
          },
        ) as response:
          if response.status == 200:
            snack_bar = ft.SnackBar(
              ft.Text("Datos actualizados correctamente."), bgcolor=ft.Colors.GREEN
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            return await response.json()
    except aiohttp.ClientError as e:
      snack_bar = ft.SnackBar(ft.Text("Error al actualizar los datos."), bgcolor=ft.Colors.RED)
      page.overlay.append(snack_bar)
      snack_bar.open = True
      page.update()
      print(f"Error al actualizar los datos del usuario: {e}")
      return None
  return None

def logout_user(page):
    page.client_storage.remove("creativeferrets.tienda.access_token")
    page.client_storage.remove("creativeferrets.tienda.refresh_token")
    page.client_storage.remove("creativeferrets.tienda.phone_number")
    page.client_storage.remove("creativeferrets.tienda.user")
    page.go("/")
