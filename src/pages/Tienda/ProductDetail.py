import flet as ft
from pages.utils.navigation import create_footer, create_navbar_product


def get_product_by_slug(slug):
    all_products = (
        # Registro Civil
        [
            {"slug": "registro-civil-nacimiento", "image": "registro_civil/1.jpg",
             "name": "Copia de Registro civil de Nacimiento", "price": "1000"},
            {"slug": "registro-civil-matrimonio", "image": "registro_civil/2.jpeg",
             "name": "Copia de Registro civil de Matrimonio", "price": "1000"},
            {"slug": "registro-civil-recien-nacidos", "image": "registro_civil/3.jpeg",
             "name": "Domicilio registro civil para recien nacidos", "price": "1000"},
            {"slug": "registro-civil-defuncion", "image": "registro_civil/4.jpeg",
             "name": "Copia de Registro civil de Defunción", "price": "1000"},
        ]
        # Autenticación
        + [
            {"slug": "autenticacion-firma", "image": "Autenticacion/1.jpeg",
             "name": "Autenticación de Firma", "price": "1000"},
            {"slug": "autenticacion-copias", "image": "Autenticacion/2.jpeg",
             "name": "Autenticación de Copias", "price": "1000"},
            {"slug": "reconocimiento-firma-contenido", "image": "Autenticacion/3.jpeg",
             "name": "Reconocimiento de firma y contenido", "price": "1000"},
            {"slug": "firma-a-ruego", "image": "Autenticacion/4.jpeg",
             "name": "Firma a Ruego - Personas que no saben o no pueden firmar", "price": "1000"},
        ]
        # Escrituras
        + [
            {"slug": "copia-autenticada-escritura", "image": "Escritura/1.jpeg",
                "name": "Copia autenticada de escritura", "price": "1000"},
            {"slug": "copia-simple-escritura", "image": "Escritura/2.jpeg",
                "name": "Copia simple de escritura", "price": "1000"},
            {"slug": "copia-electronica-escritura", "image": "Escritura/3.jpeg",
                "name": "Copia electrónica de escritura", "price": "1000"},
            {"slug": "copia-testimonial-escritura", "image": "Escritura/4.jpeg",
                "name": "Copia testimonial notarial de escritura", "price": "1000"},
            {"slug": "copia-extracto-escritura", "image": "Escritura/5.jpeg",
                "name": "Copia de extracto de escritura", "price": "1000"},
            {"slug": "minuta-escritura-ia", "image": "Escritura/6.jpeg",
                "name": "Haz tu minuta de escritura con IA", "price": "1000"},
            {"slug": "poder-ia", "image": "Escritura/7.jpeg",
                "name": "Haz tu poder en minutos con IA", "price": "1000"},
            {"slug": "cambio-nombre", "image": "Escritura/8.jpeg",
                "name": "Cambio de Nombre", "price": "1000"},
            {"slug": "testamento-ia", "image": "Escritura/9.jpeg",
                "name": "Haz tu testamento con IA", "price": "1000"},
            {"slug": "afectacion-vivienda-familiar", "image": "Escritura/10.jpeg",
                "name": "Afectación a Vivienda familiar", "price": "1000"},
            {"slug": "patrimonio-familia-inembargable", "image": "Escritura/11.jpeg",
                "name": "Patrimonio de familia inembargable", "price": "1000"},
            {"slug": "compraventa-inmuebles", "image": "Escritura/12.jpeg",
                "name": "Compraventa de inmuebles", "price": "1000"},
            {"slug": "cancelacion-hipoteca", "image": "Escritura/13.jpeg",
                "name": "Cancelación de Hipoteca", "price": "1000"},
            {"slug": "permuta-inmuebles", "image": "Escritura/14.jpeg",
                "name": "Permuta de Inmuebles", "price": "1000"},
            {"slug": "donacion", "image": "Escritura/15.jpeg",
                "name": "Donación", "price": "1000"},
            {"slug": "constitucion-hipoteca", "image": "Escritura/16.jpeg",
                "name": "Constitución de hipoteca", "price": "1000"},
            {"slug": "sucesion-bienes", "image": "Escritura/17.jpeg",
                "name": "Sucesión de bienes por causa de muerte", "price": "1000"},
            {"slug": "correccion-identidad-sexual", "image": "Escritura/18.jpeg",
                "name": "Corrección Componente de Identidad Sexual", "price": "1000"},
        ]
        # Matrimonio y Divorcio
        + [
            {"slug": "matrimonio-domicilio", "image": "matrimonio_divorcio/1.jpeg",
             "name": "Matrimonio a Domicilio", "price": "1000"},
            {"slug": "fecha-matrimonio-notaria", "image": "matrimonio_divorcio/2.jpeg",
             "name": "Escoje tu fecha de matrimonio en notaria", "price": "1000"},
            {"slug": "divorcio", "image": "matrimonio_divorcio/3.jpeg",
             "name": "Divorcio", "price": "1000"},
            {"slug": "liquidacion-sociedad-conyugal", "image": "matrimonio_divorcio/4.jpeg",
             "name": "Liquidación de Sociedad Conyugal", "price": "1000"},
            {"slug": "union-marital-hecho", "image": "matrimonio_divorcio/5.jpeg",
             "name": "Declaración de Unión Marital de Hecho", "price": "1000"},
            {"slug": "capitulaciones-matrimoniales", "image": "matrimonio_divorcio/6.jpeg",
             "name": "Capitulaciones Matrimoniales", "price": "1000"},
            {"slug": "separacion-bienes", "image": "matrimonio_divorcio/7.jpeg",
             "name": "Separación de Bienes", "price": "1000"},
        ]

        + [
            {"slug": "declaracion-juramentada", "image": "declaraciones_juramentadas/1.jpeg",
             "name": "Declaraciones Juramentadas", "price": "1000"},
            {"slug": "declaracion-ia", "image": "declaraciones_juramentadas/2.jpeg",
             "name": "Declaraciones Juramentadas con IA", "price": "1000"},

        ]
    )

    for product in all_products:
        if product["slug"] == slug:
            return product
    return None


def extract_slug_from_url(url):

    return url.replace("/product-detail/", "")


def ViewProductDetail(page, url):

    slug = extract_slug_from_url(url)
    product = get_product_by_slug(slug)

    product_name = product["name"] if product else "Producto no encontrado"
    product_image = product["image"] if product else "https://via.placeholder.com/400x200"
    product_price = product["price"] if product else "N/A"
    product_description = "Descripción no disponible." if not product else "Este es un producto detallado."
    page.controls.clear()
    navbar, update_cart_count = create_navbar_product(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()
    def add_to_cart(e):
        cart = page.session.get("cart")
        if cart is None:
            cart = []
        cart.append(product)
        page.session.set("cart", cart)
        snackbar = ft.SnackBar(
            content=ft.Text(
                f"Agregaste {product_name} al carrito.", color="white"),
            bgcolor="green",
        )
        page.overlay.append(snackbar)
        snackbar.open = True
        update_cart_count()
        page.update()

    is_favorite = [False]



    heart_icon = ft.IconButton(
        icon=ft.Icons.FAVORITE_BORDER,
        style=ft.ButtonStyle(icon_color="black"),
        icon_size=24,
        on_click=lambda e: toggle_favorite(product, page, is_favorite, heart_icon),
    )

    add_to_cart_button = ft.ElevatedButton(
            text="Agregar al carrito",
            on_click=add_to_cart,
            bgcolor="#FF5700",
            color="white",
        )

    product_image_container = ft.Container(
        content=ft.Image(
            src=product_image,
            fit=ft.ImageFit.COVER,
        ),
        width=page.width,
        height=200,
        border_radius=ft.border_radius.all(15),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    product_info = ft.Column(
        spacing=5,
        controls=[
            ft.Text(product_name, size=24, weight=ft.FontWeight.BOLD),
            ft.Row(
                spacing=10,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Container(),
                    ft.Text("Disponible", size=14, color="green"),
                ],
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("Agregar a favoritos", size=14, color="black"),
                    heart_icon,
                ]
            )
        ],
    )

    product_description_section = ft.Column(
        spacing=5,
        controls=[
            ft.Text("Descripción", size=16, weight=ft.FontWeight.BOLD),
            ft.Text(product_description, size=14, color=ft.Colors.GREY),
        ],
    )

    product_price_and_button = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Text(f"Precio: ${product_price}", size=18, color="green"),
            add_to_cart_button,
        ],
    )

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
                product_price_and_button,
                ft.Container(height=10),
            ],
        ),
    )

    return product_detail_container

def toggle_favorite(product, page, is_favorite, heart_icon):
    is_favorite[0] = not is_favorite[0]
    favorites = page.session.get("favorites")
    if not favorites:
        favorites = []

    if is_favorite[0]:
        if product not in favorites:
            favorites.append(product)
            page.session.set("favorites", favorites)

        heart_icon.icon = ft.Icons.FAVORITE
        heart_icon.style = ft.ButtonStyle(icon_color="red")
        snackbar = ft.SnackBar(
            content=ft.Text(
                f"Agregaste {product['name']} a tus favoritos.", color="white"
            ),
            bgcolor="green",
        )
    else:
        favorites = [fav for fav in favorites if fav["slug"] != product["slug"]]
        page.session.set("favorites", favorites)
        heart_icon.icon = ft.Icons.FAVORITE_BORDER
        heart_icon.style = ft.ButtonStyle(icon_color="black")
        snackbar = ft.SnackBar(
            content=ft.Text(
                f"Eliminaste {product['name']} de tus favoritos.", color="white"
            ),
            bgcolor="red",
        )

    page.overlay.append(snackbar)
    snackbar.open = True

    page.update()
