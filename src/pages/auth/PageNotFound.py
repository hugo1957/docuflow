import flet as ft
from pages.utils.navigation import create_footer, create_navbar_home


def PageNotFound(page):
    page.controls.clear()
    navbar, update_cart_count = create_navbar_home(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()

    not_found_image = ft.Image(
        src="icon.png",  # Reemplaza con la ruta de tu imagen
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )

    # Texto principal
    main_text = ft.Text(
        "¡Oops! La página que buscas no puede ser encontrada.",
        size=24,
        color="white",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    # Texto secundario
    secondary_text = ft.Text(
        "Si deseas, puedes volver a la tienda y buscar más documentos en DocuFlow.",
        size=16,
        color="white",
        text_align=ft.TextAlign.CENTER,
    )

    # Botón para ir a la tienda
    go_to_store_button = ft.ElevatedButton(
        text="Ir a la tienda",
        on_click=lambda e: page.go("/home"),
        bgcolor="#FF5700",
        color="white",
        width=150,
    )

    # Composición de la página
    content = ft.Container(
        bgcolor="#007354",
        padding=ft.padding.all(10),
        content=ft.Column(
            controls=[
                not_found_image,
                main_text,
                secondary_text,
                go_to_store_button,
                ft.Container(height=20),  # Espacio adicional
            ],
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
    )

    return content
