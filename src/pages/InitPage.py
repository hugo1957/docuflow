import flet as ft

def WelcomeView(page):
    def navigate_to(e, url):
        page.go(url)

    page.controls.clear()

    header = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.FLAG, color=ft.Colors.YELLOW),
                            ft.Text("Colombia", color=ft.Colors.BLACK,
                                    weight=ft.FontWeight.BOLD),
                        ],
                        spacing=5,
                    ),
                    border_radius=15,
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    bgcolor=ft.Colors.BLACK12,
                ),
                ft.Text(
                    "Regístrate y simplifica tu vida",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Image(src="icon.png", width=120,
                                 height=120, fit=ft.ImageFit.COVER),
                        ft.Container()
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            expand=True,
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
                        ft.Lottie(
                            src="https://creativeferrets.com/assets/lottie/google.json",
                            width=30,
                            height=30,
                        ),
                        ft.Text("Continúa con Google", color=ft.Colors.WHITE,expand=True),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
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