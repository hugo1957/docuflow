
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
                ft.Container(height=20),
                ft.Container(
                    alignment=ft.alignment.center,
                    on_click=handle_submit,
                    border_radius=ft.border_radius.all(15),
                    height=50,
                    bgcolor=ft.Colors.GREEN,
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.PHONE, color=ft.Colors.WHITE),
                            ft.Text(
                                "Recibir código por SMS",
                                size=15,
                                color=ft.Colors.WHITE,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Container(width=10),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.alignment.center,
                    )
                ),
                ft.Container(
                    alignment=ft.alignment.center,
                    on_click=handle_submit,
                    border_radius=ft.border_radius.all(15),
                    height=50,
                    bgcolor=ft.Colors.GREEN,
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
                            ft.Container(width=10),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.alignment.center,
                    )
                )
            ]
        )
    )