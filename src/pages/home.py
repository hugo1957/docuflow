import flet as ft
import threading
import json
from pages.utils.json import json_base64
from pages.utils.navigation import create_footer
def ViewHome(page):
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

          # Start loading dialog in another thread
          threading.Thread(target=load_dialog).start()
          # Show loader if dialog loading takes longer than 0.5 seconds
          threading.Timer(0.5, show_loader).start()

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

        def redes_sociales():
            return ft.Column(
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
                                    src_base64=json_base64(
                                        "lottie/Facebook.json"),
                                ),
                                width=40,
                                height=40,
                                on_click=lambda e: open_dlg(
                                    e, "Proximamente en Facebook"),
                            ),
                            ft.VerticalDivider(thickness=3),
                            ft.Container(
                                content=ft.Lottie(
                                    src_base64=json_base64(
                                        "lottie/Instagram.json"),
                                ),
                                width=40,
                                height=40,
                                on_click=lambda e: open_dlg(
                                    e, "Proximamente en Instagram"),
                            ),
                            ft.VerticalDivider(thickness=3),
                            ft.Container(
                                content=ft.Lottie(
                                    src_base64=json_base64(
                                        "lottie/Youtube.json"),
                                ),
                                width=40,
                                height=40,
                                on_click=lambda e: open_dlg(
                                    e, "Proximamente en Youtube"),
                            )
                        ]
                    )
                ]
            )

        nav_bar = ft.AppBar(
            bgcolor="#005B7A",
        )
        page.appbar = nav_bar
        page.navigation_bar = create_footer(page)
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
                                bgcolor="#3D82B1",
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
                                            ft.Icons.SEARCH_SHARP,
                                            color=ft.Colors.BLACK,
                                            size=30,
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
                            ft.Container(
                                bgcolor="#D94D00",
                                width="100%",
                                height=170,
                                content=ft.Row(
                                    alignment="center",
                                    controls=[
                                      ft.Column(

                                          controls=[
                                              ft.Text("Compra", color=ft.Colors.WHITE,
                                                      size=40, weight=ft.FontWeight.W_700),
                                              ft.Text("del dia", color=ft.Colors.WHITE,
                                                      size=40, weight=ft.FontWeight.W_700),
                                          ]
                                      ),
                                        ft.Column(
                                          controls=[
                                              ft.Text("ofertas", color=ft.Colors.WHITE,
                                                      size=40, weight=ft.FontWeight.W_700),
                                              ft.Image(src="documento.png",
                                                       width=100, height=100),
                                          ]
                                      ),
                                    ]
                                )
                            ),
                            ft.Container(
                                content=ft.Column(
                                    spacing=5,
                                    controls=[
                                        ft.Text("Registro Civil", size=24,
                                                weight=ft.FontWeight.W_600),
                                        ft.Container(


                                            content=ft.Row(
                                                spacing=5,
                                                scroll=ft.ScrollMode.HIDDEN,
                                                controls=[
                                                    create_content(
                                                        "registro_civil/1.jpg", "Copia de Registro civil de Nacimiento", "1000", "/registro-civil"),
                                                    create_content(
                                                        "registro_civil/2.jpeg", "Copia de Registro civil de Matrimonio", "1000", "/registro-civil"),
                                                    create_content(
                                                        "registro_civil/3.jpeg", "Domicilio registro civil para recien nacidos", "1000", "/registro-civil"),
                                                    create_content(
                                                        "registro_civil/4.jpeg", "Copia de Registro civil de Defunción", "1000", "/registro-civil"),

                                                ],
                                                alignment=ft.MainAxisAlignment.START,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                        ),
                                        ft.Container(
                                            alignment=ft.alignment.top_right,
                                            content=ft.TextButton(
                                                text="Ver Mas", on_click=lambda e: print("Ver")),
                                        )
                                    ])),
                            ft.Container(
                                content=ft.Column(
                                    spacing=0,
                                    controls=[
                                        ft.Text("Autenticacion", size=24,
                                                weight=ft.FontWeight.W_600),
                                        ft.Container(

                                            padding=ft.padding.all(5),
                                            content=ft.Row(
                                                spacing=5,
                                                scroll=ft.ScrollMode.AUTO,
                                                controls=[
                                                    create_content(
                                                        "Autenticacion/1.jpeg", "Autenticación de Firma ", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Autenticacion/2.jpeg", "Autenticación de Copias ", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Autenticacion/3.jpeg", "Reconocimiento de firma y contenido", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Autenticacion/4.jpeg", " Firma a Ruego - Personas que no saben o no puede firmar", "1000", "/registro-civil"),

                                                ],
                                                alignment=ft.MainAxisAlignment.START,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                        ),
                                        ft.Container(
                                            alignment=ft.alignment.top_right,
                                            content=ft.TextButton(
                                                text="Ver Mas", on_click=lambda e: print("Ver")),
                                        )
                                    ])),
                            ft.Container(
                                content=ft.Column(
                                    spacing=0,
                                    controls=[
                                        ft.Text("Escrituras", size=24,
                                                weight=ft.FontWeight.W_600),
                                        ft.Container(

                                            padding=ft.padding.all(5),
                                            content=ft.Row(
                                                scroll=ft.ScrollMode.AUTO,
                                                spacing=5,
                                                controls=[
                                                    create_content(
                                                        "Escritura/1.jpeg", "Copia autenticada de escritura", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Escritura/2.jpeg", "Copia simple de escritura", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Escritura/3.jpeg", "Copia electronica de escritura", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Escritura/4.jpeg", "Copia testimonial notarial de escritura", "1000", "/registro-civil"),

                                                ],
                                                alignment=ft.MainAxisAlignment.START,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                        ),
                                        ft.Container(

                                            padding=ft.padding.all(5),
                                            content=ft.Row(
                                                spacing=5,
                                                scroll=ft.ScrollMode.AUTO,
                                                controls=[
                                                    create_content(
                                                        "Escritura/5.jpeg", "Copia de extracto de escritura", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Escritura/6.jpeg", "Haz tu minuta de escritura con IA", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Escritura/7.jpeg", "Haz tu poder en minutos con IA", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Escritura/8.jpeg", "Cambio de Nombre", "1000", "/registro-civil"),

                                                ],
                                                alignment=ft.MainAxisAlignment.START,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                        ),
                                        ft.Container(

                                            padding=ft.padding.all(5),
                                            content=ft.Row(
                                                spacing=5,
                                                scroll=ft.ScrollMode.AUTO,
                                                controls=[
                                                    create_content(
                                                        "Escritura/9.jpeg", "Haz tu testamento con IA ", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Escritura/10.jpeg", "Afectación a Vivienda familiar", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Escritura/11.jpeg", "Patrimonio de familia inembargable", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Escritura/12.jpeg", "Compraventa de inmuebles", "1000", "/registro-civil"),

                                                ],
                                                alignment=ft.MainAxisAlignment.START,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                        ),
                                        ft.Container(

                                            padding=ft.padding.all(5),
                                            content=ft.Row(
                                                scroll=ft.ScrollMode.AUTO,
                                                controls=[
                                                    create_content(
                                                        "Escritura/13.jpeg", "Cancelación de Hipoteca", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Escritura/14.jpeg", "Permuta de Inmuebles", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Escritura/15.jpeg", "Donación", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Escritura/16.jpeg", "Constitución de hipoteca", "1000", "/registro-civil"),

                                                ],
                                                alignment=ft.MainAxisAlignment.START,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                        ),
                                        ft.Container(

                                            padding=ft.padding.all(5),
                                            content=ft.Row(
                                                spacing=5,
                                                scroll=ft.ScrollMode.AUTO,
                                                controls=[
                                                    create_content(
                                                        "Escritura/17.jpeg", "Sucesión de bienes por causa de muerte", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Escritura/18.jpeg", "Corrección Componente de Identidad Sexual", "1000", "/registro-civil"),

                                                ],
                                                alignment=ft.MainAxisAlignment.START,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                        ),
                                        ft.Container(
                                            alignment=ft.alignment.top_right,
                                            content=ft.TextButton(
                                                text="Ver Mas", on_click=lambda e: print("Ver")),
                                        )
                                    ])),
                            ft.Container(
                                content=ft.Column(
                                    spacing=0,
                                    controls=[
                                        ft.Text("Matrimonio,Divorcio y Liquidacion de Sociedad Conyugal", size=24,
                                                weight=ft.FontWeight.W_600),
                                        ft.Container(

                                            padding=ft.padding.all(5),
                                            content=ft.Row(
                                                scroll=ft.ScrollMode.AUTO,
                                                spacing=5,
                                                controls=[
                                                    create_content(
                                                        "matrimonio_divorcio _y_Liquidacion_de_Sociedad_Conyugal/1.jpeg", "Matrimonio a Domicilio", "1000", "/registro-civil"),
                                                    create_content(
                                                        "matrimonio_divorcio _y_Liquidacion_de_Sociedad_Conyugal/2.jpeg", "Escoje tu fecha de matrimonio en notaria", "1000", "/registro-civil"),
                                                    create_content(
                                                        "matrimonio_divorcio _y_Liquidacion_de_Sociedad_Conyugal/3.jpeg", "Divorcio", "1000", "/registro-civil"),
                                                    create_content(
                                                        "matrimonio_divorcio _y_Liquidacion_de_Sociedad_Conyugal/4.jpeg", "Liquidacion de Sociedad Conyugal", "1000", "/registro-civil"),

                                                ],
                                                alignment=ft.MainAxisAlignment.START,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                        ),
                                        ft.Container(

                                            padding=ft.padding.all(5),
                                            content=ft.Row(
                                                spacing=5,
                                                scroll=ft.ScrollMode.AUTO,
                                                controls=[
                                                    create_content(
                                                        "matrimonio_divorcio _y_Liquidacion_de_Sociedad_Conyugal/5.jpeg", "Declaración de Unión Marital de Hecho", "1000", "/registro-civil"),
                                                    create_content(
                                                        "matrimonio_divorcio _y_Liquidacion_de_Sociedad_Conyugal/6.jpeg", "Capitulaciones Matrimoniales", "1000", "/registro-civil"),
                                                    create_content(
                                                        "matrimonio_divorcio _y_Liquidacion_de_Sociedad_Conyugal/7.jpeg", "Separación de Bienes", "1000", "/registro-civil"),

                                                ],
                                                alignment=ft.MainAxisAlignment.START,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                        ),
                                        ft.Container(
                                            alignment=ft.alignment.top_right,
                                            content=ft.TextButton(
                                                text="Ver Mas", on_click=lambda e: print("Ver")),
                                        )
                                    ])),
                            ft.Container(
                                content=ft.Column(
                                    spacing=0,
                                    controls=[
                                        ft.Text("Declaraciones Juramentadas", size=24,
                                                weight=ft.FontWeight.W_600),
                                        ft.Container(

                                            padding=ft.padding.all(5),
                                            content=ft.Row(
                                                spacing=5,
                                                scroll=ft.ScrollMode.AUTO,
                                                controls=[
                                                    create_content(
                                                        "Declaraciones_juramentas/1.jpeg", "Declaraciones Juramentadas", "1000", "/registro-civil"),
                                                    create_content(
                                                        "Declaraciones_juramentas/2.jpeg", "Declaraciones Juramentadas con IA", "1000", "/registro-civil"),
                                                ],
                                                alignment=ft.MainAxisAlignment.START,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                        ),
                                        ft.Container(
                                            alignment=ft.alignment.top_right,
                                            content=ft.TextButton(
                                                text="Ver Mas", on_click=lambda e: print("Ver")),
                                        )
                                    ])),

                        ]
                    )
                ]
            )
        )
        return container