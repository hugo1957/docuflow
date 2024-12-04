import flet as ft 
from pages.utils.navigation import create_footer, create_navbar_product
def ViewProductDetail(page):
    page.controls.clear()
    page.appbar = create_navbar_product(page)
    page.navigation_bar = create_footer(page)
    def buy_now(e):
        print("Buy Now clicked!")

    # Función para manejar el clic en los botones de tamaño
    def on_size_click(e):
        for button in size_buttons.controls:
            if button == e.control:
                button.bgcolor = "brown"
                button.content.color = "white"
            else:
                button.bgcolor = "#F5F5F5"
                button.content.color = "black"
        page.update()

    # Iconos con acciones
    product_actions = ft.Row(
        spacing=10,
        controls=[
            ft.Container(
                content=ft.Icon(ft.Icons.LOCAL_SHIPPING, size=20, color="brown"),
                bgcolor="#F5F5F5",
                padding=10,
                border_radius=8,
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.COFFEE, size=20, color="brown"),
                bgcolor="#F5F5F5",
                padding=10,
                border_radius=8,
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.EDIT, size=20, color="brown"),
                bgcolor="#F5F5F5",
                padding=10,
                border_radius=8,
            ),
        ],
    )

    # Información del producto
    product_info = ft.Column(
        spacing=5,
        controls=[
            ft.Text("Caffe Mocha", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(
                spacing=10,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("Ice/Hot", size=14, color=ft.Colors.GREY),
                    product_actions,  # Aquí colocamos las acciones
                ],
            ),
            ft.Row(
                spacing=5,
                controls=[
                    ft.Icon(name=ft.Icons.STAR, color="orange", size=16),
                    ft.Text("4.8", size=14, color="black"),
                    ft.Text("(230)", size=12, color=ft.Colors.GREY),
                ],
            ),
        ],
    )

    # Encabezado con la imagen del producto
    product_image = ft.Container(
        content=ft.Image(
            src="https://via.placeholder.com/400x200",  # Cambia por la URL de tu imagen
            fit=ft.ImageFit.COVER,
        ),
        width=page.window.width,
        height=200,
        border_radius=ft.border_radius.all(15),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    # Descripción del producto
    product_description = ft.Column(
        spacing=5,
        controls=[
            ft.Text("Description", size=16, weight=ft.FontWeight.BOLD),
            ft.Text(
                "A cappuccino is an approximately 150 ml (5 oz) beverage, with 25 ml of espresso coffee and 85 ml of fresh milk. Read More",
                size=14,
                color=ft.Colors.GREY,
            ),
        ],
    )

    # Tamaños disponibles (clickeables)
    size_buttons = ft.Row(
        spacing=30,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                content=ft.Text("S", size=14, color="black"),
                alignment=ft.alignment.center,
                bgcolor="#F5F5F5",
                padding=10,
                border_radius=8,
                width=50,
                height=40,
                ink=True,
                on_click=on_size_click,
            ),
            ft.Container(
                content=ft.Text("M", size=14, color="white"),
                alignment=ft.alignment.center,
                bgcolor="brown",
                padding=10,
                border_radius=8,
                width=50,
                height=40,
                ink=True,
                on_click=on_size_click,
            ),
            ft.Container(
                content=ft.Text("L", size=14, color="black"),
                alignment=ft.alignment.center,
                bgcolor="#F5F5F5",
                padding=10,
                border_radius=8,
                width=50,
                height=40,
                ink=True,
                on_click=on_size_click,
            ),
        ],
    )

    # Precio y botón de compra
    product_price_and_button = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Text("Price\n$ 4.53", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Text("Buy Now", size=14, color="white"),
                alignment=ft.alignment.center,
                bgcolor="brown",
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                border_radius=8,
                on_click=buy_now,
            ),
        ],
    )

    # Contenedor principal del producto
    product_detail_container = ft.Container(
        padding=ft.padding.all(10),
        alignment=ft.alignment.center,
        expand=True,
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                product_image,
                product_info,
                ft.Divider(),
                product_description,
                ft.Text("Size", size=16, weight=ft.FontWeight.BOLD),
                size_buttons,  # Aquí están los botones clickeables
                ft.Divider(),
                product_price_and_button,
                ft.Container(height=10),
            ],
        ),
    )

    # Retorna el contenedor completo
    return product_detail_container