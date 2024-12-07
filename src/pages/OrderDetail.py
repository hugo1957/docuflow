import flet as ft
from pages.utils.navigation import create_footer, create_navbar_product

def ViewOrderDetail(page, order_id):
    navbar = create_navbar_product(page)[0]
    page.appbar = navbar
    page.navigation_bar = create_footer(page)

    orders = page.session.get("orders") or []
    order = next((o for o in orders if o["id"] == order_id), None)

    if not order:
        error_container = ft.Container(
            padding=ft.padding.all(10),
            content=ft.Text(
                f"No se encontró el pedido con ID {order_id}.",
                size=16,
                color=ft.Colors.RED,
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )
        return error_container

    order_details = ft.Column(
        controls=[
            ft.Text(f"ID del Pedido: {order['id']}", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Total: {order['total_price']}", size=16, color="green"),
            ft.Text("Información de Envío:", size=16, weight=ft.FontWeight.BOLD),
        ] + [
            ft.Text(f"{key}: {value}", size=14) for key, value in order["shipping_info"].items()
        ] + [
            ft.Divider(),
            ft.Text("Productos del Pedido:", size=16, weight=ft.FontWeight.BOLD),
        ] + [
            ft.Container(
                padding=ft.padding.all(10),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(item["name"], size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Cantidad: {item['quantity']}", size=14),
                        ft.Text(f"Total: ${float(item['price']) * item['quantity']:.2f}", size=14, color="green"),
                    ],
                ),
            )
            for item in order["cart"]
        ],
        spacing=10,
    )

    main_container = ft.Container(
        padding=ft.padding.all(10),
        content=ft.Column(
            controls=[
                ft.Text("Detalle del Pedido", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                order_details,
            ],
            expand=True,
        ),
    )

    return main_container
