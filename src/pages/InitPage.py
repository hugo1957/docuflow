import flet as ft
def WelcomeView(page):
    def navigate_to(e, url):
        page.go(url)

    page.controls.clear()

    # Encabezado
    header = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.FLAG, color=ft.colors.YELLOW),
                            ft.Text("Colombia", color=ft.colors.BLACK,
                                    weight=ft.FontWeight.BOLD),
                        ],
                        spacing=5,
                    ),
                    border_radius=15,
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    bgcolor=ft.colors.BLACK12,
                ),
                ft.Text(
                    "Regístrate y simplifica tu vida",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.WHITE,
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
                    bgcolor=ft.colors.GREEN, color=ft.colors.WHITE, shape=ft.RoundedRectangleBorder(
                        radius=10)
                ),
                width=300,
                on_click=lambda e: navigate_to(e, "/phone-login"),
            ),
            ft.ElevatedButton(
                "Continúa con Apple",
                icon=ft.Icons.APPLE,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.BLACK, color=ft.colors.WHITE, shape=ft.RoundedRectangleBorder(
                        radius=10)
                ),
                width=300,
                on_click=lambda e: navigate_to(e, "/apple-login"),
            ),
            
            ft.ElevatedButton(
                "Continúa con Google",
                icon=ft.Icons.ABC_ROUNDED,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.BLUE, color=ft.colors.WHITE, shape=ft.RoundedRectangleBorder(
                        radius=10)
                ),
                width=300,
                on_click=lambda e: navigate_to(e, "/google-login"),
            ),
            ft.TextButton(
                "Soy usuario registrado",
                style=ft.ButtonStyle(color=ft.colors.GREEN),
                on_click=lambda e: navigate_to(e, "/login"),
            ),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Contenedor principal
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