from pages.utils.navigation import create_navbar_product, create_footer
import flet as ft

def ViewTermsAndConditions(page):
    page.controls.clear()
    page.appbar = create_navbar_product(page)[0]
    page.navigation_bar = create_footer(page)
    page.update()

    header_section = ft.Container(
        padding=ft.padding.all(20),
        content=ft.Column(
            controls=[
                ft.Text("Términos y Condiciones", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "A continuación, se detallan los términos y condiciones del servicio de generación de documentos legales en DocuFlow.",
                    size=14,
                    text_align=ft.TextAlign.JUSTIFY,
                ),
            ],
            spacing=10,
        ),
    )
    
    terms_content = [
        {
            "title": "1. Uso del Servicio",
            "description": (
                "DocuFlow proporciona una plataforma para la generación de documentos legales personalizados. "
                "El usuario es responsable de garantizar la exactitud de la información proporcionada."
            ),
        },
        {
            "title": "2. Propiedad Intelectual",
            "description": (
                "Todos los derechos de los documentos generados, plantillas y materiales proporcionados por DocuFlow "
                "son propiedad de la empresa y están protegidos por leyes de derechos de autor."
            ),
        },
        {
            "title": "3. Privacidad de los Datos",
            "description": (
                "DocuFlow se compromete a proteger la privacidad de los datos del usuario. Consulte nuestra "
                "Política de Privacidad para obtener más detalles."
            ),
        },
        {
            "title": "4. Limitación de Responsabilidad",
            "description": (
                "DocuFlow no es responsable de los errores en los documentos generados debido a información incorrecta "
                "proporcionada por el usuario."
            ),
        },
        {
            "title": "5. Tarifas y Pagos",
            "description": (
                "El uso de los servicios de DocuFlow está sujeto a las tarifas vigentes en el momento de la compra. "
                "Estas tarifas no son reembolsables, salvo en casos excepcionales especificados en nuestras políticas."
            ),
        },
    ]

    terms_controls = [
        ft.Container(
            padding=ft.padding.symmetric(vertical=10),
            content=ft.Column(
                controls=[
                    ft.Text(term["title"], size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(term["description"], size=14, text_align=ft.TextAlign.JUSTIFY),
                ],
                spacing=5,
            ),
        )
        for term in terms_content
    ]

    terms_section = ft.Container(
        padding=ft.padding.symmetric(horizontal=20),
        content=ft.Column(controls=terms_controls, spacing=15),
    )

    footer_section = ft.Container(
        padding=ft.padding.all(20),
        content=ft.Text(
            "Si tienes alguna pregunta sobre estos términos y condiciones, no dudes en contactarnos a soporte@docuflow.com.",
            size=14,
            text_align=ft.TextAlign.CENTER,
        ),
    )

    container = ft.Container(
        padding=ft.padding.all(10),
        content=ft.Column(
            scroll=ft.ScrollMode.HIDDEN,
            controls=[
                header_section,
                ft.Divider(height=1, thickness=1),
                terms_section,
                ft.Divider(height=1, thickness=1),
                footer_section,
            ],
            spacing=10,
        ),
    )

    return container
