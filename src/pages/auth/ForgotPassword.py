import flet as ft
import re
from pages.utils.alert import show_construction_dialog


def ViewForgotPassword(page):
    page.controls.clear()

    email_field = ft.TextField(
        label="Correo Electrónico",
        width=350,
        height=60,
        border_radius=ft.border_radius.all(15),
        content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
        bgcolor=ft.Colors.WHITE,
        border_color="#717171",
        label_style=ft.TextStyle(color="#717171"),
        border_width=2,
    )

    def handle_reset_click(e):
        email = email_field.value
        if not email:
            snack_bar = ft.SnackBar(
                ft.Text("Debes ingresar tu correo para recuperar la contraseña"), bgcolor=ft.Colors.RED_500)
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            return
        # reset_password(page, email)

    container = ft.Column(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
        spacing=0,
        controls=[
            ft.Container(
                height=50,
                content=ft.Text("CIE", size=15,
                                color=ft.Colors.WHITE, text_align="center", weight="bold"),
                alignment=ft.alignment.center,
            ),
            ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=ft.border_radius.only(
                    top_left=17, top_right=17),
                expand=True,
                padding=ft.padding.all(10),
                content=ft.Column(
                    alignment="center",
                    horizontal_alignment="center",
                    scroll=ft.ScrollMode.HIDDEN,
                    controls=[
                        ft.Image(
                            src="forgot.svg",
                            width=300,
                            height=300
                        ),
                        ft.Text(
                            "¿Olvidaste tu contraseña?", size=20, weight="bold"
                        ),

                        email_field,
                        ft.Container(height=10),
                        ft.Container(
                            alignment=ft.alignment.center,
                            on_click=handle_reset_click,
                            ink=True,
                            border_radius=ft.border_radius.all(5),
                            width=350,
                            height=50,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.Alignment(0.8, 1),
                                colors=[
                                    "#717171",
                                    "#e5bc16",
                                ],
                            ),
                            content=ft.Text(
                                "Enviar", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            padding=ft.padding.all(10),
                        ),
                        ft.Container(height=5),

                    ]
                )
            )
        ]
    )

    return container
