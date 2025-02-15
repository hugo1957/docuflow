import flet as ft
from pages.utils.navigation import create_footer, create_navbar_product
from pages.endpoints.Orders import get_order_detail

def build_order_timeline(current_step: str) -> ft.Row:
    """
    Construye una fila con el "timeline" de un pedido,
    basado en la etapa actual (current_step).
    """
    statuses = {
        "not_processed": "No procesado",
        "processed": "Procesado",
        "shipped": "Enviado",
        "delivered": "Entregado",
        "cancelled": "Cancelado",
    }
    circle_size = 28
    line_width = 80

    def circle_color(status: str) -> str:
        # Si es la etapa actual -> amarillo, si es anterior -> verde, si es futuro -> gris
        if status == current_step:
            return "#FFD966"   # Amarillo
        elif list(statuses.keys()).index(status) < list(statuses.keys()).index(current_step):
            return "#28A745"   # Verde
        else:
            return "#CCCCCC"   # Gris

    def line_color(status: str) -> str:
        # Línea verde si la etapa ya pasó, gris si no
        return "#28A745" if list(statuses.keys()).index(status) < list(statuses.keys()).index(current_step) else "#CCCCCC"

    row_controls = []
    status_keys = list(statuses.keys())
    num_statuses = len(status_keys)

    for i, (status, label) in enumerate(statuses.items()):
        # Círculo para la etapa
        step_circle = ft.Container(
            width=circle_size,
            height=circle_size,
            border_radius=ft.border_radius.all(circle_size / 2),
            bgcolor=circle_color(status),
        )
        # Etiqueta
        step_top = ft.Row(controls=[step_circle], alignment=ft.MainAxisAlignment.CENTER)
        step_label = ft.Text(label, size=12, text_align=ft.TextAlign.CENTER)
        step_column = ft.Column(
            spacing=5,
            controls=[step_top, step_label],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        row_controls.append(step_column)

        # Línea de conexión (no la dibujamos después del último o si es "cancelled")
        if i < num_statuses - 1 and status != "cancelled":
            line = ft.Container(
                width=line_width,
                height=2,
                bgcolor=line_color(status),
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

async def fetch_order_detail_async(page: ft.Page, order_id: str):
    """Obtiene detalle del pedido desde el backend y lo guarda en client_storage."""
    order_data = await get_order_detail(page, order_id)
    if order_data:
        await page.client_storage.set_async("creativeferrets.tienda.order_detail", order_data)
    else:
        await page.client_storage.set_async("creativeferrets.tienda.order_detail", {})

async def build_view_async(page: ft.Page, main_container: ft.Container, order_id: str):
    """
    Lee el detalle del pedido desde client_storage, construye la UI
    y la asigna a main_container.content.
    """
    # Cargamos la info del pedido en storage
    order_data = await page.client_storage.get_async("creativeferrets.tienda.order_detail") or {}
    if "order" not in order_data:
        # No se encontró el pedido
        error_container = ft.Container(
            padding=ft.padding.all(10),
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
            ),
        )
        main_container.content = error_container
        page.update()
        return

    # Extraemos el pedido
    order = order_data["order"]
    # Construimos la línea de tiempo
    timeline = build_order_timeline(order.get("status", "not_processed"))

    # Armamos shipping_info
    shipping_info = {
        "Nombre completo": order.get("full_name", ""),
        "Dirección 1": order.get("address_line_1", ""),
        "Dirección 2": order.get("address_line_2", ""),
        "Ciudad": order.get("city", ""),
        "Estado/Provincia": order.get("state_province_region", ""),
        "Código Postal": order.get("postal_zip_code", ""),
        "País": order.get("country_region", ""),
        "Teléfono": order.get("telephone_number", ""),
    }

    total_price = float(order.get("amount", 0.0))
    transaction_id = order.get("transaction_id", "")
    order_items = order.get("order_items", [])

    # Sección principal de datos de pedido
    order_details = ft.Column(
        spacing=15,
        controls=[
            ft.Text(f"Transacción: {transaction_id}", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Total: ${total_price:.2f}", size=18, color="green"),
            ft.Text("Información de Envío", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                padding=ft.padding.symmetric(vertical=5),
                content=ft.Column(
                    spacing=5,
                    controls=[
                        ft.Text(f"{key}: {value}", size=16)
                        for key, value in shipping_info.items()
                    ],
                ),
            ),
            ft.Divider(),
            ft.Text("Productos del Pedido", size=18, weight=ft.FontWeight.BOLD),
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
                                    ft.Text(item["name"], size=16, weight=ft.FontWeight.BOLD),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(f"Cantidad: {item['count']}", size=14),
                                            ft.Text(
                                                f"Total: ${(item['price'] * item['count']):.2f}",
                                                size=14,
                                                color="green",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        )
                        for item in order_items
                    ],
                ),
            ),
        ],
    )

    main_container.content = ft.Container(
        padding=ft.padding.all(10),
        expand=True,
        content=ft.Column(
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Detalle del Pedido", size=24, weight=ft.FontWeight.BOLD),
                timeline,
                ft.Divider(),
                order_details,
            ],
        ),
    )
    page.update()

async def init_view_async(page: ft.Page, main_container: ft.Container, order_id: str):
    """Carga detalle del pedido y construye la vista."""
    await fetch_order_detail_async(page, order_id)
    await build_view_async(page, main_container, order_id)

def ViewOrderDetail(page: ft.Page, order_id: str):
    page.controls.clear()
    navbar, _ = create_navbar_product(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()

    main_container = ft.Container(expand=True)

    # Función sincrónica para disparar la inicialización
    def init_view():
        page.run_task(init_view_async, page, main_container, order_id)

    init_view()

    return main_container
