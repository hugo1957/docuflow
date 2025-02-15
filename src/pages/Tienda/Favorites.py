import flet as ft
import asyncio
from pages.utils.navigation import create_navbar_product, create_footer
from pages.endpoints.Cart import add_item
from pages.endpoints.Wishlist import get_wishlist_items, remove_wishlist_item
from pages.endpoints.User import validate_user
API_URL = "http://localhost:8000"

def ViewFavorites(page: ft.Page):
    # 1) LIMPIA LA PANTALLA Y ASIGNA BARRAS DE NAVEGACIÓN
    page.controls.clear()
    navbar, update_cart_count = create_navbar_product(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()

    # Contenedor principal donde mostraremos los productos favoritos
    favorite_items_container = ft.Column(spacing=20)

    # Mensaje cuando no hay favoritos
    no_favorites_message = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
            ft.Image(src="logo.png", width=150, height=150),
            ft.Text(
                "No tienes productos favoritos.",
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "Agrega productos a tus favoritos desde nuestra tienda.",
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

    # 2) DECLARAMOS FUNCIONES ASÍNCRONAS PARA OPERACIONES
    async def update_favorites_display_async():
        """
        Carga la lista de favoritos (wishlist) desde el backend
        y refresca la UI, sin bloquear la interfaz.
        """
        # Limpiamos el contenedor antes de mostrar los resultados
        favorite_items_container.controls.clear()
        is_valid = await validate_user(page)
        if not is_valid:
            return  # Redirección ya realizada en validate_user
        # get_wishlist_items(...) es asíncrono; lo invocamos con await
        try:
            data = await get_wishlist_items(page)
        except Exception:
            data = None

        if not data or "wishlist" not in data or len(data["wishlist"]) == 0:
            # Sin favoritos
            favorite_items_container.controls.append(no_favorites_message)
            update_cart_count()
            page.update()
            return

        # Título de la lista de favoritos
        favorite_items_container.controls.append(
            ft.Text("Lista de Favoritos", size=22, weight=ft.FontWeight.BOLD)
        )

        for item in data["wishlist"]:
            product = item["product"]
            product_id_ = product["id"]
            product_name = product["name"]
            product_price = float(product["price"])
            product_photo = product.get("photo", "logo.png")

            card = ft.Container(
                padding=ft.padding.all(10),
                alignment=ft.alignment.center,
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
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Image(
                                    src=f"{API_URL}{product_photo}",
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
                                                    icon=ft.Icons.SHOPPING_CART,
                                                    icon_color=ft.Colors.GREEN,
                                                    tooltip="Agregar al carrito",
                                                    on_click=lambda e, pid=product_id_: add_to_cart_from_favorites(pid),
                                                ),
                                                ft.IconButton(
                                                    icon=ft.Icons.DELETE_OUTLINE,
                                                    icon_color=ft.Colors.RED,
                                                    tooltip="Eliminar de favoritos",
                                                    on_click=lambda e, pid=product_id_: remove_from_favorites(pid),
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Cantidad (1) :", size=14),
                                ft.Text(f"${product_price:.2f}", size=14),
                            ],
                        ),
                    ],
                ),
            )
            favorite_items_container.controls.append(card)

        page.update()

    async def add_to_cart_from_favorites_async(product_id: int):
        """
        Agrega el producto al carrito (POST /cart/add-item) 
        y luego lo elimina de la wishlist (remove_wishlist_item).
        """
        # 1) Intentar agregar al carrito
        try:
            result = await add_item(page, product_id)
        except Exception:
            result = None

        if result is not None:
            # 2) Si se agregó correctamente, lo eliminamos de favoritos
            try:
                await remove_wishlist_item(page, product_id)
            except Exception:
                pass

            sb = ft.SnackBar(
                content=ft.Text(
                    "Agregado al carrito y removido de favoritos.",
                    color="white"
                ),
                bgcolor="green",
            )
            page.overlay.append(sb)
            sb.open = True
            # 3) Volver a cargar la lista de favoritos
            update_favorites_display()

        else:
            sb = ft.SnackBar(
                content=ft.Text("No se pudo agregar al carrito.", color="white"),
                bgcolor="red",
            )
            page.overlay.append(sb)
            sb.open = True

        # Actualizar contador del carrito
        update_cart_count()
        page.update()

    async def remove_from_favorites_async(product_id: int):
        """
        Elimina el producto de la wishlist.
        """
        try:
            result = await remove_wishlist_item(page, product_id)
        except Exception:
            result = None

        if result is not None:
            sb = ft.SnackBar(
                content=ft.Text(
                    "Producto eliminado de favoritos.", color="white"),
                bgcolor="green",
            )
            page.overlay.append(sb)
            sb.open = True
            # Refrescamos la lista
            update_favorites_display()
        else:
            sb = ft.SnackBar(
                content=ft.Text("No se pudo remover de favoritos.", color="white"),
                bgcolor="red",
            )
            page.overlay.append(sb)
            sb.open = True

        page.update()

    # 3) WRAPPERS SINCRÓNICOS QUE EJECUTAN LAS FUNCIONES ASÍNCRONAS EN SEGUNDO PLANO
    def update_favorites_display():
        # En lugar de usar asyncio.run(...), llamamos page.run_task(...)
        page.run_task(update_favorites_display_async)

    def add_to_cart_from_favorites(product_id):
        page.run_task(
            add_to_cart_from_favorites_async,
            product_id
        )

    def remove_from_favorites(product_id):
        page.run_task(
            remove_from_favorites_async,
            product_id
        )

    # 4) CONTENEDOR PRINCIPAL DE LA PÁGINA
    main_container = ft.Container(
        padding=ft.padding.all(10),
        expand=True,
        alignment=ft.alignment.top_center,
        content=ft.Column(
            expand=True,
            controls=[favorite_items_container],
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )

    # Llamamos de inmediato a la versión "wrapper" que lanza la tarea
    update_favorites_display()

    # Retornamos la UI (se muestra instantáneamente, mientras la carga ocurre en segundo plano)
    return main_container
