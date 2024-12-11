
import flet as ft

def WelcomeView(page):

    page.controls.clear()
    
    header = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Row(
                        [
                            ft.Image(src="flags/co.png", width=20),
                            ft.Text("Colombia", color=ft.Colors.WHITE,
                                    weight=ft.FontWeight.BOLD),
                        ],
                        spacing=5,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    border_radius=15,
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    bgcolor=ft.Colors.BLACK12,
                    width=120,
                ),
                ft.Text(
                    "Regístrate y simplifica tu vida",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),

            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=ft.padding.all(20),
        expand=True,
        alignment=ft.alignment.center,
    )

    # Botones de inicio
    buttons = ft.Column(
        [
            ft.ElevatedButton(
                "Continúa con tu celular",
                icon=ft.Icons.PHONE,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(
                        radius=10)
                ),
                width=300,
                on_click=lambda e: page.go("/phone-login"),
            ),
            ft.ElevatedButton(
                content=ft.Row(
                    controls=[
                        ft.Container(width=40),
                        ft.Lottie(
                            src="https://creativeferrets.com/assets/lottie/apple.json",
                            animate=True,
                            width=30,
                            height=30,
                        ),
                        ft.Text("Continúa con Apple", color=ft.Colors.WHITE,expand=True),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(
                        radius=10)
                ),
                width=300,
            ),
            ft.ElevatedButton(
                content=ft.Row(
                    controls=[
                        ft.Container(width=40),
                        ft.Lottie(
                            src="https://creativeferrets.com/assets/lottie/google.json",
                            width=30,
                            height=30,
                        ),
                        ft.Text("Continúa con Google", color=ft.Colors.WHITE,expand=True),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    
                ),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(
                        radius=10),
                ),
                width=300,

            ),
            ft.TextButton(
                "Soy usuario registrado",
                style=ft.ButtonStyle(color=ft.Colors.GREEN),
                on_click=lambda e: page.go("/login"),
            ),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    main_container = ft.Container(
        padding=ft.padding.all(10),
        alignment=ft.alignment.center,
        image_fit=ft.ImageFit.COVER,
        image_src="Autenticacion/1.jpeg",
        content=ft.Column(
            [
                header,
                buttons,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
    )

    return main_container