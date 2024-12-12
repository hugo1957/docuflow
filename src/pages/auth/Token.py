import flet as ft
from pages.endpoints.Auth import verify_token, resend_code
import threading
import time

def ViewToken(page):
    page.controls.clear()
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_CIRCLE_LEFT,
                            autofocus=False,on_click=lambda e: page.go("/phone-login"),
        hover_color=ft.Colors.TRANSPARENT,icon_color="#007354"),
        leading_width=60,
        bgcolor=ft.Colors.WHITE)
    page.navigation_bar = None
    page.update()

    countdown_seconds = 120  # 2 minutos
    countdown_label = ft.Text("", size=14, color=ft.Colors.GREY_600)

    resend_button = ft.Container(
        alignment=ft.alignment.center,
        on_click=None,
        border_radius=ft.border_radius.all(5),
        width=350,
        height=50,
        bgcolor=ft.Colors.GREEN,
        visible=False,
        content=ft.Text(
            "Reenviar código",
            size=15,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
        ),
    )

    phone = page.client_storage.get("creativeferrets.tienda.phone_number")

    def create_token_fields():
        return [
            ft.TextField(
                width=50,
                height=60,
                border_radius=ft.border_radius.all(15),
                text_align=ft.TextAlign.CENTER,
                bgcolor=ft.Colors.WHITE,
                border_color="#717171",
                border_width=0.5,
                expand=True,
                max_length=1,
                on_change=lambda e, i=i: handle_text_change(e, i),
            )
            for i in range(6)
        ]

    token_fields = create_token_fields()

    def handle_text_change(e, index):
        # Asegurarse de que solo se permitan dígitos
        if not e.control.value.isdigit() and e.control.value:
            e.control.value = ""
            page.update()
            return

        # Navegar hacia adelante si se ingresa un valor
        if e.control.value and index < len(token_fields) - 1:
            token_fields[index + 1].focus()
        # Navegar hacia atrás si el campo está vacío
        elif not e.control.value and index > 0:
            token_fields[index - 1].focus()

        page.update()

    def handle_verify_click(e):
        code = "".join(field.value.strip() for field in token_fields)

        if len(code) < 6:
            snack_bar = ft.SnackBar(
                ft.Text("Debes ingresar los 6 dígitos del código!"),
                bgcolor=ft.Colors.RED_500,
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            return

        if verify_token(page, code):
            page.go("/home")
        else:
            snack_bar = ft.SnackBar(
                ft.Text("Error al verificar el código."),
                bgcolor=ft.Colors.RED_500,
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True

    def handle_resend_click(e):
        if resend_code(page, phone):
            snack_bar = ft.SnackBar(
                ft.Text("Código reenviado con éxito."),
                bgcolor=ft.Colors.GREEN_500,
            )
            start_countdown()
        else:
            snack_bar = ft.SnackBar(
                ft.Text("Error al reenviar el código."),
                bgcolor=ft.Colors.RED_500,
            )
        page.overlay.append(snack_bar)
        snack_bar.open = True

    def start_countdown():
        nonlocal countdown_seconds
        countdown_seconds = 120  # 2 minutos
        resend_button.visible = False
        countdown_label.value = format_time(countdown_seconds)
        page.update()

        def countdown():
            nonlocal countdown_seconds
            while countdown_seconds > 0:
                time.sleep(1)
                countdown_seconds -= 1
                countdown_label.value = format_time(countdown_seconds)
                page.update()
            resend_button.visible = True
            resend_button.on_click = handle_resend_click
            page.update()

        threading.Thread(target=countdown).start()

    def format_time(seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"Podrás solicitar un código nuevo en {minutes:02d}:{seconds:02d}"

    start_countdown()

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
                        ft.Text("Verificación de Código 👀", size=20, color=ft.Colors.BLACK, weight=ft.FontWeight.W_100),
                        ft.Text(
                            f"A TU NÚMERO CELULAR {phone}",
                            size=15,
                            color=ft.Colors.GREEN,
                        ),
                        ft.Row(
                            controls=token_fields,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                            expand=True,
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
                        ft.Container(
                            alignment=ft.alignment.center,
                            content=ft.Text("¿No recibiste el código?", size=12, color=ft.Colors.BLACK),
                        ),
                        countdown_label,
                        resend_button,
                    ],
                ),
            )
        ],
    )
    return container
