
import flet as ft
from pages.utils.controls.inputs import MyInputField
from pages.utils.navigation import create_footer, create_navbar_product
from pages.utils.state import departamentos_data
from pages.utils.controls.Fecha import DatePickerField
import datetime


def ViewRegistroCivil(page):
    page.controls.clear()
    page.appbar = create_navbar_product(page)[0]
    page.navigation_bar = create_footer(page)

    name_field = MyInputField(
        "Nombres y apellidos completos del titular del registro")
    document_field = MyInputField("Número de Identificación del titular")
    number_serial_field = MyInputField(
        "Número de serial del registro civil, si está disponible")

    departamentos = departamentos_data["departamentos"]
    department_dropdown = ft.Dropdown(
        border_radius=ft.border_radius.all(15),
        content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
        bgcolor=ft.Colors.WHITE,
        border_color="#717171",
        label_style=ft.TextStyle(color="#717171"),
        border_width=0.5,
        options=[ft.dropdown.Option(dept["nombre"]) for dept in departamentos],
        on_change=lambda e: update_cities(e),
    )

    city_dropdown = ft.Dropdown(
        border_radius=ft.border_radius.all(15),
        content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
        bgcolor=ft.Colors.WHITE,
        border_color="#717171",
        label_style=ft.TextStyle(color="#717171"),
        border_width=0.5,
        options=[],
    )

    def update_cities(e):
        selected_department = e.control.value
        for dept in departamentos:
            if dept["nombre"] == selected_department:
                city_dropdown.options = [ft.dropdown.Option(
                    city) for city in dept["ciudades"]]
                city_dropdown.value = None
                page.update()
                break

    today = datetime.datetime.now()
    birth_date_field = DatePickerField(
        name="Fecha de Nacimiento del titular",
        first_date=datetime.datetime(year=1900, month=1, day=1),
        last_date=today,
    )

    def validate_and_confirm(e):
        if not name_field.controls[1].value.strip():
            ft.dialog.AlertDialog(
                "El campo Nombres y Apellidos es obligatorio").open()
        elif not document_field.controls[1].value.strip():
            ft.dialog.AlertDialog(
                "El campo Número de Identificación del titular es obligatorio").open()
        elif not number_serial_field.controls[1].value.strip():
            ft.dialog.AlertDialog(
                "El campo Número de Serial de Registro es obligatorio").open()
        elif not department_dropdown.value:
            ft.dialog.AlertDialog("Debe seleccionar un Departamento").open()
        elif not city_dropdown.value:
            ft.dialog.AlertDialog("Debe seleccionar una Ciudad").open()
        elif not birth_date_field.value.strip():
            ft.dialog.AlertDialog(
                "Debe seleccionar una Fecha de Nacimiento").open()
        else:
            show_confirmation_dialog()

    def show_confirmation_dialog():
        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar Guardado"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Nombres y Apellidos: {
                            name_field.controls[1].value}"),
                    ft.Text(f"Número de Identificación: {
                            document_field.controls[1].value}"),
                    ft.Text(f"Serial de Registro: {
                            number_serial_field.controls[1].value}"),
                    ft.Text(f"Departamento: {department_dropdown.value}"),
                    ft.Text(f"Ciudad: {city_dropdown.value}"),
                    ft.Text(f"Fecha de Nacimiento: {birth_date_field.value}"),
                    ft.Row(
                        controls=[
                            ft.Button(
                                "Cancelar", on_click=lambda e: close_dialog(dlg)),
                            ft.Button(
                                "Guardar", on_click=lambda e: save_data(dlg)),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=10,
                    )
                ],
                spacing=10,
            ),
        )
        if page.overlay:
            page.overlay.pop()
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def save_data(dlg):
        close_dialog(dlg)
        page.go("/checkout")

    def close_dialog(dlg):
        dlg.open = False
        page.update()

    save_button = ft.Container(
        alignment=ft.alignment.center,
        on_click=validate_and_confirm,
        ink=True,
        border_radius=ft.border_radius.all(35),
        width=350,
        height=40,
        bgcolor="#25D366",
        content=ft.Text("Guardar", size=15, color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD),
        padding=ft.padding.all(10),
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
                                ft.Text("Datos del Registro Civil Titular",
                                        text_align="left", size=20, weight="bold"),
                                ft.Container(height=5),
                                name_field,
                                birth_date_field,
                                document_field,
                                number_serial_field,
                                ft.Column(
                                    controls=[
                                        ft.Text("Departamento de Expedición",
                                                style=ft.TextStyle(color="#717171")),
                                        department_dropdown,
                                    ]
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Ciudad de Expedición", style=ft.TextStyle(
                                            color="#717171")),
                                        city_dropdown,
                                    ]
                                ),
                            ],
                        ),
                        save_button,
                    ],
                ),
            )
        ],
    )
    return container
