import flet as ft

def WelcomeView(page):
    page.controls.clear()
    page.appbar = ft.CupertinoAppBar(bgcolor=ft.Colors.WHITE, visible=False)
    page.update()

    # Header del contenedor
    header = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Row(
                        [
                            ft.Image(src="flags/co.png", width=20),
                            ft.Text("Colombia", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
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

    # Función para crear botones con animación
    def create_buttons():
        buttons = []

        # Botón común para todas las plataformas
        buttons.append(
            ft.Container(
                alignment=ft.alignment.center,
                on_click=lambda e: page.go("/phone-login"),
                border_radius=ft.border_radius.all(15),
                height=50,
                bgcolor=ft.Colors.GREEN,
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.PHONE, color=ft.Colors.WHITE),
                        ft.Text(
                            "Continúa con tu celular",
                            size=15,
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            )
        )

        # Botón para Apple (solo en iOS)
        if page.platform == ft.PagePlatform.IOS:
            buttons.append(
                ft.Container(
                    alignment=ft.alignment.center,
                    border_radius=ft.border_radius.all(15),
                    height=50,
                    bgcolor=ft.Colors.BLACK,
                    content=ft.Row(
                        controls=[
                            ft.Lottie(
                                src="https://creativeferrets.com/assets/lottie/apple.json",
                                animate=True,
                                width=30,
                                height=30,
                            ),
                            ft.Text(
                                "Continúa con Apple",
                                size=15,
                                color=ft.Colors.WHITE,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                )
            )

        # Botón para Google (solo en Android)
        if page.platform == ft.PagePlatform.ANDROID:
            buttons.append(
                ft.Container(
                    alignment=ft.alignment.center,
                    border_radius=ft.border_radius.all(15),
                    height=50,
                    bgcolor=ft.Colors.BLUE,
                    content=ft.Row(
                        controls=[
                            ft.Lottie(
                                src="https://creativeferrets.com/assets/lottie/google.json",
                                width=30,
                                height=30,
                            ),
                            ft.Text(
                                "Continúa con Google",
                                size=15,
                                color=ft.Colors.WHITE,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                )
            )

        # Mostrar todos los botones si no es ninguna de las plataformas
        if page.platform not in [ft.PagePlatform.IOS, ft.PagePlatform.ANDROID]:
            buttons.extend(
                [
                    ft.Container(
                        alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(15),
                        height=50,
                        bgcolor=ft.Colors.BLUE,
                        content=ft.Row(
                            controls=[
                                ft.Lottie(
                                    src="https://creativeferrets.com/assets/lottie/google.json",
                                    width=30,
                                    height=30,
                                ),
                                ft.Text(
                                    "Continúa con Google",
                                    size=15,
                                    color=ft.Colors.WHITE,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ),
                    ft.Container(
                        alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(15),
                        height=50,
                        bgcolor=ft.Colors.BLACK,
                        content=ft.Row(
                            controls=[
                                ft.Lottie(
                                    src="https://creativeferrets.com/assets/lottie/apple.json",
                                    animate=True,
                                    width=30,
                                    height=30,
                                ),
                                ft.Text(
                                    "Continúa con Apple",
                                    size=15,
                                    color=ft.Colors.WHITE,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ),
                ]
            )

        buttons.append(
            ft.TextButton(
                "Soy usuario registrado",
                style=ft.ButtonStyle(color=ft.Colors.GREEN),
                on_click=lambda e: page.go("/login"),
            )
        )

        return ft.AnimatedSwitcher(
            content=ft.Column(
                controls=buttons,
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=500,
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
                create_buttons(),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
    )

    return main_container