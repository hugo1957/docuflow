import flet as ft
from pages.utils.navigation import create_footer
from threading import Timer
from pages.utils.navigation import create_navbar_home


def ViewHome(page):
    page.controls.clear()
    navbar, update_cart_count = create_navbar_home(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)

    def create_carousel(page):
        # Lista de imágenes
        images = [
            {"src": "banner/1.png", "alt": "Banner 1"},
            {"src": "Autenticacion/1.jpeg", "alt": "Banner 2"},
            {"src": "banner/2.png", "alt": "Banner 3"},
        ]
        active_index = 0

        animated_image = ft.AnimatedSwitcher(
            ft.Container(
                content=ft.Image(
                    src=images[0]["src"],
                    width="100%",
                    height="100%",
                    fit=ft.ImageFit.CONTAIN,  # Ocupa todo el contenedor
                ),
                width="100%",
                height=200,
                border_radius=ft.border_radius.all(15),  
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
            duration=500, 
            transition=ft.AnimatedSwitcherTransition.FADE,
        )
        def update_carousel(index=None):
            nonlocal active_index
            if index is None:
                active_index = (active_index + 1) % len(images)
            else:  
                active_index = index
            animated_image.content = ft.Container(
                content=ft.Image(
                    src=images[active_index]["src"],
                    fit=ft.ImageFit.COVER,
                ),
                width=page.window.width,
                height=200,
                border_radius=ft.border_radius.all(15),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            )
            update_dots()
            page.update()
        def update_dots():
            for i, dot in enumerate(dots.controls):
                dot.bgcolor = "#007BFF" if i == active_index else "#CCCCCC"
        def start_timer():
            def auto_update():
                update_carousel()
                start_timer() 
            Timer(4.0, auto_update).start() 
        dots = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=10,
                    height=10,
                    border_radius=50,
                    bgcolor="#007BFF" if i == active_index else "#CCCCCC",
                    on_click=lambda e, i=i: update_carousel(i),
                )
                for i in range(len(images))
            ],
        )

        carousel = ft.Container(
            width=page.window.width,
            content=ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=page.window.width,
                        height=200,
                        content=animated_image, 
                    ),
                    ft.Container(
                        alignment=ft.alignment.center,
                        padding=ft.padding.symmetric(vertical=10),
                        content=dots, 
                    ),
                ],
            ),
        )
        start_timer()
        return carousel

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
                container.bgcolor = "#e5bc16"
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
        indicator_color="#e5bc16",
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
        ],
    )
    dynamic_content = ft.Container(content=create_tab_content(0))
    update_tab_colors(0)
    container = ft.Container(
        padding=ft.padding.all(0),
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Container(
                    bgcolor="#005B7A",
                    padding=ft.padding.all(10),
                    content=ft.TextField(
                        bgcolor=ft.Colors.WHITE,
                        color=ft.Colors.BLACK,
                        label="Buscar en DocuFlow.com",
                        prefix_icon=ft.Icons.SEARCH,
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
                            width=page.window.width,
                            content=create_carousel(page),
                            padding=ft.padding.all(15),
                        ),
                        tabs,
                        dynamic_content,
                    ],
                ),
            ],
        ),
    )
    return container


def create_content(page, image, name, valor, url):
    return ft.Container(
        width=200,
        height=300,
        expand=True,
        padding=ft.padding.all(10),
        border_radius=ft.border_radius.all(15),
        bgcolor=ft.Colors.GREY_100,
        content=ft.Column(
            controls=[

                ft.Stack(
                    [
                        ft.Image(
                            src=image,
                            width=200,
                            height=140,
                            fit=ft.ImageFit.COVER,
                            border_radius=ft.border_radius.all(15),
                        ),

                    ]
                ),
                ft.Text(
                    name,
                    weight=ft.FontWeight.BOLD,
                    size=18,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,  
                ),
                ft.Text("Deep Foam", size=14, color="#717171"),
                ft.Row(
                    controls=[
                        ft.Text(f"${valor}", size=18, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.Icons.SHOPPING_CART_OUTLINED,
                                icon_color=ft.Colors.WHITE,
                                bgcolor="#e5bc16",
                                on_click=lambda e: page.go(f"/product-detail/{url}"),
                            ),
                            border_radius=ft.border_radius.all(8),
                            width=40,
                            height=40,
                            bgcolor="#e5bc16",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

            ],
            spacing=10,
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
                        f"/product-detail/{product['slug']}"
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
        content=ft.Column(controls=rows, expand=True,
                          scroll=ft.ScrollMode.HIDDEN,
                          alignment=ft.MainAxisAlignment.CENTER,
                          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                          spacing=10,),
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
                        f"/product-detail/{product['slug']}"
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

    # Crear el contenedor principal con las filas generadas
    return ft.Container(
        padding=ft.padding.all(5),
        alignment=ft.alignment.center,
        content=ft.Column(controls=rows,expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,),
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
                        f"/product-detail/{product['slug']}"
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

    # Agregar el botón "Ver Más" al final
    rows.append(
        ft.Container(
            alignment=ft.alignment.top_right,
            content=ft.TextButton(
                text="Ver Más",
                on_click=lambda e: print("Ver Más"),
            ),
        )
    )

    # Crear el contenedor principal
    return ft.Container(
        padding=ft.padding.all(5),
        alignment=ft.alignment.center,
        content=ft.Column(controls=rows,expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,),
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
                        f"/product-detail/{product['slug']}"
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

    # Agregar el botón "Ver Más" al final
    rows.append(
        ft.Container(
            alignment=ft.alignment.top_right,
            content=ft.TextButton(
                text="Ver Más",
                on_click=lambda e: print("Ver Más"),
            ),
        )
    )

    # Crear el contenedor principal
    return ft.Container(
        padding=ft.padding.all(5),
        alignment=ft.alignment.center,
        content=ft.Column(controls=rows,expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,),
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
                        f"/product-detail/{product['slug']}"
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

    # Agregar el botón "Ver Más" al final
    rows.append(
        ft.Container(
            alignment=ft.alignment.top_right,
            content=ft.TextButton(
                text="Ver Más",
                on_click=lambda e: print("Ver Más"),
            ),
        )
    )

    # Crear el contenedor principal
    return ft.Container(
        padding=ft.padding.all(5),
        alignment=ft.alignment.center,
        content=ft.Column(controls=rows,expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,),
    )
