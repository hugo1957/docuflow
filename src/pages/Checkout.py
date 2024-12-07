import uuid
import flet as ft
from pages.utils.navigation import create_footer, create_navbar_product


def ViewCheckout(page):
    page.controls.clear()
    navbar, update_cart_count = create_navbar_product(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()

    cart_items_container = ft.Column(spacing=10)
    total_price_text = ft.Text("", size=20, weight=ft.FontWeight.BOLD)
    shipping_info_fields = create_shipping_info_fields()

    coupon_field = ft.TextField(
        label="Cupón de descuento",
        hint_text="Ingresa tu código de cupón",
        border_radius=ft.border_radius.all(8),
        expand=True,
    )
    apply_coupon_button = ft.ElevatedButton(
        text="Aplicar",
        on_click=lambda e: apply_coupon(e, coupon_field.value),
        bgcolor="#e5bc16",
        color="white",
    )

    pay_button = ft.ElevatedButton(
        text="Completar pago",
        on_click=lambda e: process_payment(e),
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
                        ft.Image(src="icon.png", width=200, height=200),
                        ft.Text("Tu carrito está vacío", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Text("¡Visita nuestra tienda y agrega productos a tu carrito!", size=16, text_align=ft.TextAlign.CENTER),
                        ft.ElevatedButton(text="Ir a la tienda", on_click=lambda e: page.go("/"), bgcolor="#e5bc16", color="white", width=150),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
            )
            cart_items_container.controls.append(empty_cart_view)
            total_price_text.value = ""
            pay_button.visible = False
            page.update()
            return
        pay_button.visible = True
        for item in cart:
            if "quantity" not in item:
                item["quantity"] = 1
            cart_item = ft.Container(
                padding=ft.padding.all(10),
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Image(
                            src=item["image"],
                            width=100,
                            height=100,
                            border_radius=ft.border_radius.all(10),
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        ft.Text(item["name"], size=16, weight=ft.FontWeight.BOLD, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Precio unitario: ${item['price']}", size=14, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Cantidad: {item['quantity']}", size=14, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Total: ${float(item['price']) * item['quantity']:.2f}", size=16, weight=ft.FontWeight.BOLD),
                    ],
                ),
            )
            cart_items_container.controls.append(cart_item)
        total_price = sum(float(item["price"]) * item["quantity"] for item in cart)
        total_price_text.value = f"Total: ${total_price:.2f}"
        page.update()

    def validate_shipping_info(fields):
        for field in fields.controls:
            if not field.value.strip():
                return f"El campo {field.label} es obligatorio."
        return None

    def apply_coupon(e, coupon_code):
        if coupon_code.strip() == "DESCUENTO10":
            page.snack_bar = ft.SnackBar(content=ft.Text("¡Cupón aplicado! 10% de descuento."), bgcolor=ft.colors.GREEN)
            page.snack_bar.open = True
            cart = page.session.get("cart") or []
            for item in cart:
                item["price"] = float(item["price"]) * 0.9
            page.session.set("cart", cart)
            update_cart_display()
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Cupón inválido."), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
        page.update()

    def process_payment(e):
        error = validate_shipping_info(shipping_info_fields)
        if error:
            page.snack_bar = ft.SnackBar(content=ft.Text(error), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()
            return

        order = create_order(page)
        if order:
            page.session.set("cart", [])
            update_cart_count()
            page.go("/payment-success")
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Error al registrar la orden."), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()

    def create_order(page):
        cart = page.session.get("cart") or []
        shipping_info = {field.label: field.value for field in shipping_info_fields.controls}
        order_id = str(uuid.uuid4())
        order = {
            "id": order_id,
            "cart": cart,
            "shipping_info": shipping_info,
            "total_price": total_price_text.value,
        }
        orders = page.session.get("orders") or []
        orders.append(order)
        page.session.set("orders", orders)
        print("Orden registrada:", order)
        return order

    update_cart_display()
    update_cart_count()

    main_container = ft.Container(
        padding=ft.padding.all(10),
        content=ft.Column(
            controls=[
                ft.Text("Checkout", size=24, weight=ft.FontWeight.BOLD),
                cart_items_container,
                ft.Divider(),
                ft.Column(
                    controls=[
                        ft.Text("Información de Envío", size=20, weight=ft.FontWeight.BOLD),
                        shipping_info_fields,
                    ],
                    spacing=10,
                ),
                ft.Row(controls=[coupon_field, apply_coupon_button], spacing=10),
                ft.ResponsiveRow(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[total_price_text, pay_button]),
                ft.Container(height=10),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
    )

    return main_container

def create_shipping_info_fields():
    fields = [
        ft.TextField(label="Nombre Completo", border_radius=ft.border_radius.all(8), expand=True),
        ft.TextField(label="Dirección", border_radius=ft.border_radius.all(8), expand=True),
        ft.TextField(label="Ciudad", border_radius=ft.border_radius.all(8), expand=True),
        ft.TextField(label="Estado/Provincia", border_radius=ft.border_radius.all(8), expand=True),
        ft.TextField(label="Código Postal", border_radius=ft.border_radius.all(8), expand=True),
        ft.TextField(label="País", border_radius=ft.border_radius.all(8), expand=True),
    ]
    return ft.Column(controls=fields, spacing=10, expand=True)
