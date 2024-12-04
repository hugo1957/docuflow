
import flet as ft
def create_content(image, name, valor, url):
    return ft.Container(
        width=180,
        height=260,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    padding=ft.padding.all(0),
                    alignment=ft.alignment.top_right,
                    content=ft.IconButton(
                        icon=ft.Icons.SHOPPING_CART_OUTLINED,
                        icon_color="#FFBC03",
                        icon_size=20,
                        tooltip="Agregar al carrito",

                    ),
                ),
                ft.Container(
                    expand=True,
                    padding=ft.padding.all(0),
                    border_radius=ft.border_radius.all(100),
                    content=ft.Image(
                        src=image,
                        width=120,
                        height=120,
                    ),
                ),
                ft.Text(
                    name,
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                ),
                ft.Text(
                    f"Valor: {valor}",
                    size=12,
                    color=ft.Colors.BLACK54,
                ),
            ],
        ),
        padding=ft.padding.all(10),
        border_radius=ft.border_radius.all(10),
        bgcolor=ft.Colors.BLUE,
    )