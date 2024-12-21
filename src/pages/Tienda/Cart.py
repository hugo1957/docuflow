
import flet as ft
from pages.utils.navigation import create_footer, create_navbar_product

def ViewCart(page):
    page.controls.clear()
    navbar, update_cart_count = create_navbar_product(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()
    
    # Contenedor principal
    main_container = ft.Container(
        expand=True,
        content=None  # Se definirá al final (cart layout)
    )

    # Contenedor donde se listarán los productos del carrito
    cart_items_container = ft.Column(spacing=20)  # Espacio entre tarjetas

    # Texto con el precio total (de todo el carrito)
    total_price_text = ft.Text("", size=20, weight=ft.FontWeight.BOLD)

    # Botón para checkout
    checkout_button = ft.ElevatedButton(
        text="Verificar",
        on_click=lambda e: page.go("/checkout"),
        bgcolor="#FF5700",
        color="white",
        width=150,
    )

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

    def update_cart_display():
        """Refresca la vista del carrito y ajusta la presentación."""
        cart_items_container.controls.clear()
        cart = page.session.get("cart") or []

        if not cart:
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
            # Opcional: Fondo para "vacío"
            main_container.bgcolor = None

        else:
            # Sí hay productos
            main_container.bgcolor = ft.Colors.WHITE
            checkout_button.visible = True

            # Agregamos un título (similar a “Lista de Favoritos”)
            cart_items_container.controls.append(
                ft.Text("Lista del Carrito de Compra", size=22, weight=ft.FontWeight.BOLD)
            )

            # Creamos la tarjeta para cada ítem
            for idx, item in enumerate(cart):
                if "quantity" not in item:
                    item["quantity"] = 1
                
                product_image = item["image"]
                product_name  = item["name"]
                product_price = float(item["price"])  # Convertimos a float
                quantity      = item["quantity"]
                subtotal      = product_price * quantity

                cart_item = ft.Container(
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
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            # Fila superior: imagen, datos, botones
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                spacing=10,
                                controls=[
                                    # Imagen
                                    ft.Image(
                                        src=product_image,
                                        width=80,
                                        height=80,
                                        fit=ft.ImageFit.COVER,
                                        border_radius=ft.border_radius.all(8),
                                    ),
                                    # Nombre, precio, más/menos
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
                                            # Fila con +, - y cantidad
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(
                                                        icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                                                        on_click=lambda e, i=idx: decrease_quantity(e, i),
                                                    ),
                                                    ft.Text(
                                                        str(quantity),
                                                        size=16,
                                                        weight=ft.FontWeight.BOLD,
                                                        text_align=ft.TextAlign.CENTER,
                                                    ),
                                                    ft.IconButton(
                                                        icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                                        on_click=lambda e, i=idx: increase_quantity(e, i),
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    # Icono de eliminar
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        on_click=lambda e, i=idx: remove_from_cart(e, i),
                                        icon_color=ft.Colors.RED,
                                    ),
                                ],
                            ),
                            # Fila inferior: "Total Order (X) : $subtotal"
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        f"Cantidad ({quantity}) :",
                                        size=14
                                    ),
                                    ft.Text(
                                        f"${subtotal:.2f}",
                                        size=14
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
                cart_items_container.controls.append(cart_item)

            # Calculamos el precio total de todo el carrito
            total_price = sum(float(i["price"]) * i["quantity"] for i in cart)
            total_price_text.value = f"Total: ${total_price:.2f}"

        page.update()

    # Columna general con el carrito, total y botón de checkout
    main_container.content = ft.Container(
      padding=ft.padding.all(10),
      content=ft.Column(
        controls=[
            cart_items_container,
            # Sección final: total + botón
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True,
                controls=[total_price_text, checkout_button],
            ),
        ],
        expand=True,
        scroll=ft.ScrollMode.HIDDEN,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )
    )

    # Cargamos la vista al iniciar
    update_cart_display()
    update_cart_count()

    return main_container
