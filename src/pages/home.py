import flet as ft
from pages.utils.navigation import create_footer
from threading import Timer
from fletcarousel import BasicAnimatedHorizontalCarousel, HintLine, AutoCycle
from pages.utils.navigation import create_navbar_home
def ViewHome(page):
    page.controls.clear()
    page.appbar = create_navbar_home(page)
    page.navigation_bar = create_footer(page)

    def create_carousel(page):
        return BasicAnimatedHorizontalCarousel(
            page=page,
            auto_cycle=AutoCycle(duration=5),
            expand=True,
            padding=0,
            hint_lines=HintLine(
                active_color="red",
                inactive_color="gray",
                alignment=ft.MainAxisAlignment.CENTER,
                max_list_size=400,
                size=4,
            ),
            items=[
                ft.Container(
                    content=ft.Image(
                        src=f"banner/{i}.png",
                        fit=ft.ImageFit.COVER,
                    ),
                    height=200,
                    expand=True,
                    width=page.window.width,
                    bgcolor="white",
                    border_radius=15,
                    alignment=ft.alignment.center,
                )
                for i in range(1, 4)
            ],
        )

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
            container = tab.tab_content
            column = container.content
            text = column.controls[0]

            if i == selected_index:
                container.bgcolor = "#e5bc16"
                text.color = ft.Colors.WHITE
            else:
                container.bgcolor = None
                text.color = ft.Colors.BLACK

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
                            on_click=lambda e: print("Clickable without Ink clicked!"),
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
    
