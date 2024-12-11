import flet as ft
from pages.endpoints.Auth import login_user
from pages.utils.numero_telefono import PhoneInputDropdown

def ViewLogin(page):
    page.controls.clear()
    page.appbar = ft.AppBar(bgcolor=ft.Colors.WHITE)
    page.navigation_bar = None
    page.update()

    phone_input = PhoneInputDropdown()

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar número de teléfono"),
        content=ft.Text(""),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: close_confirm_dialog()),
            ft.TextButton("Confirmar", on_click=lambda e: confirm_phone_number(e)),
        ],
    )

    def close_confirm_dialog():
        confirm_dialog.open = False
        page.update()

    def confirm_phone_number(e):
        phone = phone_input.phone_field.value
        country_code = phone_input.dropdown.value
        full_phone = f"{country_code}{phone}"

        if login_user(page, full_phone):
            close_confirm_dialog()
            page.go("/token")
        else:
            close_confirm_dialog()
            snack_bar = ft.SnackBar(
                ft.Text("Error al enviar el número de teléfono."),
                bgcolor=ft.Colors.RED_500,
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    def open_confirm_dialog():
        phone = phone_input.phone_field.value
        country_code = phone_input.dropdown.value
        full_phone = f"{country_code}{phone}"
        if not phone or len(phone) < phone_input.phone_field.max_length:
            snack_bar = ft.SnackBar(
                ft.Text("Debes ingresar un número de teléfono válido!"),
                bgcolor=ft.Colors.RED_500,
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            return
        confirm_dialog.content.value = f"¿Es este tu número de teléfono?\n{full_phone}"
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    def handle_phone_change(phone_number):
        if len(phone_number) >= 3:
            sms_button.visible = True
            whatsapp_button.visible = True
        else:
            sms_button.visible = False
            whatsapp_button.visible = False
        page.update()

    phone_input.on_phone_change = handle_phone_change

    sms_button = ft.Container(
        alignment=ft.alignment.center,
        on_click=lambda e: open_confirm_dialog(),
        border_radius=ft.border_radius.all(15),
        height=50,
        bgcolor=ft.Colors.GREEN,
        visible=False,
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.PHONE, color=ft.Colors.WHITE),
                ft.Text(
                    "Recibir código por SMS",
                    size=15,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    whatsapp_button = ft.Container(
        alignment=ft.alignment.center,
        on_click=lambda e: open_confirm_dialog(),
        border_radius=ft.border_radius.all(15),
        height=50,
        bgcolor=ft.Colors.GREEN,
        visible=False,
        content=ft.Row(
            controls=[
                ft.Lottie(
                    src="https://creativeferrets.com/assets/lottie/whastapp.json",
                    animate=True,
                    width=30,
                    height=30,
                ),
                ft.Text(
                    "Recibir código por WhatsApp",
                    size=15,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    container = ft.Container(
        alignment=ft.alignment.center,
        expand=True,
        padding=ft.padding.all(20),
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Container(height=20),
                ft.Text("Número de teléfono", style=ft.TextStyle(color="#717171")),
                phone_input,
                ft.Container(height=20),
                sms_button,
                whatsapp_button,
            ],
        ),
    )

    return container
