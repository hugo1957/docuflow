import flet as ft
from pages.utils.navigation import create_navbar_product, create_footer


def ViewFavorites(page):
    page.controls.clear()
    navbar, update_cart_count = create_navbar_product(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()

    favorites = page.session.get("favorites") or []
    cart = page.session.get("cart") or []

    # Contenedor donde se mostrarán todos los items favoritos
    favorite_items_container = ft.Column(spacing=20)

    # Mensaje a mostrar cuando no haya favoritos
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

    def add_to_cart_from_favorites(product):
        if product not in cart:
            cart.append(product)
            page.session.set("cart", cart)
        if product in favorites:
            favorites.remove(product)
            page.session.set("favorites", favorites)
        update_cart_count()
        update_favorites_display()

    def remove_from_favorites(product):
        if product in favorites:
            favorites.remove(product)
            page.session.set("favorites", favorites)
        update_favorites_display()

    def update_favorites_display():
        favorite_items_container.controls.clear()

        # ¿No hay favoritos? Agregamos el mensaje vacío
        if not favorites:
            favorite_items_container.controls.append(no_favorites_message)
        else:
            # Título general (Shopping List)
            favorite_items_container.controls.append(
                ft.Text("Lista de Favoritos", size=22,
                        weight=ft.FontWeight.BOLD)
            )

            # Construimos la "tarjeta" para cada producto
            for product in favorites:
                product_image = product["image"]
                product_name = product["name"]
                product_price = product["price"]

                # Tarjeta principal
                favorite_item = ft.Container(
                    padding=ft.padding.all(10),
                    alignment=ft.alignment.center,
                    margin=ft.margin.symmetric(vertical=5),
                    border_radius=ft.border_radius.all(8),
                    shadow=ft.BoxShadow(
                        blur_radius=2,
                        spread_radius=1,

                    ),
                    bgcolor="#FFFFFF",
                    content=ft.Column(
                        spacing=10,
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            # Fila superior: Imagen + datos + botones
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    # Imagen
                                    ft.Image(
                                        src=product_image,
                                        width=80,
                                        height=80,
                                        fit=ft.ImageFit.COVER,
                                        border_radius=ft.border_radius.all(8),
                                    ),
                                    # Nombre y precio
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
                                                f"Precio: ${product_price}",
                                                size=14,
                                            ),
                                            ft.Row(
                                                expand=True,
                                                controls=[
                                                    ft.IconButton(
                                                        icon=ft.Icons.SHOPPING_CART,
                                                        on_click=lambda e, p=product: add_to_cart_from_favorites(
                                                            p),
                                                        icon_color=ft.Colors.GREEN,
                                                    ),
                                                    ft.IconButton(
                                                        icon=ft.Icons.DELETE_OUTLINE,
                                                        on_click=lambda e, p=product: remove_from_favorites(
                                                            p),
                                                        icon_color=ft.Colors.RED,
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    # Botones

                                ],
                            ),
                            # Fila inferior: "Total Order (1) : $xx"
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Total Order (1) :", size=14),
                                    ft.Text(f"${product_price}", size=14),
                                ],
                            ),
                        ],
                    ),
                )
                # Agregamos la tarjeta al contenedor de favoritos
                favorite_items_container.controls.append(favorite_item)

        page.update()

    # Contenedor principal que se retorna
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

    # Construimos la vista al cargar
    update_favorites_display()

    return main_container