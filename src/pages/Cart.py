import flet as ft
from pages.utils.navigation import create_footer, create_navbar_product

def ViewCart(page):
    page.controls.clear()
    page.appbar = create_navbar_product(page)
    page.navigation_bar = create_footer(page)

    cart = page.session.get("cart")
    if cart is None:
        cart = []
        
    if not cart:
        empty_cart_message = ft.Text("Tu carrito está vacío.", size=20)
        page.add(empty_cart_message)
        page.update()
        return
    def remove_from_cart(e, item):
        cart = page.session.get("cart")
        if cart is None:
            cart = []
        cart.remove(item)
        page.session.set("cart", cart)
        page.appbar = create_navbar_product(page)
        ViewCart(page)

    cart_items = []
    for item in cart:
        cart_item = ft.Row(
            controls=[
                ft.Image(src=item["image"], width=50, height=50),
                ft.Column(
                    controls=[
                        ft.Text(item["name"], size=16),
                        ft.Text(f"Precio: ${item['price']}", size=14),
                    ]
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE,
                    on_click=lambda e, item=item: remove_from_cart(e, item),
                ),
            ]
        )
        cart_items.append(cart_item)

    # Calcular el precio total
    total_price = sum(float(item["price"]) for item in cart)
    total_price_text = ft.Text(f"Total: ${total_price}", size=18, weight=ft.FontWeight.BOLD)

    # Botón para proceder al pago
    checkout_button = ft.ElevatedButton(
        text="Proceder al pago",
        on_click=lambda e: print("Procediendo al pago..."),
        bgcolor="#e5bc16",
        color="white",
    )

    container = (
        ft.Column(
            controls=cart_items + [ft.Divider(), total_price_text, checkout_button],
            scroll=ft.ScrollMode.AUTO,
        )
    )
    return container

