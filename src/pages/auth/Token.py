import flet as ft

def ViewToken(page):
    page.controls.clear()
    page.update()
    token_fields = []
    for i in range(6):
        token_fields.append(
            ft.TextField(
                width=50,
                height=60,
                border_radius=ft.border_radius.all(15),
                text_align=ft.TextAlign.CENTER,
                bgcolor=ft.Colors.WHITE,
                border_color="#717171",
                label_style=ft.TextStyle(color="#717171"),
                border_width=2,
                expand=True,
                max_length=1,
                keyboard_type=ft.KeyboardType.NUMBER,
                on_change=lambda e, i=i: handle_text_change(e, i)
            )
        )

    def handle_text_change(e, index):
        # Validar que solo se ingresen números
        if not e.control.value.isdigit():
            e.control.value = ""
            page.update()
            return

        # Mover el foco al siguiente campo si hay un valor
        if e.control.value and index < len(token_fields) - 1:
            token_fields[index + 1].focus()
        page.update()

    def handle_verify_click(e):
        # Obtenemos el código ingresado uniendo el valor de cada TextField
        code = "".join(field.value.strip() for field in token_fields)
        if len(code) < 6:
            # Muestra un SnackBar si no se han ingresado los 6 dígitos
            snack_bar = ft.SnackBar(
                ft.Text("Debes ingresar los 6 dígitos del código!"), bgcolor=ft.Colors.RED_500
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            return

        # Aquí puedes agregar la lógica para verificar el token
        # Por ejemplo: verify_token(page, code)
        print(f"Código ingresado: {code}")
        page.go("/home")
        # Si el token es válido:
        # page.go("/alguna-ruta-de-exito")

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
                        ft.Text(
                            "Verificación de Código",
                            size=20,
                            color=ft.Colors.BLACK,
                            weight=ft.FontWeight.W_100,
                            font_family="Heavitas"
                        ),
                        ft.Text(
                            "Ingresa el código de 6 dígitos que recibiste",
                            size=15,
                            color=ft.Colors.BLACK,
                            font_family="Poppins"
                        ),
                        ft.Row(
                            controls=token_fields,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10
                        ),
                        ft.Container(
                            alignment=ft.alignment.center,
                            on_click=handle_verify_click,
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
                                "Verificar Código", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            padding=ft.padding.all(10),
                        ),
                    ]
                )
            )
        ]
    )
    return container