import flet as ft
from pages.utils.navigation import create_footer, create_navbar_product

def ViewOrders(page):
    # Limpia la vista y configura la navegación
    page.controls.clear()
    navbar, _ = create_navbar_product(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()

    # Obtenemos la lista de pedidos guardada en session
    orders = page.session.get("orders") or []

    # Función para navegar al detalle de un pedido
    def go_to_order_detail(order_id):
        page.go(f"/order-detail/{order_id}")

    # Encabezado con logo e título
    header_container = ft.Container(
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(vertical=10),
        content=ft.Column(
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(
                    src="logo.png",  # Ajusta el path a tu logo/ícono
                    width=80,
                    height=80,
                ),
                ft.Text(
                    "Tus Pedidos",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
        ),
    )

    # Construimos la lista de pedidos (o el mensaje de “no hay pedidos”)
    order_items = []
    if not orders:
        # Si no hay pedidos, mostramos un contenedor con un mensaje
        order_items.append(
            ft.Container(
                alignment=ft.alignment.center,
                padding=ft.padding.all(10),
                content=ft.Text(
                    "No tienes pedidos realizados.",
                    size=16,
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.GREY,
                ),
            )
        )
    else:
        # Si hay pedidos, creamos un contenedor por cada uno
        for order in orders:
            order_item = ft.Container(
                padding=ft.padding.all(10),
                margin=ft.margin.symmetric(vertical=5),
                border_radius=ft.border_radius.all(8),
                # Puedes dar un color de fondo suave si deseas:
                # bgcolor="#f8f8f8",
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            f"ID Pedido: {order['id']}",
                            size=16,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            f"Total: ${order['total_price']}",
                            size=14,
                            color="green"
                        ),
                        ft.ElevatedButton(
                            text="Ver Detalle",
                            bgcolor="#FF5700",
                            color="white",
                            on_click=lambda e, order_id=order["id"]: go_to_order_detail(order_id),
                        ),
                    ],
                ),
            )
            order_items.append(order_item)

    # Columna donde se añaden todos los pedidos o el mensaje “sin pedidos”
    order_items_column = ft.Column(
        controls=order_items,
        spacing=10,
    )

    # Contenedor principal (fondo blanco por omisión)
    main_container = ft.Container(
        padding=ft.padding.all(10),
        expand=True,
        content=ft.Column(
            spacing=10,
            expand=True,
            controls=[
                header_container,
                ft.Divider(),
                order_items_column,
            ],
        ),
    )

    return main_container
