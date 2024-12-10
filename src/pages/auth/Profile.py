from pages.utils.inputs import create_input_field, create_dropdown_field
from pages.utils.alert import show_construction_dialog
from pages.utils.navigation import create_footer
import flet as ft
import datetime


def ViewProfile(page):
    page.controls.clear()
    page.navigation_bar = create_footer(page)
    name_field = create_input_field("Nombres")
    last_name_field = create_input_field("Apellidos")
    document_field = create_input_field("Número de Identificación")
    email_field = create_input_field("E-mail")
    phone_field = create_input_field("Celular")
    register_number_field = create_input_field("Número de Registro Civil")
    city_field = create_input_field("Ciudad expedición")
    deparment_field = create_input_field("Departamento")
    notaria_registraduria = create_input_field("Notaría, Número o Registraduría")
    direccion = create_input_field("Dirección")
    ciudad = create_input_field("Ciudad")
    estado_provincia = create_input_field("Estado/Provincia")
    zip = create_input_field("Código Postal")
    pais = create_dropdown_field(
            "País", options=["Colombia", "Ecuador", "Perú", "Otro"])
    def on_date_change(e):
        selected_date = e.control.value.strftime("%Y-%m-%d")
        birth_date_field.value = selected_date
        page.update()

    birth_date_field = ft.TextField(
        border_radius=ft.border_radius.all(15),
        content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
        bgcolor=ft.Colors.WHITE,
        border_color="#717171",
        label_style=ft.TextStyle(color="#717171"),
        border_width=0.5,
        value="",
        expand=True,
    )

    container = ft.Column(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
        spacing=0,
        controls=[
            ft.Container(
                padding=ft.padding.all(20),
                expand=True,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        ft.Column(
                            expand=True,
                            scroll=ft.ScrollMode.HIDDEN,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                            spacing=5,
                            controls=[
                                ft.Container(height=5),
                                ft.Text("Mi Perfil", text_align="left", size=20, weight="bold"),
                                ft.Container(height=5),

                                name_field,
                                last_name_field,
                                document_field,
                                email_field,
                                phone_field,
                                ft.Column(
                                    controls=[
                                        ft.Text("Fecha de Nacimiento", style=ft.TextStyle(color="#717171")),
                                        ft.Row(
                                            controls=[
                                                birth_date_field,
                                                ft.IconButton(
                                                    icon=ft.Icons.CALENDAR_MONTH,
                                                    icon_color="blue",
                                                    on_click=lambda e: page.open(
                                                        ft.DatePicker(
                                                            first_date=datetime.datetime(year=2023, month=10, day=1),
                                                            last_date=datetime.datetime(year=2024, month=10, day=1),
                                                            on_change=on_date_change,
                                                        )
                                                    ),
                                                ),
                                            ],
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                    ],
                                    spacing=10,
                                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                                ),
                                ft.Container(height=5),
                                ft.Text("Ubicacion", text_align="left", size=20, weight="bold"),
                                direccion,
                                ciudad,
                                estado_provincia,
                                zip,
                                pais,
                                ft.Container(height=5),
                                ft.Text("Para más DocuFlow", text_align="left", size=20, weight="bold"),
                                register_number_field,
                                city_field,
                                deparment_field,
                                notaria_registraduria,
                            ]
                        ),
                        ft.Container(
                            alignment=ft.alignment.center,
                            # on_click=handle_login_click,
                            ink=True,
                            border_radius=ft.border_radius.all(35),
                            width=350,
                            height=40,
                            bgcolor="#25D366",
                            content=ft.Text(
                                "Guardar", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            padding=ft.padding.all(10),
                        ),
                    ]
                )
            )
        ]
    )

    return container
