import asyncio
import flet as ft

from pages.utils.navigation import create_footer, create_navbar_product
from pages.utils.controls.inputs import MyInputField
from pages.utils.controls.dropdownFlag import CountryDropdown

from pages.endpoints.Coupon import check_coupon
from pages.endpoints.Payments import process_payment, get_payment_total
from pages.endpoints.Shipping import get_shipping_options
from pages.endpoints.Cart import get_items

API_URL = "http://localhost:8000"

def ViewCheckout(page: ft.Page):
    # Limpia la UI
    page.controls.clear()
    navbar, update_cart_count = create_navbar_product(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()

    # Contenedores y campos
    cart_items_container = ft.Column(
        spacing=10,
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    total_price_text = ft.Text("", size=20, weight=ft.FontWeight.BOLD)

    shipping_info_fields = ft.Column(
        controls=[
            MyInputField("Nombre Completo"),
            MyInputField("Dirección (Línea 1)"),
            MyInputField("Dirección (Línea 2)"),
            MyInputField("Ciudad"),
            MyInputField("Estado/Provincia"),
            MyInputField("Código Postal"),
            MyInputField("Teléfono"),
        ],
        spacing=10,
        expand=True,
    )

    country_dropdown = CountryDropdown(on_country_change=None)

    shipping_options_container = ft.Column(controls=[], spacing=10)

    # Campo y botón de cupón
    coupon_field = ft.TextField(
        label="Cupón de descuento",
        hint_text="Ingresa tu código de cupón",
        border_radius=ft.border_radius.all(15),
        content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
        bgcolor=ft.Colors.WHITE,
        border_color="#717171",
        label_style=ft.TextStyle(color="#717171"),
        border_width=0.5,
        expand=True,
    )

    # ------------------------------------------------------------------------
    # FUNCIONES ASÍNCRONAS: TODO accesso a client_storage con get_async/set_async
    # ------------------------------------------------------------------------

    async def apply_coupon_async():
        coupon_code = coupon_field.value.strip()
        if not coupon_code:
            sb = ft.SnackBar(
                content=ft.Text("No ingresaste un cupón."),
                bgcolor=ft.Colors.RED,
            )
            page.overlay.append(sb)
            sb.open = True
            page.update()
            return

        try:
            coupon_data = await check_coupon(page, coupon_code)
            if coupon_data and coupon_data.get("valid", False):
                # Guardar el nombre del cupón asíncronamente
                await page.client_storage.set_async("creativeferrets.coupon.name", coupon_code)
                sb = ft.SnackBar(
                    content=ft.Text("¡Cupón aplicado exitosamente!"),
                    bgcolor=ft.Colors.GREEN,
                )
            else:
                # El cupón no es válido, limpiamos
                await page.client_storage.set_async("creativeferrets.coupon.name", "")
                sb = ft.SnackBar(
                    content=ft.Text("Cupón inválido."),
                    bgcolor=ft.Colors.RED,
                )
            page.overlay.append(sb)
            sb.open = True
            page.update()

        except Exception as ex:
            sb = ft.SnackBar(
                content=ft.Text(f"Error al verificar cupón: {ex}"),
                bgcolor=ft.Colors.RED,
            )
            page.overlay.append(sb)
            sb.open = True
            page.update()

        # Actualizar carrito (por si el cupón afecta el total):
        await update_cart_display_async()

    async def process_payment_action_async():
        error_msg = await validate_shipping_info()
        if error_msg:
            sb = ft.SnackBar(content=ft.Text(error_msg), bgcolor=ft.Colors.RED)
            page.overlay.append(sb)
            sb.open = True
            page.update()
            return

        # Verificar el carrito
        try:
            cart_data = await get_items(page)
        except Exception as ex:
            sb = ft.SnackBar(
                content=ft.Text(f"Error al obtener el carrito: {ex}"),
                bgcolor=ft.Colors.RED,
            )
            page.overlay.append(sb)
            sb.open = True
            page.update()
            return

        # Cargar datos de shipping y cupón
        shipping_data = await page.client_storage.get_async("creativeferrets.shipping.info") or {}
        shipping_id = await page.client_storage.get_async("creativeferrets.selected_shipping_id") or ""
        applied_coupon = await page.client_storage.get_async("creativeferrets.coupon.name") or ""

        if not cart_data.get("cart"):
            sb = ft.SnackBar(
                content=ft.Text("Carrito vacío. No se puede procesar pago."),
                bgcolor=ft.Colors.RED,
            )
            page.overlay.append(sb)
            sb.open = True
            page.update()
            return

        # Procesar el pago en el backend
        try:
            payment_result = await process_payment(
                page=page,
                shipping_id=shipping_id,
                coupon_name=applied_coupon,
                full_name=shipping_data.get("Nombre Completo", ""),
                address_line_1=shipping_data.get("Dirección (Línea 1)", ""),
                address_line_2=shipping_data.get("Dirección (Línea 2)", ""),
                city=shipping_data.get("Ciudad", ""),
                state_province_region=shipping_data.get("Estado/Provincia", ""),
                postal_zip_code=shipping_data.get("Código Postal", ""),
                country_region=shipping_data.get("País", ""),
                telephone_number=shipping_data.get("Teléfono", ""),
            )
            if payment_result and payment_result.get("success", False):
                # Limpiar el carrito en client_storage
                await page.client_storage.set_async("creativeferrets.cart.items", {"cart": []})
                update_cart_count()
                page.go("/payment-success")
            else:
                sb = ft.SnackBar(
                    content=ft.Text("Error en el proceso de pago."),
                    bgcolor=ft.Colors.RED,
                )
                page.overlay.append(sb)
                sb.open = True
                page.update()

        except Exception as ex:
            sb = ft.SnackBar(
                content=ft.Text(f"Excepción al procesar pago: {ex}"),
                bgcolor=ft.Colors.RED,
            )
            page.overlay.append(sb)
            sb.open = True
            page.update()

    async def load_shipping_options_async():
        """Obtiene opciones de envío usando métodos asíncronos de client_storage."""
        # Verificamos si ya está en client_storage
        has_shipping_options = await page.client_storage.contains_key_async("creativeferrets.shipping.options")

        if has_shipping_options:
            shipping_options = await page.client_storage.get_async("creativeferrets.shipping.options")
        else:
            try:
                shipping_options = await get_shipping_options()
                await page.client_storage.set_async("creativeferrets.shipping.options", shipping_options)
            except Exception:
                shipping_options = []

        shipping_options_container.controls.clear()

        selected_shipping_id = await page.client_storage.get_async("creativeferrets.selected_shipping_id") or ""
        radio_group = ft.RadioGroup(
            content=ft.Text("Selecciona una opción de envío", size=16, weight=ft.FontWeight.BOLD),
            value=selected_shipping_id,
            on_change=on_shipping_selected  # wrapper sincrónico
        )
        radio_row = ft.Column()

        for option in shipping_options.get('shipping_options', []):
            radio = ft.Radio(
                label=f"{option['name']} - ${option['price']} ({option['time_to_delivery']})",
                value=option['id'],
            )
            radio_row.controls.append(radio)

        radio_group.content = radio_row
        shipping_options_container.controls.append(radio_group)
        page.update()

    async def on_shipping_selected_async(value):
        """Al seleccionar un shipping_id, lo guardamos y refrescamos el carrito."""
        await page.client_storage.set_async("creativeferrets.selected_shipping_id", value)
        await update_cart_display_async()

    async def update_cart_display_async():
        """Muestra items del carrito y calcula total con shipping y/o cupón."""
        cart_items_container.controls.clear()

        # Obtener carrito
        try:
            cart_data = await get_items(page)
        except Exception as ex:
            sb = ft.SnackBar(
                content=ft.Text(f"Error al obtener el carrito: {ex}"),
                bgcolor=ft.Colors.RED,
            )
            page.overlay.append(sb)
            sb.open = True
            page.update()
            return

        if not cart_data or len(cart_data.get("cart", [])) == 0:
            cart_items_container.controls.append(
                ft.Container(
                    padding=ft.padding.all(10),
                    content=ft.Column(
                        controls=[
                            ft.Image(src="logo.png", width=100, height=100),
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
                                on_click=lambda _: page.go("/home"),
                                bgcolor="#FF5700",
                                color="white",
                                width=150,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                )
            )
            total_price_text.value = ""
            pay_button.visible = False
            page.update()
            pay_button.visible = True
            return

        # Si no está vacío
        for item in cart_data["cart"]:
            try:
                product = item["product"]
                product_name = product["name"]
                product_price = float(product["price"])
                quantity = int(item["count"])
                product_image = product.get("photo", "logo.png")
                subtotal = product_price * quantity
            except (KeyError, TypeError):
                continue

            cart_item = ft.Container(
                padding=ft.padding.all(10),
                alignment=ft.alignment.center,
                content=ft.Row(
                    controls=[
                        ft.Image(
                            src=f"{API_URL}{product_image}",
                            width=80,
                            height=80,
                            border_radius=ft.border_radius.all(10),
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        ft.Column(
                            expand=True,
                            controls=[
                                ft.Text(
                                    product_name,
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    max_lines=2,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Text(f"Precio unitario: ${product_price:.2f}", size=14),
                                ft.Text(f"Cantidad: {quantity}", size=14),
                                ft.Text(
                                    f"Subtotal: ${subtotal:.2f}",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                ),
            )
            cart_items_container.controls.append(cart_item)

        # Tomar shippingId y cupón
        shipping_id = await page.client_storage.get_async("creativeferrets.selected_shipping_id") or ""
        applied_coupon = await page.client_storage.get_async("creativeferrets.coupon.name") or ""

        if not shipping_id:
            total_price_text.value = "Total: $0.00"
            page.update()
            return

        # Obtener total
        try:
            payment_data = await get_payment_total(
                page=page,
                shipping_id=shipping_id,
                coupon_name=applied_coupon if applied_coupon else "default",
            )
            if payment_data and "total_amount" in payment_data:
                total_amount = float(payment_data["total_amount"])
                total_price_text.value = f"Total: ${total_amount:.2f}"
                await page.client_storage.set_async("creativeferrets.cart.total", payment_data)
            else:
                total_price_text.value = "Total: $0.00"
        except Exception:
            total_price_text.value = "Total: $0.00"

        page.update()

    async def _init_view_async():
        """Carga opciones de envío y actualiza el carrito al abrir la vista."""
        await load_shipping_options_async()
        await update_cart_display_async()

    # -----------------------------------------------------------------------
    # WRAPPERS SINCRÓNICOS (eventos UI), que internamente usan page.run_task(...)
    # -----------------------------------------------------------------------
    def on_apply_coupon_click(e):
        page.run_task(apply_coupon_async)

    def on_pay_button_click(e):
        page.run_task(process_payment_action_async)

    def on_shipping_selected(e: ft.ControlEvent):
        # e.control.value => shipping_id
        page.run_task(on_shipping_selected_async, e.control.value)

    def init_view():
        page.run_task(_init_view_async)

    # -----------------------------------------------------------------------
    # VALIDACIÓN DE CAMPOS DE ENVÍO (SINCRÓNICA, no llama a endpoints)
    # -----------------------------------------------------------------------
    async def validate_shipping_info():
        required_labels = [
            "Nombre Completo",
            "Dirección (Línea 1)",
            "Ciudad",
            "Estado/Provincia",
            "Código Postal",
            "Teléfono",
        ]
        shipping_data = {}
        for ctrl in shipping_info_fields.controls:
            label = ctrl.controls[0].value
            value = ctrl.controls[1].value.strip()
            shipping_data[label] = value

        for req_label in required_labels:
            if not shipping_data.get(req_label):
                return f"El campo '{req_label}' es obligatorio."

        selected_country = country_dropdown.value if country_dropdown.value else "Colombia"
        shipping_data["País"] = selected_country

        # Guardar asíncronamente
        # (Para no mezclar, lo hacemos en un wrapper, pero aquí un "quick approach" => blocking)
        # Lo ideal: page.run_task() => async, pero si es corto, no hay problema.
        # Ejemplo:
        #   await page.client_storage.set_async("creativeferrets.shipping.info", shipping_data)
        #   => No se puede 'await' en una función sync, se hace en otro wrapper
        # 
        # Por simplicidad se asume que "validate_shipping_info()" es rápido:
        await page.client_storage.set_async("creativeferrets.shipping.info", shipping_data)

        return None

    # -----------------------------------------------------------------------
    # CONSTRUIMOS LA INTERFAZ FINAL
    # -----------------------------------------------------------------------
    update_cart_count()
    init_view()

    pay_button = ft.ElevatedButton(
        text="Completar pago",
        on_click=on_pay_button_click,
        bgcolor="#FF5700",
        color="white",
        width=200,
    )
    apply_coupon_button = ft.ElevatedButton(
        text="Aplicar",
        on_click=on_apply_coupon_click,
        bgcolor="#FF5700",
        color="white",
    )

    main_container = ft.Container(
        padding=ft.padding.all(10),
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=[
                ft.Text("Checkout", size=24, weight=ft.FontWeight.BOLD),
                cart_items_container,
                ft.Divider(),
                ft.Column(
                    controls=[
                        ft.Text("Información de Envío", size=20, weight=ft.FontWeight.BOLD),
                        shipping_info_fields,
                        ft.Text("País", style=ft.TextStyle(color="#717171")),
                        country_dropdown,
                        ft.Text("Opciones de Envío", size=20, weight=ft.FontWeight.BOLD),
                        shipping_options_container,
                    ],
                    spacing=10,
                ),
                ft.Row(
                    controls=[coupon_field, apply_coupon_button],
                    spacing=10,
                ),
                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[total_price_text, pay_button],
                ),
                ft.Container(height=20),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
    )

    return main_container
