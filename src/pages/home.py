import flet as ft
import threading
import json
from pages.utils.json import json_base64
from pages.utils.navigation import create_footer
from threading import Timer


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
                    width="100%",
                    height="100%",
                    fit=ft.ImageFit.CONTAIN,  # Ocupa todo el contenedor
                ),
                width="100%",
                height=200,
                border_radius=ft.border_radius.all(15),  # Bordes redondeados
                clip_behavior=ft.ClipBehavior.HARD_EDGE,  # Recorta contenido fuera de bordes
            ),
            duration=500,  # Duración de la animación (ms)
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

                    fit=ft.ImageFit.COVER,  # Ocupa todo el contenedor
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

            Timer(4.0, auto_update).start()  # Cambia la imagen cada 2 segundos

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

        carousel = ft.Container(
            width=page.window.width,
            content=ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=page.window.width,
                        height=200,
                        content=animated_image,  # Imagen animada
                    ),
                    ft.Container(
                        alignment=ft.alignment.center,
                        padding=ft.padding.symmetric(vertical=10),
                        content=dots,  # Puntos centrados
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
            registro_civil_content(),
            autenticacion_content(),
            escrituras_content(),
            matrimonio_divorcio_content(),

            declaraciones_juramentadas_content(),
        ]
        return contents[index]

    def update_tab_content(e):
        selected_tab = e.control.selected_index
        dynamic_content.content = create_tab_content(selected_tab)
        dynamic_content.update()

    tabs = ft.Tabs(
        selected_index=0,
        on_change=update_tab_content,
        indicator_color=ft.colors.TRANSPARENT,
        indicator_border_radius=ft.border_radius.all(10),
        label_color="#e5bc16",
        scrollable=True,
        tabs=[
            ft.Tab(
                tab_content=ft.Column(
                    controls=[
                        ft.Text("Registro Civil", size=15),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ),
            ft.Tab(
                tab_content=ft.Column(
                    controls=[
                        ft.Text("Autenticación", size=15),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ),
            ft.Tab(
                tab_content=ft.Column(
                    controls=[
                        ft.Text("Escrituras", size=15),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ),
            ft.Tab(
                tab_content=ft.Column(
                    controls=[
                        ft.Text("Matrimonio y Divorcio", size=15),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ),
            ft.Tab(
                tab_content=ft.Column(
                    controls=[
                        ft.Text("Declaraciones", size=15),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
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


def create_content(image, name, valor, url):
    return ft.Container(
        width=180,
        height=260,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    padding=ft.padding.all(0),
                    alignment=ft.alignment.top_right,
                    content=ft.IconButton(
                        icon=ft.Icons.SHOPPING_CART_OUTLINED,
                        icon_color="#FFBC03",
                        icon_size=20,
                        tooltip="Agregar al carrito",

                    ),
                ),
                ft.Container(
                    expand=True,
                    padding=ft.padding.all(0),
                    border_radius=ft.border_radius.all(100),
                    content=ft.Image(
                        src=image,
                        width=120,
                        height=120,
                    ),
                ),
                ft.Text(
                    name,
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                ),
                ft.Text(
                    f"Valor: {valor}",
                    size=12,
                    color=ft.Colors.BLACK54,
                ),
            ],
        ),
        padding=ft.padding.all(10),
        border_radius=ft.border_radius.all(10),
        bgcolor=ft.Colors.BLUE,
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
    
