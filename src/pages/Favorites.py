import flet as ft
from pages.utils.navigation import create_navbar_product, create_footer

def ViewFavorites(page):
    favorites = page.session.get("favorites") or []
    cart = page.session.get("cart") or []
    page.controls.clear()
    navbar, update_cart_count = create_navbar_product(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()
    
    favorite_items_container = ft.Column(spacing=10)
    no_favorites_message = ft.Container(
        alignment=ft.alignment.center,
        padding=ft.padding.all(10),
        content=ft.Column(
            controls=[
                ft.Image(
                    src="icon.png",
                    width=200,
                    height=200,
                ),
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
                    on_click=lambda e: page.go("/"),
                    bgcolor="#e5bc16",
                    color="white",
                    width=150,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
    )

    def update_favorites_display():
        favorite_items_container.controls.clear()
        if not favorites:
            favorite_items_container.controls.append(no_favorites_message)
            page.update()
            return

        for product in favorites:
            favorite_item = ft.Container(
                padding=ft.padding.all(10),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Image(
                            src=product["image"],
                            width=80,
                            height=80,
                            fit=ft.ImageFit.COVER,
                            border_radius=ft.border_radius.all(8),
                        ),
                        ft.Column(
                            expand=True,
                            spacing=5,
                            controls=[
                                ft.Text(
                                    product["name"],
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    max_lines=2,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Text(f"Precio: ${product['price']}", size=14),
                            ],
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Agregar al carrito",
                                    bgcolor="#e5bc16",
                                    color="white",
                                    on_click=lambda e, product=product: add_to_cart_from_favorites(product),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    on_click=lambda e, product=product: remove_from_favorites(product),
                                    icon_color=ft.Colors.RED,
                                ),
                            ],
                        ),
                    ],
                ),
            )
            favorite_items_container.controls.append(favorite_item)
        page.update()

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

    update_favorites_display()

    main_container = ft.Container(
        padding=ft.padding.all(10),
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                favorite_items_container,
            ],
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )
    return main_container
