import flet as ft
from pages.utils.navigation import create_footer, create_navbar_product


def ViewCart(page):
    page.controls.clear()
    navbar, update_cart_count = create_navbar_product(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()
    
    cart_items_container = ft.Column(spacing=10)
    total_price_text = ft.Text("", size=20, weight=ft.FontWeight.BOLD)
    checkout_button = ft.ElevatedButton(
        text="Proceder al pago",
        on_click=lambda e: page.go("/checkout"),
        bgcolor="#e5bc16",
        color="white",
        width=200,
    )

    def update_cart_display():
        cart_items_container.controls.clear()
        cart = page.session.get("cart") or []
        if not cart:
            empty_cart_view = ft.Container(
                padding=ft.padding.all(10),
                content=ft.Column(
                    controls=[
                        ft.Image(
                            src="icon.png",
                            width=200,
                            height=200,
                        ),
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
                            on_click=lambda e: page.go("/"),
                            bgcolor="#e5bc16",
                            color="white",
                            width=150,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                )
            )
            cart_items_container.controls.append(empty_cart_view)
            total_price_text.value = ""
            checkout_button.visible = False
            page.update()
            return
        checkout_button.visible = True
        for idx, item in enumerate(cart):
            if "quantity" not in item:
                item["quantity"] = 1
            cart_item = ft.Container(
                padding=ft.padding.all(10),
                content=ft.Column(
                    expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
                    controls=[
                        ft.Image(
                            src=item["image"],
                            width=page.window.width,
                            height=100,
                            border_radius=ft.border_radius.all(10),
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    item["name"],
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    max_lines=2,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Text(f"Precio: ${item['price']}", size=14),
                            ],
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                                    on_click=lambda e, idx=idx: decrease_quantity(e, idx),
                                ),
                                ft.Text(
                                    f"{item['quantity']}",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                    on_click=lambda e, idx=idx: increase_quantity(e, idx),
                                ),
                            ],
                        ),
                        ft.IconButton(
                            
                            icon=ft.Icons.DELETE_OUTLINE,
                            on_click=lambda e, idx=idx: remove_from_cart(e, idx),
                            icon_color=ft.Colors.RED,
                        ),
                    ],
                ),
            )
            cart_items_container.controls.append(cart_item)
        total_price = sum(float(item["price"]) * item["quantity"] for item in cart)
        total_price_text.value = f"Total: ${total_price:.2f}"
        page.update()


    def remove_from_cart(e, idx):
        cart = page.session.get("cart") or []
        del cart[idx]
        page.session.set("cart", cart)
        update_cart_count()
        update_cart_display()

    def increase_quantity(e, idx):
        cart = page.session.get("cart") or []
        cart[idx]["quantity"] += 1
        page.session.set("cart", cart)
        update_cart_count()
        update_cart_display()

    def decrease_quantity(e, idx):
        cart = page.session.get("cart") or []
        if cart[idx]["quantity"] > 1:
            cart[idx]["quantity"] -= 1
        else:
            del cart[idx]
        page.session.set("cart", cart)
        update_cart_count()
        update_cart_display()

    update_cart_display()
    update_cart_count()

    main_container = ft.Container(
        padding=ft.padding.all(10),
        expand=True,
        content=ft.Column(
            controls=[
                cart_items_container,
                ft.Divider(),
                ft.ResponsiveRow(
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[total_price_text, checkout_button],
                ),
            ],
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )

    return main_container
