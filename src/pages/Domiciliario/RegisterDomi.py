
import flet as ft
from pages.utils.numero_telefono import PhoneInputDropdown
from pages.utils.inputs import create_input_field
from pages.utils.navigation import create_footer, create_navbar_home

def ViewRegisterDomiciliario(page):
    
    def on_register(e):
        # Aquí manejas el registro del domiciliario
        print("Registro enviado")

    def handle_country_change(selected_country):
        print(f"País seleccionado: {selected_country}")

    def handle_phone_change(phone_number):
        print(f"Número ingresado: {phone_number}")

    # Inicializar el componente de entrada de teléfono
    phone_input = PhoneInputDropdown(
        on_country_change=handle_country_change,
        on_phone_change=handle_phone_change,
    )

    page.controls.clear()
    page.appbar = create_navbar_home(page)[0]
    page.navigation_bar = create_footer(page)
    page.update()

    # Campo de contraseña y repetir contraseña
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
            ),
        ]
    )

    # Sección de términos ajustada para evitar desbordamiento
    terms_section = ft.Column(
        controls=[
            ft.Checkbox(
                label=(
                    "Acepto expresamente la autorización de tratamiento de datos personales "
                    "y la Política de Tratamiento de Datos Personales de DocuFlow."
                ),

            ),
            ft.Checkbox(
                label=(
                    "Acepto expresamente las condiciones de activación de mi cuenta al "
                    "interior de 'DocuFlow Domicilios'."
                ),

            ),
        ],
        spacing=10,
    )

    # Botón de registro
    register_button = ft.Container(
        content=ft.ElevatedButton("Crear cuenta", on_click=on_register),
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(vertical=10),
    )

    # Contenedor principal
    container = ft.Container(
        padding=ft.padding.all(20),
        content=ft.Column(
            controls=[
                ft.Text("Crea tu cuenta", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "¡Regístrate y empieza a trabajar!", size=18, weight=ft.FontWeight.BOLD
                ),
               
                create_input_field("Nombre"),
                create_input_field("Apellidos"),
                create_input_field("Correo electrónico"),
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
