import flet as ft
import asyncio
from pages.utils.navigation import create_footer, create_navbar_product
from pages.endpoints.Cart import add_item
from pages.endpoints.Wishlist import (
    add_wishlist_item,
    remove_wishlist_item,
    get_wishlist_items
)
from pages.endpoints.Tienda import get_product_detail

API_URL = "http://localhost:8000"

def ViewProductDetail(page, url):
    # Extrae el ID del producto de la URL
    product_id = url.replace("/product-detail/", "")

    # Limpiar la página y asignar barra de navegación
    page.controls.clear()
    navbar, update_cart_count = create_navbar_product(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)

    # ----------------------------------
    # CONTROLES DE LA UI (labels, etc.)
    # ----------------------------------
    product_name_text = ft.Text(
        "Cargando producto...", size=24, weight=ft.FontWeight.BOLD
    )
    product_image_control = ft.Image(
        src="https://via.placeholder.com/400x200", fit=ft.ImageFit.COVER
    )
    product_price_text = ft.Text("Precio: $ --", size=18, color="green")
    product_status_text = ft.Text(
        "Cargando disponibilidad...", size=14, color="black"
    )
    product_description_text = ft.Text("Cargando descripción...", size=14)

    # Botón de wishlist (corazón)
    wishlist_button = ft.Container(
        width=40,
        height=40,
        border_radius=ft.border_radius.all(5),
        border=ft.border.all(color="#E0E0E0"),  # línea gris suave
        alignment=ft.alignment.center,
        content=ft.Icon(name=ft.Icons.FAVORITE_BORDER, color="grey"),
        ink=True,
        on_click=None,  # Se asignará dinámicamente
    )

    # Botón de “Agregar al Carrito”
    add_to_cart_button = ft.Container(
        content=ft.Text("Agregar al Carrito", color="white", size=14),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        border_radius=ft.border_radius.all(5),
        bgcolor="#4CAF50",  # verde
        alignment=ft.alignment.center,
        width=page.width - 70,  # Ajusta ancho si lo deseas
        on_click=None,          # Se asignará dinámicamente
        ink=True,
    )

    # Contenedor de la imagen
    product_image_container = ft.Container(
        content=product_image_control,
        width=page.width,
        height=200,
        border_radius=ft.border_radius.all(15),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    # Info principal del producto
    product_info = ft.Column(
        spacing=5,
        controls=[
            product_name_text,
            product_status_text
        ],
    )

    # Descripción
    product_description_section = ft.Column(
        spacing=5,
        controls=[
            ft.Text("Descripción", size=16, weight=ft.FontWeight.BOLD),
            product_description_text,
        ],
    )

    # Fila con wishlist y “Agregar al carrito”
    product_price_and_button = ft.Row(
        spacing=5,
        controls=[
            wishlist_button,
            add_to_cart_button,
        ],
    )

    # Contenedor principal
    product_detail_container = ft.Container(
        padding=ft.padding.all(10),
        alignment=ft.alignment.center,
        expand=True,
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                product_image_container,
                product_info,
                ft.Divider(),
                product_description_section,
                ft.Divider(),
                product_price_text,
                product_price_and_button,
                ft.Container(height=10),
            ],
        ),
    )

    # -------------------------------------------------------------------
    # ASYNC FUNCTIONS (carga de detalles, wishlist, añadir/quitar, etc.)
    # -------------------------------------------------------------------

    async def load_product_detail_async():
        """Obtiene detalle del producto del backend y actualiza la UI."""
        try:
            product_data = await get_product_detail(page, product_id)
        except Exception:
            product_data = None

        if product_data and "product" in product_data:
            data = product_data["product"]
            name = data.get("name", "Sin nombre")
            price = float(data.get("price", 0.0))
            description = data.get("description", "Sin descripción")
            image_url = data.get("photo", "https://via.placeholder.com/400x200")
            quantity = data.get("quantity", 0)

            product_name_text.value = name
            product_image_control.src = f"{API_URL}{image_url}"
            product_price_text.value = f"Precio: ${price:.2f}"
            product_description_text.value = description

            if quantity > 0:
                product_status_text.value = f"Disponible - {quantity} en inventario"
                product_status_text.color = "green"
                # Activamos el botón “Agregar al Carrito”
                add_to_cart_button.on_click = add_to_cart_handler
            else:
                product_status_text.value = "No Disponible - Sin inventario"
                product_status_text.color = "red"
                add_to_cart_button.on_click = None  # Desactivado
        else:
            product_name_text.value = "Producto no encontrado"
            product_description_text.value = "Lo sentimos, no pudimos cargar este producto."

        page.update()

    async def refresh_wishlist_status_async():
        """
        Verifica si este producto está en la wishlist y actualiza ícono y on_click.
        """
        data = None
        try:
            data = await get_wishlist_items(page)
        except Exception:
            pass

        in_wishlist = False
        if data and "wishlist" in data:
            # Determina si este producto ya está en la wishlist
            in_wishlist = any(
                str(item["product"]["id"]) == product_id
                for item in data["wishlist"]
            )

        if in_wishlist:
            wishlist_button.content = ft.Icon(ft.Icons.FAVORITE, color="red")
            wishlist_button.on_click = remove_from_wishlist_handler
        else:
            wishlist_button.content = ft.Icon(ft.Icons.FAVORITE_BORDER, color="grey")
            wishlist_button.on_click = add_to_wishlist_handler

        page.update()

    async def add_to_wishlist_async():
        """Agrega el producto a la lista de deseos."""
        res = None
        try:
            res = await add_wishlist_item(page, product_id)
        except Exception:
            pass

        if res is not None:
            sb = ft.SnackBar(
                content=ft.Text("Producto agregado a la lista de deseos.", color="white"),
                bgcolor="green",
            )
        else:
            sb = ft.SnackBar(
                content=ft.Text("No se pudo agregar a la lista de deseos.", color="white"),
                bgcolor="red",
            )
        page.overlay.append(sb)
        sb.open = True
        page.update()

        # Actualizar el ícono wishlist
        await refresh_wishlist_status_async()

    async def remove_from_wishlist_async():
        """Remueve el producto de la lista de deseos."""
        res = None
        try:
            res = await remove_wishlist_item(page, product_id)
        except Exception:
            pass

        if res is not None:
            sb = ft.SnackBar(
                content=ft.Text("Producto removido de la lista de deseos.", color="white"),
                bgcolor="green",
            )
        else:
            sb = ft.SnackBar(
                content=ft.Text("No se pudo remover de la lista de deseos.", color="white"),
                bgcolor="red",
            )
        page.overlay.append(sb)
        sb.open = True
        page.update()

        # Actualizar ícono wishlist
        await refresh_wishlist_status_async()

    async def add_to_cart_async():
        """Agrega el producto al carrito."""
        res = None
        try:
            res = await add_item(page, product_id)
        except Exception:
            pass

        if res is not None:
            if res.get("status") == 409:
                sb = ft.SnackBar(
                    content=ft.Text("El producto ya está en el carrito.", color="white"),
                    bgcolor="orange",
                )
            else:
                sb = ft.SnackBar(
                    content=ft.Text("Producto agregado al carrito.", color="white"),
                    bgcolor="green",
                )
                # Llamar a la función devuelta por create_navbar_product
                update_cart_count()
        else:
            sb = ft.SnackBar(
                content=ft.Text("No se pudo agregar al carrito.", color="white"),
                bgcolor="red",
            )
        page.overlay.append(sb)
        sb.open = True
        page.update()

    # ---------------------------------------------------------------
    # Wrappers "sincrónicos" que se asocian con on_click
    # y llaman a las corrutinas en segundo plano.
    # ---------------------------------------------------------------
    def load_product_detail():
        page.run_task(load_product_detail_async)

    def refresh_wishlist_status():
        page.run_task(refresh_wishlist_status_async)

    def add_to_wishlist_handler(_):
        page.run_task(add_to_wishlist_async)

    def remove_from_wishlist_handler(_):
        page.run_task(remove_from_wishlist_async)

    def add_to_cart_handler(_):
        page.run_task(add_to_cart_async)

    # ---------------------------------------------------------------
    # LÓGICA INICIAL: Cargar detalle, wishlist y actualizar carrito
    # ---------------------------------------------------------------
    load_product_detail()         # Carga la info en 2do plano
    refresh_wishlist_status()     # Actualiza el ícono de wishlist
    update_cart_count()           # Actualiza contador del carrito

    # Retornamos el contenedor principal con todo
    return product_detail_container
