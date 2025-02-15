import flet as ft
from pages.utils.navigation import create_footer, create_navbar_product
from pages.endpoints.Orders import list_orders

async def load_orders_async(page: ft.Page):
    """Llama al endpoint list_orders y guarda el resultado en client_storage."""
    orders_data = await list_orders(page)  # list_orders es asíncrona
    if orders_data:
        await page.client_storage.set_async("creativeferrets.tienda.orders", orders_data)
    else:
        await page.client_storage.set_async("creativeferrets.tienda.orders", {"orders": []})

async def build_view_async(page: ft.Page, main_container: ft.Container):
    """Lee los pedidos desde client_storage (async) y construye la UI."""
    orders_data = await page.client_storage.get_async("creativeferrets.tienda.orders") or {"orders": []}
    orders = orders_data.get("orders", [])

    # Contenedor de encabezado con logo y título
    header_container = ft.Container(
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(vertical=10),
        content=ft.Column(
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(src="logo.png", width=80, height=80),
                ft.Text("Tus Pedidos", size=24, weight=ft.FontWeight.BOLD),
            ],
        ),
    )

    # Construimos la lista de pedidos o mensaje de "no hay pedidos"
    order_items = []
    if not orders:
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
        for order in orders:
            order_item = ft.Container(
                padding=ft.padding.all(10),
                margin=ft.margin.symmetric(vertical=5),
                border_radius=ft.border_radius.all(8),
                shadow=ft.BoxShadow(blur_radius=2, spread_radius=1),
                bgcolor="#FFFFFF",
                content=ft.Column(
                    spacing=10,
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            f"Número de Pedido: {order['transaction_id']}",
                            size=16,
                            max_lines=1,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            f"Estado: {order['status']}",
                            size=14,
                            color="blue",
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    f"Total: ${order['amount']}",
                                    size=14,
                                    color="green",
                                ),
                                ft.ElevatedButton(
                                    text="Ver Detalle",
                                    bgcolor="#FF5700",
                                    color="white",
                                    on_click=lambda e, order_id=order["transaction_id"]: go_to_order_detail(page, order_id),
                                ),
                            ],
                        ),
                    ],
                ),
            )
            order_items.append(order_item)

    # Columna con todos los pedidos
    order_items_column = ft.Column(
        controls=order_items,
        spacing=10,
    )

    # Armamos el contenido de main_container
    main_container.content = ft.Container(
        content=ft.Column(
            spacing=10,
            expand=True,
            controls=[
                header_container,
                ft.Divider(),
                order_items_column,
            ],
        ),
        padding=ft.padding.all(10),
    )

    page.update()

def go_to_order_detail(page: ft.Page, order_id: str):
    """Navega a la vista de detalle de un pedido."""
    page.go(f"/order-detail/{order_id}")

async def init_view_async(page: ft.Page, main_container: ft.Container):
    """
    Carga la lista de pedidos (endpoints) y luego construye la UI
    sin bloquear la interfaz de Flet.
    """
    # 1) Llamamos al endpoint y guardamos en client_storage
    await load_orders_async(page)
    # 2) Construimos la vista leyendo lo que guardamos
    await build_view_async(page, main_container)

def ViewOrders(page: ft.Page):
    # Limpiamos la vista y configuramos la navegación
    page.controls.clear()
    navbar, _ = create_navbar_product(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()

    # Contenedor principal
    main_container = ft.Container(expand=True)

    # Llamamos a la inicialización asíncrona en segundo plano
    def init_view():
        page.run_task(init_view_async, page, main_container)

    init_view()

    return main_container
