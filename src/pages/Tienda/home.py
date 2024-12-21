import flet as ft
from pages.utils.navigation import create_footer
from pages.utils.navigation import create_navbar_home
from pages.utils.image import create_image_with_loader
from pages.utils.carusel import create_carousel
from pages.endpoints.Auth import refresh_token, load_user, logout_user
import asyncio

def ViewHome(page):
    page.controls.clear()
    navbar = create_navbar_home(page)[0]
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()

    try:
        access_token = page.client_storage.get("creativeferrets.tienda.access_token")
        if not access_token:
            refresh_token(page)
            access_token = page.client_storage.get("creativeferrets.tienda.access_token")
        if access_token:
            asyncio.run(load_user(page))
        else:
            page.go("/phone-login")
            return
    except Exception as e:
        print(f"Error en la autenticación: {e}")
        page.go("/phone-login")
        return

    def create_tab_content(index):
        categories = [
            "Registro Civil",
            "Autenticación",
            "Escrituras",
            "Matrimonio, Divorcio y Liquidación de Sociedad Conyugal",
            "Declaraciones Juramentadas",
        ]
        contents = [
            registro_civil_content(page),
            autenticacion_content(page),
            escrituras_content(page),
            matrimonio_divorcio_content(page),
            declaraciones_juramentadas_content(page),
        ]
        return contents[index]

    def update_tab_colors(selected_index):
        for i, tab in enumerate(tabs.tabs):
            container = tab.tab_content
            column = container.content
            text = column.controls[0]

            if i == selected_index:
                container.bgcolor = "#FF5700"
                text.color = ft.Colors.WHITE
            else:
                container.bgcolor = None
                text.color = ft.Colors.BLACK

    def update_tab_content(e):
        selected_index = e.control.selected_index if e else 0
        update_tab_colors(selected_index)
        dynamic_content.content = create_tab_content(selected_index)
        page.update()

    tabs = ft.Tabs(
        selected_index=0,
        on_change=update_tab_content,
        indicator_color="#FF5700",
        indicator_border_radius=ft.border_radius.all(10),
        scrollable=True,
        indicator_tab_size=False,
        overlay_color="transparent",
        tabs=[
            ft.Tab(
                tab_content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Registro Civil", size=15,
                                    color=ft.Colors.BLACK),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    border_radius=ft.border_radius.all(10),
                )
            ),
            ft.Tab(
                tab_content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Autenticación", size=15,
                                    color=ft.Colors.BLACK),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    border_radius=ft.border_radius.all(10),
                )
            ),
            ft.Tab(
                tab_content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Escrituras", size=15,
                                    color=ft.Colors.BLACK),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    border_radius=ft.border_radius.all(10),
                )
            ),
            ft.Tab(
                tab_content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Matrimonio y Divorcio",
                                    size=15, color=ft.Colors.BLACK),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    border_radius=ft.border_radius.all(10),
                )
            ),
            ft.Tab(
                tab_content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Declaraciones", size=15,
                                    color=ft.Colors.BLACK),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    border_radius=ft.border_radius.all(10),
                )
            ),
            ft.Tab(
                tab_content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Enrolamiento", size=15,
                                    color=ft.Colors.BLACK),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    border_radius=ft.border_radius.all(10),
                )
            ),
            ft.Tab(
                tab_content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Permiso Viajes de Menores",
                                    size=15, color=ft.Colors.BLACK),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    border_radius=ft.border_radius.all(10),
                )
            ),

        ],
    )
    dynamic_content = ft.Container(content=create_tab_content(0))
    update_tab_colors(0)

    redes_sociales = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                "Redes Sociales",
                size=15,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        content=ft.Lottie(
                            src="https://creativeferrets.com/assets/lottie/facebook.json", reverse=False,
                            animate=True),
                        width=40,
                        height=40,

                    ),
                    ft.VerticalDivider(thickness=3),
                    ft.Container(
                        content=ft.Lottie(
                            src="https://creativeferrets.com/assets/lottie/instagram.json", reverse=False,
                            animate=True),
                        width=40,
                        height=40,

                    ),
                    ft.VerticalDivider(thickness=3),
                    ft.Container(
                        content=ft.Lottie(
                            src="https://creativeferrets.com/assets/lottie/youtube.json", reverse=False,
                            animate=True),
                        width=40,
                        height=40,

                    )
                ]
            )
        ]
    )
    container = ft.Container(
        padding=ft.padding.all(0),
        alignment=ft.alignment.center,
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Container(
                    bgcolor="#007354",
                    padding=ft.padding.all(10),
                    content=ft.TextField(
                        border_radius=ft.border_radius.all(10),
                        content_padding=ft.padding.symmetric(
                            horizontal=20, vertical=15),
                        bgcolor=ft.Colors.WHITE,
                        border_color="#717171",
                        label_style=ft.TextStyle(color="#717171"),
                        border_width=0.5,
                        expand=True,
                        prefix_icon=ft.Icons.SEARCH,
                        hint_text="Buscar en docuflowapp.com",

                    ),
                ),
                ft.Column(
                    scroll=ft.ScrollMode.HIDDEN,
                    spacing=0,
                    expand=True,
                    controls=[
                        ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            width="100%",
                            height=50,
                            padding=ft.padding.all(10),
                            on_click=lambda e: print(
                                "Clickable without Ink clicked!"),
                            ink=True,
                            content=ft.Row(
                                spacing=5,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.SHARE_LOCATION_SHARP,
                                        color=ft.Colors.BLACK,
                                        size=20,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            "Enviar a Baranquilla",
                                            color=ft.Colors.BLACK,
                                        ),
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=True,
                            alignment=ft.alignment.center,
                            content=create_carousel(page),
                            padding=ft.padding.all(10),
                        ),
                        tabs,
                        dynamic_content,
                        redes_sociales
                    ],
                ),
            ],
        ),
    )
    return container


def create_content(page, image, name, valor, url):
    return ft.Container(
        width=200,
        height=350,
        expand=True,
        padding=ft.padding.all(10),
        border_radius=ft.border_radius.all(15),
        bgcolor=ft.Colors.GREY_100,
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=[
                ft.Column(
                    controls=[ft.Row(
                        controls=[
                            ft.Container(
                                width=10,
                                height=10,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.SHOPPING_CART_OUTLINED,
                                icon_color=ft.Colors.WHITE,
                                bgcolor="#FF5700",
                                on_click=lambda e: page.go(
                                    f"/product-detail/{url}"),
                            ),

                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                        ft.Container(
                        alignment=ft.alignment.center,
                        width=150,  # Ajusta el ancho para simular la lámpara
                        height=200,  # Altura de la forma de la lámpara
                        border_radius=ft.BorderRadius(
                            top_left=75,  # Más redondeado en la parte superior
                            top_right=75,
                            bottom_left=40,  # Menos redondeado en la parte inferior
                            bottom_right=40,
                        ),
                        bgcolor="#f0f0f0",  # Color del contenedor de la imagen
                        shadow=ft.BoxShadow(
                            blur_radius=15,
                            spread_radius=5,
                            color="rgba(0,0,0,0.2)",
                        ),
                        content=create_image_with_loader(
                            src=image,
                            width=150,
                            height=200,
                            fit=ft.ImageFit.FILL,
                        ),
                    ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                ),

                ft.Text(
                    name,
                    weight=ft.FontWeight.BOLD,
                    size=18,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                ft.Text("Deep Foam", size=14, color="#717171"),
                ft.Text(f"${valor}", size=18,
                        weight=ft.FontWeight.BOLD),
            ],
            spacing=0,

        ),
    )


def registro_civil_content(page):
    registro_civil_products = [
        {
            "slug": "registro-civil-nacimiento",
            "image": "registro_civil/1.jpg",
            "name": "Copia de Registro civil de Nacimiento",
            "price": "1000",
        },
        {
            "slug": "registro-civil-matrimonio",
            "image": "registro_civil/2.jpeg",
            "name": "Copia de Registro civil de Matrimonio",
            "price": "1000",
        },
        {
            "slug": "registro-civil-recien-nacidos",
            "image": "registro_civil/3.jpeg",
            "name": "Domicilio registro civil para recien nacidos",
            "price": "1000",
        },
        {
            "slug": "registro-civil-defuncion",
            "image": "registro_civil/4.jpeg",
            "name": "Copia de Registro civil de Defunción",
            "price": "1000",
        },
    ]

    rows = []
    for i in range(0, len(registro_civil_products), 2):
        row_controls = []
        for product in registro_civil_products[i:i + 2]:
            row_controls.append(
                ft.Container(
                    width="calc(50% - 10px)",
                    content=create_content(
                        page,
                        product["image"],
                        product["name"],
                        product["price"],
                        product["slug"],
                    ),
                )
            )
        rows.append(
            ft.Row(
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
                controls=row_controls,
            )
        )

    return ft.Container(
        padding=ft.padding.all(5),
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=rows,
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )


def autenticacion_content(page):
    autenticacion_products = [
        {
            "slug": "autenticacion-firma",
            "image": "Autenticacion/1.jpeg",
            "name": "Autenticación de Firma",
            "price": "1000",
        },
        {
            "slug": "autenticacion-copias",
            "image": "Autenticacion/2.jpeg",
            "name": "Autenticación de Copias",
            "price": "1000",
        },
        {
            "slug": "reconocimiento-firma-contenido",
            "image": "Autenticacion/3.jpeg",
            "name": "Reconocimiento de firma y contenido",
            "price": "1000",
        },
        {
            "slug": "firma-a-ruego",
            "image": "Autenticacion/4.jpeg",
            "name": "Firma a Ruego - Personas que no saben o no pueden firmar",
            "price": "1000",
        },
    ]

    rows = []
    for i in range(0, len(autenticacion_products), 2):
        row_controls = []
        for product in autenticacion_products[i:i + 2]:
            row_controls.append(
                ft.Container(
                    width="calc(50% - 10px)",
                    content=create_content(
                        page,
                        product["image"],
                        product["name"],
                        product["price"],
                        product["slug"],
                    ),
                )
            )
        rows.append(
            ft.Row(
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
                controls=row_controls,
            )
        )

    return ft.Container(
        padding=ft.padding.all(5),
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=rows,
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )


def escrituras_content(page):
    escrituras_products = [
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

    rows = []
    for i in range(0, len(escrituras_products), 2):
        row_controls = []
        for product in escrituras_products[i:i + 2]:
            row_controls.append(
                ft.Container(
                    width="calc(50% - 10px)",
                    content=create_content(
                        page,
                        product["image"],
                        product["name"],
                        product["price"],
                        product["slug"],
                    ),
                )
            )
        rows.append(
            ft.Row(
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
                controls=row_controls,
            )
        )

    return ft.Container(
        padding=ft.padding.all(5),
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=rows,
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )


def matrimonio_divorcio_content(page):
    matrimonio_divorcio_products = [
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

    rows = []
    for i in range(0, len(matrimonio_divorcio_products), 2):
        row_controls = []
        for product in matrimonio_divorcio_products[i:i + 2]:
            row_controls.append(
                ft.Container(
                    width="calc(50% - 10px)",
                    content=create_content(
                        page,
                        product["image"],
                        product["name"],
                        product["price"],
                        product["slug"],
                    ),
                )
            )
        rows.append(
            ft.Row(
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
                controls=row_controls,
            )
        )

    return ft.Container(
        padding=ft.padding.all(5),
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=rows,
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )


def declaraciones_juramentadas_content(page):
    declaraciones_juramentadas_products = [
        {"slug": "declaracion-juramentada", "image": "declaraciones_juramentadas/1.jpeg",
            "name": "Declaraciones Juramentadas", "price": "1000"},
        {"slug": "declaracion-ia", "image": "declaraciones_juramentadas/2.jpeg",
            "name": "Declaraciones Juramentadas con IA", "price": "1000"},

    ]

    rows = []
    for i in range(0, len(declaraciones_juramentadas_products), 2):
        row_controls = []
        for product in declaraciones_juramentadas_products[i:i + 2]:
            row_controls.append(
                ft.Container(
                    width="calc(50% - 10px)",
                    content=create_content(
                        page,
                        product["image"],
                        product["name"],
                        product["price"],
                        product["slug"],
                    ),
                )
            )
        rows.append(
            ft.Row(
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
                controls=row_controls,
            )
        )

    return ft.Container(
        padding=ft.padding.all(5),
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=rows,
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )


