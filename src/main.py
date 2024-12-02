import flet as ft
from pages.utils.json import json_base64
import threading
def main(page: ft.Page):
    page.adaptive = True
    page.window.always_on_top = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    page.padding = ft.padding.all(0)
    # page.session.set("api_url", "https://inventario.ciempanorte.com")

    def home():
        def open_dlg(e, text):
          def show_loader():
              if not e.control.page.overlay:  # Verifica si no hay otros elementos en el overlay
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
              if e.control.page.overlay:  # Verifica si hay elementos en el overlay antes de eliminarlos
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
                expand=True,
                width=180,
                height=280,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Image(
                                src=image,
                                width=100,
                                height=100,

                            ),
                            border_radius=ft.border_radius.all(
                                40),
                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
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
                        ft.ElevatedButton(
                            "Agregar al Carrito", icon=ft.Icons.ADD_SHOPPING_CART, bgcolor="#FFBC03", color=ft.Colors.BLACK,
                            on_click=lambda e: open_dlg(e, f"Agregado al carrito {name}"),),

                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                ),
                padding=ft.padding.all(10),
                border_radius=ft.border_radius.all(10),
                bgcolor=ft.Colors.WHITE,

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
                                  src_base64=json_base64("lottie/Facebook.json"),
                                  ),
                              width=40,
                              height=40,
                              on_click=lambda e: open_dlg(e, "Proximamente en Facebook"),
                          ),
                          ft.VerticalDivider(thickness=3),
                          ft.Container(
                              content=ft.Lottie(
                                  src_base64=json_base64("lottie/Instagram.json"),
                                  ),
                              width=40,
                              height=40,
                              on_click=lambda e: open_dlg(e, "Proximamente en Instagram"),
                          ),
                          ft.VerticalDivider(thickness=3),
                          ft.Container(
                              content=ft.Lottie(
                                  src_base64=json_base64("lottie/Youtube.json"),
                                  ),
                              width=40,
                              height=40,
                              on_click=lambda e: open_dlg(e, "Proximamente en Youtube"),
                          )
                      ]
                  )
              ]
          )
        nav_bar = ft.AppBar(
            bgcolor="#005B7A",
        )
        page.appbar  = nav_bar
        page.navigation_bar = ft.NavigationBar(
            bgcolor=ft.Colors.WHITE,
            elevation=0,
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icons.HOME,),
                ft.NavigationBarDestination(
                    icon=ft.Icons.MAN_2_OUTLINED),
                ft.NavigationBarDestination(
                    icon=ft.Icons.ADD_SHOPPING_CART_OUTLINED,
                    selected_icon=ft.Icons.ADD_SHOPPING_CART,
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.MENU_ROUNDED,
                    selected_icon=ft.Icons.MENU,
                    
                ),
            ]
        )
        container = ft.Container(
            padding=ft.padding.all(0),
            content=ft.Column(
                scroll=ft.ScrollMode.HIDDEN,
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
                            spacing=0,
                            controls=[
                                ft.Text("Registro Civil", size=24,
                                        weight=ft.FontWeight.W_600),
                                ft.Container(
                                    bgcolor="#51B2C2",
                                    padding=ft.padding.all(10),
                                    content=ft.Row(
                                        scroll=ft.ScrollMode.AUTO,
                                        controls=[
                                            create_content(
                                                "registro_civil/1.png", "Copia de Registro civil de Nacimiento", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Copia de Registro civil de Matrimonio", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Domicilio registro civil para recien nacidos", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Copia de Registro civil de Defunción", "1000", "/registro-civil"),

                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                                ft.Container(
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
                                    bgcolor="#51B2C2",
                                    padding=ft.padding.all(10),
                                    content=ft.Row(
                                        scroll=ft.ScrollMode.AUTO,
                                        controls=[
                                            create_content(
                                                "registro_civil/1.png", "Autenticación de Firma ", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Autenticación de Copias ", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Reconocimiento de firma y contenido", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", " Firma a Ruego - Personas que no saben o no puede firmar", "1000", "/registro-civil"),

                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                                ft.Container(
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
                                    bgcolor="#51B2C2",
                                    padding=ft.padding.all(10),
                                    content=ft.Row(
                                        scroll=ft.ScrollMode.AUTO,
                                        controls=[
                                            create_content(
                                                "registro_civil/1.png", "Copia autenticada de escritura", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Copia simple de escritura", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Copia electronica de escritura", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Copia testimonial notarial de escritura", "1000", "/registro-civil"),

                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                                ft.Container(
                                    bgcolor="#51B2C2",
                                    padding=ft.padding.all(10),
                                    content=ft.Row(
                                        scroll=ft.ScrollMode.AUTO,
                                        controls=[
                                            create_content(
                                                "registro_civil/1.png", "Copia de extracto de escritura", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Haz tu minuta de escritura con IA", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Haz tu poder en minutos con IA", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Cambio de Nombre", "1000", "/registro-civil"),

                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                                ft.Container(
                                    bgcolor="#51B2C2",
                                    padding=ft.padding.all(10),
                                    content=ft.Row(
                                        scroll=ft.ScrollMode.AUTO,
                                        controls=[
                                            create_content(
                                                "registro_civil/1.png", "Haz tu testamento con IA ", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Afectación a Vivienda familiar", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Patrimonio de familia inembargable", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Compraventa de inmuebles", "1000", "/registro-civil"),

                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                                ft.Container(
                                    bgcolor="#51B2C2",
                                    padding=ft.padding.all(10),
                                    content=ft.Row(
                                        scroll=ft.ScrollMode.AUTO,
                                        controls=[
                                            create_content(
                                                "registro_civil/1.png", "Cancelación de Hipoteca", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Permuta de Inmuebles", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Donación", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Constitución de hipoteca", "1000", "/registro-civil"),

                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                                ft.Container(
                                    bgcolor="#51B2C2",
                                    padding=ft.padding.all(10),
                                    content=ft.Row(
                                        scroll=ft.ScrollMode.AUTO,
                                        controls=[
                                            create_content(
                                                "registro_civil/1.png", "Sucesión de bienes por causa de muerte", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Corrección Componente de Identidad Sexual", "1000", "/registro-civil"),
                                            
                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                                ft.Container(
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
                                    bgcolor="#51B2C2",
                                    padding=ft.padding.all(10),
                                    content=ft.Row(
                                        scroll=ft.ScrollMode.AUTO,
                                        controls=[
                                            create_content(
                                                "registro_civil/1.png", "Matrimonio a Domicilio", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Escoje tu fecha de matrimonio en notaria", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Divorcio", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Liquidacion de Sociedad Conyugal", "1000", "/registro-civil"),

                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                                ft.Container(
                                    bgcolor="#51B2C2",
                                    padding=ft.padding.all(10),
                                    content=ft.Row(
                                        scroll=ft.ScrollMode.AUTO,
                                        controls=[
                                            create_content(
                                                "registro_civil/1.png", "Declaración de Unión Marital de Hecho", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Capitulaciones Matrimoniales", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Separación de Bienes", "1000", "/registro-civil"),

                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                                ft.Container(
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
                                    bgcolor="#51B2C2",
                                    padding=ft.padding.all(10),
                                    content=ft.Row(
                                        scroll=ft.ScrollMode.AUTO,
                                        controls=[
                                            create_content(
                                                "registro_civil/1.png", "Declaraciones Juramentadas", "1000", "/registro-civil"),
                                            create_content(
                                                "documento.png", "Declaraciones Juramentadas con IA", "1000", "/registro-civil"),
                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                                ft.Container(
                                    content=ft.TextButton(
                                        text="Ver Mas", on_click=lambda e: print("Ver")),
                                )
                            ])),

                ]
            )
        )
        page.add(ft.SafeArea(content=container, expand=True))
        page.update()

    home()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
