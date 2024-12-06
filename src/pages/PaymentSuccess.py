import flet as ft
from pages.utils.navigation import create_footer, create_navbar_product

def ViewPaymentSuccess(page):
    page.controls.clear()
    page.appbar = create_navbar_product(page)[0]
    page.navigation_bar = create_footer(page)

    success_view = ft.Container(
        padding=ft.padding.all(10),
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=[
                ft.Image(
                    src="icon.png",
                    width=150,
                    height=150,
                ),
                ft.Text(
                    "¡Gracias por tu compra!",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Tu pedido ha sido procesado con éxito.",
                    size=16,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.ResponsiveRow(
                    controls=[
                        ft.ElevatedButton(
                    text="Volver al inicio",
                    on_click=lambda e: page.go("/"),
                    bgcolor="#e5bc16",
                    color="white",
                    width=150,
                ),
                        ft.ElevatedButton(
                    text="Ver Orden de Compra",
                    on_click=lambda e: page.go("/orden-de-compra"),
                    bgcolor="#e5bc16",
                    color="white",
                    width=150,
                )
                    ])
            ],
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )
    return success_view 