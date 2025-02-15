import flet as ft
from pages.utils.navigation import create_footer, create_navbar_product
from pages.utils.controls.numero_telefono import PhoneInputDropdown
from pages.utils.controls.inputs import MyInputField

def ViewRegisterDomiciliario(page):
    def on_register(e):
        print("Registro enviado")

    def handle_country_change(selected_country):
        print(f"País seleccionado: {selected_country}")

    def handle_phone_change(phone_number):
        print(f"Número ingresado: {phone_number}")

    phone_input = PhoneInputDropdown(
        on_country_change=handle_country_change,
        on_phone_change=handle_phone_change,
    )

    page.controls.clear()
    page.appbar = create_navbar_product(page)[0]
    page.navigation_bar = create_footer(page)
    page.update()

    # Aquí metemos el checkbox en una fila, y al lado el texto largo
    checkbox1 = ft.Checkbox(value=False)
    text1 = ft.Text(
        "Acepto expresamente la autorización de tratamiento de datos personales y la Política de Tratamiento de Datos Personales de DocuFlow.",
        max_lines=None,  # Para que no corte
        overflow=ft.TextOverflow.CLIP,
        expand=True,
        text_align=ft.TextAlign.START,
    )

    checkbox2 = ft.Checkbox(value=False)
    text2 = ft.Text(
        "Acepto expresamente las condiciones de activación de mi cuenta al interior de 'DocuFlow Domicilios'.",
        max_lines=None,
        overflow=ft.TextOverflow.CLIP,
        text_align=ft.TextAlign.START,
        expand=True
    )

    terms_section = ft.Container(
      content=ft.Column(
        controls=[
            ft.Row([checkbox1,text1], vertical_alignment=ft.CrossAxisAlignment.CENTER,alignment=ft.MainAxisAlignment.CENTER,expand=True),
            ft.Row([checkbox2,text2], vertical_alignment=ft.CrossAxisAlignment.CENTER,alignment=ft.MainAxisAlignment.CENTER,expand=True),
        ],
        expand=True,
        spacing=10,
    ),
      expand=True,
    )

    register_button = ft.Container(
        content=ft.ElevatedButton("Crear cuenta", on_click=on_register),
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(vertical=10),
    )

    password_field = ft.Column(
        controls=[
            ft.Text("Contraseña", style=ft.TextStyle(color="#717171")),
            ft.TextField(
                password=True,
                can_reveal_password=True,
                border_radius=ft.border_radius.all(15),
                content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
                bgcolor=ft.Colors.WHITE,
                border_color="#717171",
                label_style=ft.TextStyle(color="#717171"),
                border_width=0.5,
                expand=True,
                filled=False,
            ),
        ]
    )

    repeat_password_field = ft.Column(
        controls=[
            ft.Text("Repetir contraseña", style=ft.TextStyle(color="#717171")),
            ft.TextField(
                password=True,
                can_reveal_password=True,
                border_radius=ft.border_radius.all(15),
                content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
                bgcolor=ft.Colors.WHITE,
                border_color="#717171",
                label_style=ft.TextStyle(color="#717171"),
                border_width=0.5,
                expand=True,
                filled=False,
            ),
        ]
    )

    container = ft.Container(
        padding=ft.padding.all(20),
        content=ft.Column(
            controls=[
                ft.Text("Crea tu cuenta", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("¡Regístrate y empieza a trabajar!", size=18, weight=ft.FontWeight.BOLD),
                MyInputField("Nombre"),
                MyInputField("Apellidos"),
                MyInputField("Correo electrónico"),
                ft.Column(
                    spacing=0,
                    controls=[
                        ft.Text("Número de teléfono", style=ft.TextStyle(color="#717171")),
                        phone_input,
                    ]
                ),
                password_field,
                repeat_password_field,
                terms_section,
                register_button,
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO
        ),
    )

    return container
