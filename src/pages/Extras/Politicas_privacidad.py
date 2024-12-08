from pages.utils.navigation import create_navbar_product, create_footer
import flet as ft

def ViewPrivacyPolicy(page):
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
                ft.Text("Política de Privacidad", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Conoce cómo DocuFlow protege y utiliza tu información personal para brindarte un servicio seguro y confiable.",
                    size=14,
                    text_align=ft.TextAlign.JUSTIFY,
                ),
            ],
            spacing=10,
        ),
    )

    # Contenido de la política de privacidad
    privacy_content = [
        {
            "title": "1. Recopilación de Información",
            "description": (
                "Recopilamos información personal que tú nos proporcionas al registrarte, realizar compras, o interactuar con nuestros servicios. "
                "Esto incluye datos como tu nombre, correo electrónico, dirección, y detalles de pago."
            ),
        },
        {
            "title": "2. Uso de la Información",
            "description": (
                "Usamos tu información para procesar tus pedidos, personalizar tu experiencia, y mejorar nuestros servicios. "
                "También podemos usar tus datos para enviarte actualizaciones sobre nuestros productos y promociones."
            ),
        },
        {
            "title": "3. Compartición de Información",
            "description": (
                "No compartimos tu información personal con terceros, salvo cuando sea necesario para procesar tu pedido, cumplir con la ley, "
                "o proteger los derechos de DocuFlow y nuestros usuarios."
            ),
        },
        {
            "title": "4. Seguridad de los Datos",
            "description": (
                "Implementamos medidas de seguridad adecuadas para proteger tu información personal de accesos no autorizados, alteraciones, o divulgaciones."
            ),
        },
        {
            "title": "5. Tus Derechos",
            "description": (
                "Tienes derecho a acceder, corregir o eliminar tu información personal. Puedes contactarnos en cualquier momento para ejercer estos derechos."
            ),
        },
        {
            "title": "6. Cambios en la Política",
            "description": (
                "Nos reservamos el derecho de modificar esta política de privacidad en cualquier momento. Los cambios se publicarán en esta página."
            ),
        },
    ]

    # Renderiza las secciones de la política de privacidad
    privacy_controls = [
        ft.Container(
            padding=ft.padding.symmetric(vertical=10),
            content=ft.Column(
                controls=[
                    ft.Text(policy["title"], size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(policy["description"], size=14, text_align=ft.TextAlign.JUSTIFY),
                ],
                spacing=5,
            ),
        )
        for policy in privacy_content
    ]

    privacy_section = ft.Container(
        padding=ft.padding.symmetric(horizontal=20),
        content=ft.Column(controls=privacy_controls, spacing=15),
    )

    # Sección de finalización
    footer_section = ft.Container(
        padding=ft.padding.all(20),
        content=ft.Text(
            "Si tienes preguntas sobre nuestra política de privacidad, contáctanos en soporte@docuflow.com.",
            size=14,
            text_align=ft.TextAlign.CENTER,
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
                privacy_section,
                ft.Divider(height=1, thickness=1),
                footer_section,
            ],
            spacing=10,
        ),
    )

    return container
