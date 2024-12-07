import flet as ft
from pages.utils.navigation import create_footer, create_navbar_product

def ViewOrders(page):
    navbar = create_navbar_product(page)[0]
    page.appbar = navbar
    page.navigation_bar = create_footer(page)

    orders = page.session.get("orders") or [] 

    def go_to_order_detail(order_id):
        page.go(f"/order-detail/{order_id}")

    order_items = []
    for order in orders:
        order_item = ft.Container(
            padding=ft.padding.all(10),
            margin=ft.margin.symmetric(vertical=5),
            border_radius=ft.border_radius.all(8),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(f"ID Pedido: {order['id']}", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Total: {order['total_price']}", size=14, color="green"),
                    ft.ElevatedButton(
                        text="Ver Detalle",
                        bgcolor="#e5bc16",
                        color="white",
                        on_click=lambda e, order_id=order["id"]: go_to_order_detail(order_id),
                    ),
                ],
            ),
        )
        order_items.append(order_item)

    if not order_items:
        order_items.append(
            ft.Container(
                padding=ft.padding.all(10),
                content=ft.Text(
                    "No tienes pedidos realizados.",
                    size=16,
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.GREY,
                ),
                alignment=ft.alignment.center,
            )
        )

    main_container = ft.Container(
        padding=ft.padding.all(10),
        content=ft.Column(
            controls=[
                ft.Text("Tus Pedidos", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                *order_items,
            ],
            expand=True,
            spacing=10,
        ),
    )

    return main_container
