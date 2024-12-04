from pages.utils.inputs import create_input_field, create_dropdown_field
import datetime
from threading import Timer
from pages.utils.alert import show_construction_dialog
import re
import flet as ft
import os
from functools import lru_cache
import threading
from pages.home import ViewHome
from pages.utils.json import json_base64
from pages.utils.navigation import create_footer
from pages.auth.Profile import ViewProfile


def main(page: ft.Page):
    page.adaptive = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    theme = ft.Theme()
    theme.page_transitions.windows = ft.PageTransitionTheme.NONE
    theme.page_transitions.android = ft.PageTransitionTheme.NONE
    theme.page_transitions.ios = ft.PageTransitionTheme.NONE
    page.theme = theme
    page.window.always_on_top = True
    # page.session.set("api_url", "https://app.latirculm.com")
    # page.fonts = {
    #     "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
    # }
    # page.theme = ft.Theme(
    #     primary_color_dark="black",
    #     primary_color_light="white",
    # )
    page.padding = ft.padding.all(0)

    def event(e):
        if e.data == "detach" and page.platform == ft.PagePlatform.ANDROID:
            os._exit(1)
    page.on_app_lifecycle_state_change = event

    def show_loader():
        loader = ft.Container(
            content=ft.ProgressRing(width=50, height=50, stroke_width=5),
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.TRANSPARENT)
        )
        page.overlay.append(loader)
        page.update()

    def hide_loader():
        if page.overlay:
            page.overlay.pop()
            page.update()

    @lru_cache(maxsize=None)
    def load_view(view_function):
        timer = threading.Timer(0.5, show_loader)
        timer.start()

        def wrapper():
            view_function()
            timer.cancel()
            hide_loader()

        threading.Thread(target=wrapper).start()

    def handle_navigation(route):
        page.controls.clear()

        if route == "/":
            load_view(lambda: page.add(ft.SafeArea(
                content=ViewHome(page), expand=True)))
        elif route == "/profile":
            load_view(lambda: page.add(ft.SafeArea(
                content=ViewProfile(page), expand=True)))

        page.update()

    def route_change(e):
        handle_navigation(e.route)

    def view_pop(e):
        page.controls.pop()
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)



def ViewHome(page):
    nav_bar = ft.AppBar(
        bgcolor="#005B7A",
    )
    page.appbar = nav_bar
    page.navigation_bar = create_footer(page)

    def open_dlg(e, text):
        def show_loader():
            if not e.control.page.overlay:
                dlg = ft.AlertDialog(
                    content=ft.ProgressRing(
                        width=50, height=50, stroke_width=5),
                    title=ft.Text("Cargando...")
                )
                e.control.page.overlay.append(dlg)
                dlg.open = True
                page.update()

        def load_dialog():
            dlg = ft.AlertDialog(
                title=ft.Text(text),
                actions=[
                    ft.TextButton(
                        "Cerrar", on_click=lambda e: close_dialog(dlg))
                ],
            )
            if e.control.page.overlay:
                e.control.page.overlay.pop()
            e.control.page.overlay.append(dlg)
            dlg.open = True
            page.update()

        def close_dialog(dlg):
            dlg.open = False
            page.update()
        threading.Thread(target=load_dialog).start()
        threading.Timer(0.5, show_loader).start()

    def create_carousel(page):
        # Lista de imágenes
        images = [
            {"src": "banner/1.png", "alt": "Banner 1"},
            {"src": "Autenticacion/1.jpeg", "alt": "Banner 2"},
            {"src": "banner/2.png", "alt": "Banner 3"},
        ]

        # Índice para la imagen activa
        active_index = 0

        # Imagen animada
        animated_image = ft.AnimatedSwitcher(
            ft.Container(
                content=ft.Image(
                    src=images[0]["src"],
                    width=page.window.width,
                    height=200,
                    fit=ft.ImageFit.CONTAIN,
                ),
                width=page.window.width,
                height=200,
                border_radius=ft.border_radius.all(15),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
            duration=500,
            transition=ft.AnimatedSwitcherTransition.FADE,
        )

        # Función para actualizar el carrusel
        def update_carousel(index=None):
            nonlocal active_index
            if index is None:  # Cambio automático
                active_index = (active_index + 1) % len(images)
            else:  # Cambio manual
                active_index = index

            # Actualizar imagen animada
            animated_image.content = ft.Container(
                content=ft.Image(
                    src=images[active_index]["src"],
                    width=page.window.width,
                    height=200,
                    fit=ft.ImageFit.COVER,
                ),
                width=page.window.width,
                height=200,
                border_radius=ft.border_radius.all(15),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            )
            update_dots()
            page.update()

        # Función para actualizar los puntos
        def update_dots():
            for i, dot in enumerate(dots.controls):
                dot.bgcolor = "#007BFF" if i == active_index else "#CCCCCC"

        # Temporizador para el cambio automático de imágenes
        def start_timer():
            def auto_update():
                update_carousel()
                start_timer()  # Reinicia el temporizador

            timer = threading.Timer(4.0, auto_update)
            timer.start()

        # Controles de puntos
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

        # Contenedor del carrusel
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

        # Listener para cambios en el tamaño de la ventana
        def on_resize(e):
            carousel.width = page.window.width
            update_carousel()

        page.on_resized = on_resize
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
            registro_civil_content(),
            autenticacion_content(),
            escrituras_content(),
            matrimonio_divorcio_content(),
            declaraciones_juramentadas_content(),
        ]
        return contents[index]


    def update_tab_content(e):
        selected_index = e.control.selected_index if e else 0
        for i, tab in enumerate(tabs.tabs):
            container = tab.tab_content  # Accede al contenedor del tab
            column = container.content  # Accede al contenido dentro del contenedor
            text = column.controls[0]  # Accede al texto dentro del contenido

            # Estilo dinámico según el tab seleccionado
            if i == selected_index:
                container.bgcolor = "#e5bc16"  # Fondo amarillo
                text.color = ft.Colors.WHITE  # Letras blancas
            else:
                container.bgcolor = None  # Sin fondo
                text.color = ft.Colors.BLACK  # Letras negras

        # Cambia el contenido dinámico según el tab seleccionado
        dynamic_content.content = create_tab_content(selected_index)
        page.update()


    # Tabs dinámicos
    tabs = ft.Tabs(
        selected_index=0,
        on_change=update_tab_content,
        indicator_color="#e5bc16",  # Indicador amarillo para la selección
        indicator_border_radius=ft.border_radius.all(10),
        scrollable=True,
        tabs=[
            ft.Tab(
                tab_content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Registro Civil", size=15, color=ft.Colors.BLACK),
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
                            ft.Text("Autenticación", size=15, color=ft.Colors.BLACK),
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
                            ft.Text("Escrituras", size=15, color=ft.Colors.BLACK),
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
                            ft.Text("Matrimonio y Divorcio", size=15, color=ft.Colors.BLACK),
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
                            ft.Text("Declaraciones", size=15, color=ft.Colors.BLACK),
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
                            )
                        ),
                        ft.Container(content=create_carousel(
                            page), padding=ft.padding.all(15)),
                        tabs,
                        dynamic_content,
                    ]
                )
            ]
        )
    )
    return container



def create_content(image, name, valor, rating):
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
                # Texto principal
                ft.Text(name, weight=ft.FontWeight.BOLD, size=18),
                ft.Text("Deep Foam", size=14, color="#717171"),
                # Precio y botón
                ft.Row(
                    controls=[
                        ft.Text(f"${valor}", size=18, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.Icons.SHOPPING_CART_OUTLINED,
                                icon_color=ft.Colors.WHITE,
                                bgcolor="#D69F7E",
                                on_click=lambda e: print(f"Agregado al carrito: {name}"),
                            ),
                            border_radius=ft.border_radius.all(8),
                            width=40,
                            height=40,
                            bgcolor="#D69F7E",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                
            ],
            spacing=10,
        ),
    )


def registro_civil_content():
    return ft.Container(
        padding=ft.padding.all(5),
        content=ft.Column(
            controls=[
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",  
                            content=create_content(
                                "registro_civil/1.jpg", "Copia de Registro civil de Nacimiento", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "registro_civil/2.jpeg", "Copia de Registro civil de Matrimonio", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                ft.Row(
                  scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "registro_civil/3.jpeg", "Domicilio registro civil para recien nacidos", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "registro_civil/4.jpeg", "Copia de Registro civil de Defunción", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
            ]
        ),
    )



def autenticacion_content():
    return ft.Container(
      padding=ft.padding.all(5),
        content=ft.Column(
            controls=[
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Autenticacion/1.jpeg", "Autenticación de Firma ", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Autenticacion/2.jpeg", "Autenticación de Copias ", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                ft.Row(
                  scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Autenticacion/3.jpeg", "Reconocimiento de firma y contenido", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Autenticacion/4.jpeg", " Firma a Ruego - Personas que no saben o no puede firmar", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
            ]
        ),
    )


def escrituras_content():
    return ft.Container(
        padding=ft.padding.all(5),
        content=ft.Column(
            controls=[
                # Primera fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/1.jpeg", "Copia autenticada de escritura", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/2.jpeg", "Copia simple de escritura", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Segunda fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/3.jpeg", "Copia electrónica de escritura", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/4.jpeg", "Copia testimonial notarial de escritura", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Tercera fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/5.jpeg", "Copia de extracto de escritura", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/6.jpeg", "Haz tu minuta de escritura con IA", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Cuarta fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/7.jpeg", "Haz tu poder en minutos con IA", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/8.jpeg", "Cambio de Nombre", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Quinta fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/9.jpeg", "Haz tu testamento con IA", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/10.jpeg", "Afectación a Vivienda familiar", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Sexta fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/11.jpeg", "Patrimonio de familia inembargable", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/12.jpeg", "Compraventa de inmuebles", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Séptima fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/13.jpeg", "Cancelación de Hipoteca", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/14.jpeg", "Permuta de Inmuebles", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Octava fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/15.jpeg", "Donación", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/16.jpeg", "Constitución de hipoteca", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Novena fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/17.jpeg", "Sucesión de bienes por causa de muerte", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Escritura/18.jpeg", "Corrección Componente de Identidad Sexual", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Botón "Ver Más"
                ft.Container(
                    alignment=ft.alignment.top_right,
                    content=ft.TextButton(
                        text="Ver Más", on_click=lambda e: print("Ver Más")
                    ),
                ),
            ]
        )
    )


def matrimonio_divorcio_content():
    return ft.Container(
        padding=ft.padding.all(5),
        content=ft.Column(
            controls=[
                # Primera fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "matrimonio_divorcio _y_Liquidacion_de_Sociedad_Conyugal/1.jpeg", "Matrimonio a Domicilio", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "matrimonio_divorcio _y_Liquidacion_de_Sociedad_Conyugal/2.jpeg", "Escoje tu fecha de matrimonio en notaria", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Segunda fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "matrimonio_divorcio _y_Liquidacion_de_Sociedad_Conyugal/3.jpeg", "Divorcio", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "matrimonio_divorcio _y_Liquidacion_de_Sociedad_Conyugal/4.jpeg", "Liquidación de Sociedad Conyugal", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Tercera fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "matrimonio_divorcio _y_Liquidacion_de_Sociedad_Conyugal/5.jpeg", "Declaración de Unión Marital de Hecho", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "matrimonio_divorcio _y_Liquidacion_de_Sociedad_Conyugal/6.jpeg", "Capitulaciones Matrimoniales", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Cuarta fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "matrimonio_divorcio _y_Liquidacion_de_Sociedad_Conyugal/7.jpeg", "Separación de Bienes", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Botón "Ver Más"
                ft.Container(
                    alignment=ft.alignment.top_right,
                    content=ft.TextButton(
                        text="Ver Más", on_click=lambda e: print("Ver Más")
                    ),
                ),
            ]
        )
    )


def declaraciones_juramentadas_content():
    return ft.Container(
        padding=ft.padding.all(5),
        content=ft.Column(
            controls=[
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Declaraciones_Juramentadas/1.jpeg", "Declaración Juramentada de Ingresos", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Declaraciones_Juramentadas/2.jpeg", "Declaración Juramentada de Bienes", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Segunda fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Declaraciones_Juramentadas/3.jpeg", "Declaración Juramentada de No Poseer Vivienda", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Declaraciones_Juramentadas/4.jpeg", "Declaración Juramentada de No Tener Vivienda Propia", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Tercera fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Declaraciones_Juramentadas/5.jpeg", "Declaración Juramentada de No Tener Vivienda Familiar", "1000", "/registro-civil"
                            ),
                        ),
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Declaraciones_Juramentadas/6.jpeg", "Declaración Juramentada de No Tener Vivienda Familiar", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Cuarta fila
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Container(
                            width="calc(50% - 10px)",
                            content=create_content(
                                "Declaraciones_Juramentadas/7.jpeg", "Declaración Juramentada de No Tener Vivienda Familiar", "1000", "/registro-civil"
                            ),
                        ),
                    ]
                ),
                # Botón "Ver Más"
                ft.Container(
                    alignment=ft.alignment.top_right,
                    content=ft.TextButton(
                        text="Ver Más", on_click=lambda e: print("Ver Más")
                    ),
                ),
            ]
        )
    )
    


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
