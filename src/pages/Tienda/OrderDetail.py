import flet as ft
from pages.utils.navigation import create_footer, create_navbar_product


def build_order_timeline(current_step: int) -> ft.Row:
    statuses = ["Validando", "En proceso", "En camino", "Entregado"]
    circle_size = 28
    line_width = 80

    def circle_color(i: int) -> str:
        if i < current_step:
            return "#28A745"
        elif i == current_step:
            return "#FFD966"
        else:
            return "#CCCCCC"

    def line_color(i: int) -> str:
        return "#28A745" if i < current_step else "#CCCCCC"

    row_controls = []

    for i, label in enumerate(statuses):
        step_circle = ft.Container(
            width=circle_size,
            height=circle_size,
            border_radius=ft.border_radius.all(circle_size / 2),
            bgcolor=circle_color(i),
        )

        step_top = ft.Row(
            controls=[step_circle],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        step_label = ft.Text(label, size=12, text_align=ft.TextAlign.CENTER)

        step_column = ft.Column(
            spacing=5,
            controls=[step_top, step_label],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        row_controls.append(step_column)

        if i < len(statuses) - 1:
            line = ft.Container(
                width=line_width,
                height=2,
                bgcolor=line_color(i),
                alignment=ft.alignment.center,
            )
            row_controls.append(line)

    timeline_row = ft.Container(
        content=ft.Row(
            controls=row_controls,
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            scroll=ft.ScrollMode.HIDDEN,
        ),
        padding=ft.padding.all(10),
    )
    return timeline_row


def ViewOrderDetail(page, order_id):
    order_id = 1
    page.controls.clear()
    navbar = create_navbar_product(page)[0]
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()
    orders = page.session.get("orders") or []
    order = next((o for o in orders if o["id"] == order_id), None)

    if not order:
        error_container = ft.Container(
            padding=ft.padding.all(10),
            content=ft.Column(
                controls=[
                    ft.Image(src="logo.png", width=150, height=150),
                    ft.Text(
                        f"No se encontró el pedido con número {order_id}.",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.ElevatedButton(
                        text="Volver a la tienda",
                        on_click=lambda e: page.go("/home"),
                        bgcolor="#FF5700",
                        color="white",
                        width=150,
                    ),
                    ft.ElevatedButton(
                        text="Ver Órdenes de Compra",
                        on_click=lambda e: page.go("/orders"),
                        bgcolor="#FF5700",
                        color="white",
                        width=170,
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )
        return error_container

    timeline = build_order_timeline(order.get("status", 1))

    order_details = ft.Column(
        spacing=15,
        controls=[
            ft.Text(f"ID del Pedido: {order['id']}",
                    size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Total: ${order['total_price']:.2f}",
                    size=18, color="green"),
            ft.Text("Información de Envío",
                    size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                padding=ft.padding.symmetric(vertical=5),
                content=ft.Column(
                    spacing=5,
                    controls=[
                        ft.Text(
                            f"{key.capitalize()}: {value}", size=16
                        )
                        for key, value in order["shipping_info"].items()
                    ],
                ),
            ),
            ft.Divider(),
            ft.Text("Productos del Pedido",
                    size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                padding=ft.padding.symmetric(vertical=5),
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Container(
                            padding=ft.padding.all(10),
                            bgcolor="#FAFAFA",
                            border_radius=8,
                            content=ft.Column(
                                spacing=5,
                                controls=[
                                    ft.Text(item["name"],
                                            size=16,
                                            weight=ft.FontWeight.BOLD),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(f"Cantidad: {item['quantity']}",
                                                    size=14),
                                            ft.Text(
                                                f"Total: ${item['price'] *
                                                           item['quantity']:.2f}",
                                                size=14,
                                                color="green",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        )
                        for item in order["cart"]
                    ],
                ),
            ),
        ],
    )

    main_container = ft.Container(
        padding=ft.padding.all(10),
        expand=True,
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text(
                    "Detalle del Pedido",
                    size=24,
                    weight=ft.FontWeight.BOLD
                ),
                timeline,
                ft.Divider(),
                order_details,
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    return main_container
