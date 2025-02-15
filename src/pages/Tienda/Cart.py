import flet as ft
import asyncio

from pages.utils.navigation import create_footer, create_navbar_product
from pages.endpoints.Cart import (
    get_items,
    get_total,
    remove_item,
    update_item,
)
from pages.endpoints.User import validate_user
API_URL = "http://localhost:8000"

def ViewCart(page):
    # Limpia la UI y asigna la barra de navegación
    page.controls.clear()
    navbar, update_cart_count = create_navbar_product(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()

    # Contenedores principales
    main_container = ft.Container(expand=True, content=None)
    cart_items_container = ft.Column(spacing=20, expand=True)
    total_price_text = ft.Text("", size=20, weight=ft.FontWeight.BOLD)
    checkout_button = ft.Container(
      content=ft.Text("Verificar", color="white", size=14),
      padding=ft.padding.symmetric(horizontal=20, vertical=10),
      border_radius=ft.border_radius.all(5),
      bgcolor="#FF5700",  # naranja
      alignment=ft.alignment.center,
      on_click=lambda e: page.go("/checkout"),
      ink=True,
    )

    # -------------------------------------------------------------------
    # FUNCIONES ASÍNCRONAS (llamadas con page.run_task(...) desde wrappers)
    # -------------------------------------------------------------------

    async def update_cart_display_async():
        """Carga todos los productos del carrito y actualiza la UI, sin bloquear."""
        cart_items_container.controls.clear()
        is_valid = await validate_user(page)
        
        if not is_valid:
            return  # Redirección ya realizada en validate_user
        # # 1) Obtener items del carrito
        try:
            items = await get_items(page)
        except Exception:
            items = None

        if not items or "cart" not in items or len(items["cart"]) == 0:
            # Carrito vacío
            empty_cart_view = ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Image(src="logo.png", width=150, height=150),
                    ft.Text(
                        "Tu carrito está vacío",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "¡Visita nuestra tienda y agrega productos a tu carrito!",
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.ElevatedButton(
                        text="Ir a la tienda",
                        on_click=lambda e: page.go("/home"),
                        bgcolor="#FF5700",
                        color="white",
                        width=150,
                    ),
                ],
            )
            cart_items_container.controls.append(empty_cart_view)
            total_price_text.value = ""
            checkout_button.visible = False
            main_container.bgcolor = None
            page.update()
            return

        # Carrito con items
        main_container.bgcolor = ft.Colors.WHITE
        checkout_button.visible = True
        cart_items_container.controls.append(
            ft.Text("Lista del Carrito de Compra", size=22, weight=ft.FontWeight.BOLD)
        )

        # 2) Crear UI para cada item
        for item in items["cart"]:
            try:
                product = item["product"]
                product_id = product["id"]
                product_name = product["name"]
                product_price = float(product["price"])
                quantity = int(item["count"])
                product_image = product.get("photo", "logo.png")
                subtotal = product_price * quantity
            except (KeyError, TypeError) as e:
                print(f"Error al procesar el item: {e}")
                continue

            cart_item = ft.Container(
                padding=ft.padding.all(10),
                alignment=ft.alignment.center,
                margin=ft.margin.symmetric(vertical=5),
                border_radius=ft.border_radius.all(8),
                shadow=ft.BoxShadow(blur_radius=2, spread_radius=1),
                bgcolor="#FFFFFF",
                content=ft.Column(
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            spacing=10,
                            controls=[
                                ft.Image(
                                    src=f"{API_URL}{product_image}",
                                    width=80,
                                    height=80,
                                    fit=ft.ImageFit.COVER,
                                    border_radius=ft.border_radius.all(8),
                                ),
                                ft.Column(
                                    spacing=5,
                                    expand=True,
                                    controls=[
                                        ft.Text(
                                            product_name,
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            max_lines=2,
                                            overflow=ft.TextOverflow.ELLIPSIS,
                                        ),
                                        ft.Text(
                                            f"Precio: ${product_price:.2f}",
                                            size=14,
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.IconButton(
                                                    icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                                                    on_click=lambda e, pid=product_id, qty=quantity: decrease_quantity(pid, qty),
                                                ),
                                                ft.Text(
                                                    str(quantity),
                                                    size=16,
                                                    weight=ft.FontWeight.BOLD,
                                                    text_align=ft.TextAlign.CENTER,
                                                ),
                                                ft.IconButton(
                                                    icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                                    on_click=lambda e, pid=product_id, qty=quantity: increase_quantity(pid, qty),
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_color=ft.Colors.RED,
                                    on_click=lambda e, pid=product_id: remove_item_from_cart(pid),
                                ),
                            ],
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"Cantidad ({quantity}) :", size=14),
                                ft.Text(f"${subtotal:.2f}", size=14),
                            ],
                        ),
                    ],
                ),
            )
            cart_items_container.controls.append(cart_item)

        # 3) Obtener total
        total_data = None
        try:
            total_data = await get_total(page)
        except Exception:
            pass

        if total_data and "total_cost" in total_data:
            total_value = float(total_data["total_cost"])
            total_price_text.value = f"Total: ${total_value:.2f}"
        else:
            total_price_text.value = "Total: $0.00"

        page.update()

    async def remove_item_from_cart_async(product_id):
        """Elimina un producto del carrito y refresca la UI."""
        result = None
        try:
            result = await remove_item(page, product_id)
        except Exception:
            pass
        if result:
            # Refrescar la pantalla
            await update_cart_display_async()
            # SnackBar
            snack_bar = ft.SnackBar(
                content=ft.Text("Producto eliminado del carrito."),
                bgcolor=ft.Colors.ORANGE,
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
        # Actualizar contador
        update_cart_count()
        page.update()

    async def increase_quantity_async(product_id, current_qty):
        """Aumenta la cantidad en 1 y refresca la UI."""
        new_qty = current_qty + 1
        result = None
        try:
            result = await update_item(page, product_id, new_qty)
        except Exception:
            pass
        if result:
            await update_cart_display_async()
        update_cart_count()
        page.update()

    async def decrease_quantity_async(product_id, current_qty):
        """Disminuye la cantidad en 1 o elimina si queda en 0, y refresca la UI."""
        new_qty = current_qty - 1
        result = None
        try:
            if new_qty >= 1:
                result = await update_item(page, product_id, new_qty)
            else:
                result = await remove_item(page, product_id)
        except Exception:
            pass
        if result:
            await update_cart_display_async()
        update_cart_count()
        page.update()

    # ----------------------------------------------------------------------
    # WRAPPERS SINCRÓNICOS que se asocian a botones y llaman a corrutinas:
    # ----------------------------------------------------------------------
    def update_cart_display():
        page.run_task(update_cart_display_async)

    def remove_item_from_cart(product_id):
        page.run_task(remove_item_from_cart_async, product_id)

    def increase_quantity(product_id, current_qty):
        page.run_task(increase_quantity_async, product_id, current_qty)

    def decrease_quantity(product_id, current_qty):
        page.run_task(decrease_quantity_async, product_id, current_qty)

    # ----------------------------------------------------------------------
    # ESTRUCTURA PRINCIPAL DE LA VISTA
    # ----------------------------------------------------------------------
    main_container.content = ft.Container(
        padding=ft.padding.all(10),
        content=ft.Column(
            controls=[
                cart_items_container,
                total_price_text,
                checkout_button
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
        ),
    )

    # Al cargar la vista, refrescamos el carrito y el contador
    update_cart_display()
    update_cart_count()

    return main_container
