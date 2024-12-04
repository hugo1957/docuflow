import flet as ft
import re 
from pages.utils.alert import show_construction_dialog
def validate_password_strength(password):
    if len(password) < 6:
        return "Débil"
    elif re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'[0-9]', password) and re.search(r'[!@#$%^&*]', password):
        return "Fuerte"
    else:
        return "Moderada"


def ViewLogin(page):
    page.controls.clear()

    email_field = ft.TextField(
        label="Correo Electrónico",
        width=350,
        height=60,
        border_radius=ft.border_radius.all(15),
        content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
        bgcolor=ft.Colors.WHITE,
        border_color="#717171",
        label_style=ft.TextStyle(color="#717171", font_family="Poppins"),
        border_width=2,

    )
    password_field = ft.TextField(
        label="Contraseña",
        width=350,
        height=60,
        password=True,
        can_reveal_password=True,
        border_radius=ft.border_radius.all(15),
        content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
        bgcolor=ft.Colors.WHITE,
        border_color="#717171",
        label_style=ft.TextStyle(color="#717171"),
        border_width=2,)

    def handle_login_click(e):
        email = email_field.value
        password = password_field.value
        if not email or not password:
            snack_bar = ft.SnackBar(
                ft.Text("Debes ingresar un correo y una contraseña valida!"), bgcolor=ft.Colors.RED_500)
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            return
        # login_user(page, email, password)

    container = ft.Column(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
        spacing=0,
        controls=[
            ft.Container(
                height=50,
                content=ft.Text("CIE", size=15,
                                color=ft.Colors.WHITE, text_align="center", weight=ft.FontWeight.BOLD, font_family="Poppins"),
                alignment=ft.alignment.center,
            ),
            ft.Container(
                bgcolor=ft.Colors.WHITE,
                padding=ft.padding.all(20),
                border_radius=ft.border_radius.only(
                    top_left=17, top_right=17),
                expand=True,
                content=ft.Column(
                    spacing=20,
                    horizontal_alignment="center",
                    scroll=ft.ScrollMode.HIDDEN,
                    controls=[
                        ft.Container(height=5),
                        ft.Text(
                            "Bienvenido!!", size=20, color=ft.Colors.BLACK, weight=ft.FontWeight.W_100, font_family="Heavitas"
                        ),
                        ft.Text(
                            "Inicia sesión para continuar", size=15, color=ft.Colors.BLACK, font_family="Poppins"
                        ),
                        email_field,
                        password_field,
                        ft.Container(
                            alignment=ft.alignment.center,
                            on_click=handle_login_click,
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
                                "Iniciar Sesión", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            padding=ft.padding.all(10),
                        ),
                        ft.TextButton("Olvidé mi contraseña?", on_click=lambda e: page.go("/forgot-password"), style=ft.ButtonStyle(
                            color="#717171")),
                        ft.Container(
                            content=ft.Row(
                                alignment="center",
                                vertical_alignment="center",
                                controls=[
                                    ft.Container(
                                        content=ft.Divider(
                                            thickness=1, color=ft.Colors.GREY),
                                        expand=True,
                                    ),
                                    ft.Text("Inicia con", size=15,
                                            color=ft.Colors.GREY),
                                    ft.Container(
                                        content=ft.Divider(
                                            thickness=1, color=ft.Colors.GREY),
                                        expand=True,
                                    ),
                                ]
                            ),
                        ),
                        ft.Container(
                            content=ft.ResponsiveRow(
                                [
                                    ft.Container(
                                        content=ft.Row(
                                            controls=[
                                                ft.Image(
                                                    src="redes/google.svg",
                                                    width=24,
                                                    height=24
                                                ),
                                                ft.Text(
                                                    "Google", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)
                                            ],
                                            alignment="center"
                                        ),
                                        padding=ft.padding.symmetric(
                                            vertical=10, horizontal=20),
                                        border_radius=ft.border_radius.all(8),
                                        border=ft.border.all(
                                            color="#717171", width=1),
                                        ink=True,
                                        # Alineación responsiva
                                        col={"sm": 12, "md": 6,
                                             "lg": 5, "xl": 4},
                                        on_click=lambda _: show_construction_dialog(
                                            page, "Google", "La autenticacion")
                                    ),
                                    ft.Container(
                                        content=ft.Row(
                                            spacing=0,
                                            controls=[
                                                
                                                ft.Container(
                                                    width=20,
                                                    height=20,
                                                    content=ft.Image(
                                                    src="redes/facebook-login.svg",
                                                    width=24,
                                                    height=24
                                                ),
                                                    ),
                                                ft.Text(
                                                    "Facebook", color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD)
                                            ],
                                            alignment="center"
                                        ),
                                        padding=ft.padding.symmetric(
                                            vertical=10, horizontal=20),
                                        border_radius=ft.border_radius.all(8),
                                        border=ft.border.all(
                                            color="#717171", width=1),
                                        # Alineación responsiva
                                        col={"sm": 12, "md": 6,
                                             "lg": 5, "xl": 4},
                                        on_click=lambda _: show_construction_dialog(
                                            page, "Facebook", "La autenticacion")
                                    )
                                ],
                                alignment="center",  # Alinear al centro
                                # Espaciado entre columnas para pantallas pequeñas y medianas
                                run_spacing={"xs": 10, "md": 10},
                            ),
                            padding=ft.padding.symmetric(vertical=20)
                        )

                    ]
                )
            )
        ]
    )
    return container
