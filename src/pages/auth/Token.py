import flet as ft

def ViewToken(page):
    page.controls.clear()
    page.appbar = ft.AppBar(
        bgcolor=ft.Colors.WHITE,
    )
    page.navigation_bar = None
    page.update()
    token_fields = [
        ft.TextField(
            width=50,
            height=60,
            border_radius=ft.border_radius.all(15),
            text_align=ft.TextAlign.CENTER,
            bgcolor=ft.Colors.WHITE,
            border_color="#717171",
            border_width=2,
            expand=True,
            max_length=1,
            on_change=lambda e, i=i: handle_text_change(e, i),
        )
        for i in range(6)
    ]

    def handle_text_change(e, index):
        if not e.control.value.isdigit():
            e.control.value = ""
            page.update()
            return

        if e.control.value and index < len(token_fields) - 1:
            token_fields[index + 1].focus()
        elif not e.control.value and index > 0:
            token_fields[index - 1].focus()
        page.update()

    def handle_verify_click(e):
        code = "".join(field.value.strip() for field in token_fields)
        if len(code) < 6:
            snack_bar = ft.SnackBar(ft.Text("Debes ingresar los 6 dígitos del código!"), bgcolor=ft.Colors.RED_500)
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            return
        page.go("/home")

    container = ft.Column(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
        spacing=0,
        controls=[
            ft.Container(
                padding=ft.padding.all(20),
                expand=True,
                content=ft.Column(
                    spacing=20,
                    horizontal_alignment="center",
                    scroll=ft.ScrollMode.HIDDEN,
                    controls=[
                        ft.Container(height=5),
                        ft.Text("Verificación de Código", size=20, color=ft.Colors.BLACK, weight=ft.FontWeight.W_100),
                        ft.Text("Ingresa el código de 6 dígitos que recibiste por SMS o WhastApp", size=15, color=ft.Colors.BLACK),
                        ft.Row(
                            controls=token_fields,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        ft.Container(
                            alignment=ft.alignment.center,
                            on_click=handle_verify_click,
                            ink=True,
                            border_radius=ft.border_radius.all(5),
                            width=350,
                            height=50,
                            bgcolor=ft.Colors.GREEN,
                            content=ft.Text("Verificar Código", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            padding=ft.padding.all(10),
                        ),
                    ],
                ),
            )
        ],
    )
    return container
