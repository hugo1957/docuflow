
import flet as ft
from pages.utils.numero_telefono import PhoneInputDropdown


def ViewLogin(page):
    def handle_country_change(selected_country):
        print(f"País seleccionado: {selected_country}")

    def handle_phone_change(phone_number):
        print(f"Número ingresado: {phone_number}")

    def handle_submit(e):
        phone = phone_input.phone_field.value
        if not phone or len(phone) < phone_input.phone_field.max_length:
            snack_bar = ft.SnackBar(
                ft.Text("Debes ingresar un número de teléfono válido!"),
                bgcolor=ft.Colors.RED_500,
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            return
        page.go("/token")

    phone_input = PhoneInputDropdown(
        on_country_change=handle_country_change,
        on_phone_change=handle_phone_change,
    )

    page.controls.clear()
    
    return ft.Container(
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
                ft.Container(
                    
                    alignment=ft.alignment.center,
                    on_click=handle_submit,
                    border_radius=ft.border_radius.all(5),
                    height=50,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.Alignment(0.8, 1),
                        colors=["#717171", "#e5bc16"],
                    ),
                    content=ft.Text(
                        "Iniciar Sesión",
                        size=15,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                    ),
                ),
            ]
        )
    )