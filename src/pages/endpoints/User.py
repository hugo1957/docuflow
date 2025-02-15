import flet as ft
from pages.endpoints.Auth import load_user, update_user_data, fetch_user_data

API_URL = "https://api.creativeferrets.com"

async def validate_user(page):
    try:
        # 1) Verificamos token en client_storage
        access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
        if not access_token:
            page.go("/phone-login")
            return False

        # 2) Verificamos usuario (parcial) en client_storage
        user_data = await page.client_storage.get_async("creativeferrets.tienda.user")
        if not user_data:
            await load_user(page)
            user_data = await page.client_storage.get_async("creativeferrets.tienda.user")
        if not user_data:
            page.go("/phone-login")
            return False

        # 3) Obtenemos datos completos del usuario desde tu backend
        full_user_data = None
        try:
            full_user_data = await fetch_user_data(page, user_data["id"])
            # Fusionamos "profile" en el nivel superior (solo una vez)
            profile_data = full_user_data.pop("profile", {})
            full_user_data.update(profile_data)

        except Exception as ex:
            print("Error al obtener datos del usuario:", ex)


        # 4) Revisamos agreed_terms en full_user_data (ya está fusionado)
        if not full_user_data.get("agreed_terms"):
            def accept_terms_click(e):
                page.run_task(accept_terms_async, page, full_user_data, bs)

            async def accept_terms_async(page, merged_data, bottom_sheet):
                merged_data["agreed_terms"] = True
                updated_user = await update_user_data(page, user_data["id"], merged_data)
                if updated_user:
                    bottom_sheet.open = False
                    page.update()
                    # Recargamos la misma ruta para que pase la validación
                    page.go(page.route)

            # BottomSheet para aceptar términos
            bs = ft.BottomSheet(
                open=True,
                content=ft.Container(
                    padding=50,
                    content=ft.Column(
                        tight=True,
                        controls=[
                            ft.Text("Por favor, acepta los términos y condiciones para continuar."),
                            ft.ElevatedButton("Aceptar", on_click=accept_terms_click),
                        ],
                    ),
                ),
            )
            page.open(bs)
            page.update()
            return False

        # 5) Validamos datos de perfil incompleto (usando el user_data parcial)
        if (
            user_data.get("email", "").endswith("@example.com")
            or user_data.get("first_name") == "Usuario"
            or user_data.get("last_name") == "Nuevo"
        ):
            page.go("/profile")
            snack = ft.SnackBar(
                ft.Text("Por favor, completa tu perfil."),
                bgcolor=ft.Colors.ORANGE_400,
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()
            return False

        return True

    except Exception as e:
        print(f"Error en la autenticación: {e}")
        page.go("/phone-login")
        return False
