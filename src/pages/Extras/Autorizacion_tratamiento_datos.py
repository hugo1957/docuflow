from pages.utils.navigation import create_navbar_product, create_footer
import flet as ft

def ViewDataAuthorization(page):
    # Limpia controles anteriores
    page.controls.clear()
    page.appbar = create_navbar_product(page)[0]
    page.navigation_bar = create_footer(page)
    page.update()

    # Encabezado de la sección
    header_section = ft.Container(
        padding=ft.padding.all(20),
        content=ft.Column(
            controls=[
                ft.Text("Autorización de Tratamiento de Datos", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "DocuFlow solicita tu autorización para el tratamiento de tus datos personales, de acuerdo con nuestra política de privacidad y las leyes aplicables.",
                    size=14,
                    text_align=ft.TextAlign.JUSTIFY,
                ),
            ],
            spacing=10,
        ),
    )

    # Contenido de la autorización de tratamiento de datos
    authorization_content = [
        {
            "title": "1. Finalidad del Tratamiento",
            "description": (
                "Los datos personales que recopilamos serán utilizados para las siguientes finalidades: "
                "gestionar tu registro, procesar pedidos, realizar comunicaciones relacionadas con nuestros servicios, "
                "y enviarte información sobre promociones y ofertas."
            ),
        },
        {
            "title": "2. Responsabilidad",
            "description": (
                "DocuFlow es responsable del manejo de tus datos personales, garantizando su seguridad y confidencialidad. "
                "Solo serán tratados por personal autorizado y en cumplimiento de las leyes aplicables."
            ),
        },
        {
            "title": "3. Derechos del Titular",
            "description": (
                "Como titular de los datos, tienes derecho a acceder, actualizar, rectificar y solicitar la eliminación de tu información. "
                "Puedes ejercer estos derechos contactándonos a soporte@docuflow.com."
            ),
        },
        {
            "title": "4. Compartición de Datos",
            "description": (
                "Tus datos personales no serán compartidos con terceros sin tu autorización previa, salvo en casos necesarios para "
                "cumplir con obligaciones legales o para la prestación de los servicios ofrecidos por DocuFlow."
            ),
        },
        {
            "title": "5. Vigencia de la Autorización",
            "description": (
                "Tu autorización para el tratamiento de datos será válida durante el tiempo necesario para cumplir las finalidades descritas "
                "o según lo exijan las leyes aplicables."
            ),
        },
    ]

    # Renderiza las secciones de la autorización
    authorization_controls = [
        ft.Container(
            padding=ft.padding.symmetric(vertical=10),
            content=ft.Column(
                controls=[
                    ft.Text(item["title"], size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(item["description"], size=14, text_align=ft.TextAlign.JUSTIFY),
                ],
                spacing=5,
            ),
        )
        for item in authorization_content
    ]

    authorization_section = ft.Container(
        padding=ft.padding.symmetric(horizontal=20),
        content=ft.Column(controls=authorization_controls, spacing=15),
    )

    # Sección de aceptación
    acceptance_section = ft.Container(
        padding=ft.padding.all(20),
        content=ft.Column(
            controls=[
                ft.Text(
                    "Al continuar utilizando nuestros servicios, confirmas que aceptas nuestra política de tratamiento de datos personales.",
                    size=14,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.ElevatedButton(
                            text="Aceptar",
                            on_click=lambda e: page.go("/home"),
                            bgcolor="#007354",
                            color=ft.Colors.WHITE,
                            width=150,
                        ),
                        ft.ElevatedButton(
                            text="Rechazar",
                            on_click=lambda e: page.go("/"),
                            bgcolor=ft.Colors.RED,
                            color=ft.Colors.WHITE,
                            width=150,
                        ),
                    ],
                ),
            ],
            spacing=20,
        ),
    )

    # Contenedor principal
    container = ft.Container(
        padding=ft.padding.all(10),
        content=ft.Column(
            scroll=ft.ScrollMode.HIDDEN,
            controls=[
                header_section,
                ft.Divider(height=1, thickness=1),
                authorization_section,
                ft.Divider(height=1, thickness=1),
                acceptance_section,
            ],
            spacing=10,
        ),
    )

    return container
