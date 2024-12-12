import flet as ft
from pages.utils.controls.inputs import MyInputField
from pages.utils.navigation import create_footer, create_navbar_product
from pages.utils.state import departamentos_data
from pages.utils.controls.dropdownFlag import CountryDropdown
from pages.utils.controls.Fecha import DatePickerField 
import datetime
def ViewRegistroMenores(page):
    page.controls.clear()
    page.appbar = create_navbar_product(page)[0]
    page.navigation_bar = create_footer(page)

    # Campos principales
    name_field = MyInputField("Nombres y Apellidos del Menor")
    document_field = MyInputField("Número de Identificación del Menor")
    birth_certificate_field = MyInputField("Registro Civil de Nacimiento")
    passport_field = MyInputField("Número de Pasaporte (si aplica)")
    destination_field = CountryDropdown(on_country_change=None)
    purpose_field = MyInputField("Propósito del Viaje")

    today = datetime.datetime.now()
    birth_date_field = DatePickerField(
        name="Fecha de Nacimiento del Menor",
        first_date=datetime.datetime(year=1900, month=1, day=1),
        last_date=today,
    )
    departure_date_field = DatePickerField(
        name="Fecha de Salida",
        first_date=today,
        on_change=lambda value: return_date_field.set_limits(
            first_date=datetime.datetime.strptime(value, "%Y-%m-%d")
        ),
    )
    return_date_field = DatePickerField(
        name="Fecha de Regreso",
        first_date=today,
    )

    # Información del padre
    father_name_field = MyInputField("Nombre del Padre")
    father_id_field = MyInputField("Número de Identificación del Padre")
    father_phone_field = MyInputField("Teléfono del Padre")

    is_father_deceased = ft.Checkbox(label="¿Padre fallecido?")
    father_death_fields = ft.Column(
        visible=False,
        controls=[
            MyInputField("Registro Civil de Defunción del Padre"),
        ],
    )

    # Información de la madre
    mother_name_field = MyInputField("Nombre de la Madre")
    mother_id_field = MyInputField("Número de Identificación de la Madre")
    mother_phone_field = MyInputField("Teléfono de la Madre")

    is_mother_deceased = ft.Checkbox(label="¿Madre fallecida?")
    mother_death_fields = ft.Column(
        visible=False,
        controls=[
            MyInputField("Registro Civil de Defunción de la Madre"),
        ],
    )

    def toggle_field_visibility(e, field_type):
        if field_type == "father":
            father_death_fields.visible = is_father_deceased.value
        elif field_type == "mother":
            mother_death_fields.visible = is_mother_deceased.value
        page.update()

    is_father_deceased.on_change = lambda e: toggle_field_visibility(e, "father")
    is_mother_deceased.on_change = lambda e: toggle_field_visibility(e, "mother")

    # Dropdowns de departamentos y ciudades
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
                city_dropdown.options = [ft.dropdown.Option(city) for city in dept["ciudades"]]
                city_dropdown.value = None
                page.update()
                break

    # Validación y confirmación
    def validate_and_confirm(e):
        errors = []
        required_fields = [
            (name_field, "Nombres y Apellidos del Menor"),
            (document_field, "Número de Identificación del Menor"),
            (birth_certificate_field, "Registro Civil de Nacimiento"),
            (destination_field, "Lugar de Destino del Viaje"),
            (purpose_field, "Propósito del Viaje"),
            (father_name_field, "Nombre del Padre"),
            (father_id_field, "Número de Identificación del Padre"),
            (father_phone_field, "Teléfono del Padre"),
            (mother_name_field, "Nombre de la Madre"),
            (mother_id_field, "Número de Identificación de la Madre"),
            (mother_phone_field, "Teléfono de la Madre"),
        ]

        # Validar campos de texto
        for field, name in required_fields:
            if not field.controls[1].value.strip():
                errors.append(f"El campo '{name}' es obligatorio.")

        # Validar campos de fecha
        if not departure_date_field.value:
            errors.append("Debe seleccionar la Fecha de Salida.")
        if not return_date_field.value:
            errors.append("Debe seleccionar la Fecha de Regreso.")
        if not birth_date_field.value:
            errors.append("Debe seleccionar la Fecha de Nacimiento del Menor.")

        # Validar fallecimiento
        if is_father_deceased.value and not father_death_fields.controls[0].controls[1].value.strip():
            errors.append("Debe proporcionar el 'Registro Civil de Defunción del Padre' si ha fallecido.")
        if is_mother_deceased.value and not mother_death_fields.controls[0].controls[1].value.strip():
            errors.append("Debe proporcionar el 'Registro Civil de Defunción de la Madre' si ha fallecido.")
        if not department_dropdown.value:
            errors.append("Debe seleccionar un Departamento.")
        if not city_dropdown.value:
            errors.append("Debe seleccionar una Ciudad.")

        if errors:
            dlg = ft.AlertDialog(
                title=ft.Text("Errores de Validación"),
                content=ft.Text("\n".join(errors)),
            )
            dlg.open = True
            page.overlay.append(dlg)
            page.update()
        else:
            show_confirmation_dialog()

    def show_confirmation_dialog():
        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar Datos"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Nombres del Menor: {name_field.controls[1].value}"),
                    ft.Text(f"Documento del Menor: {document_field.controls[1].value}"),
                    ft.Text(f"Fecha de Nacimiento: {birth_date_field.value}"),
                    ft.Text(f"Fecha de Salida: {departure_date_field.value}"),
                    ft.Text(f"Fecha de Regreso: {return_date_field.value}"),
                    # Agregar más campos relevantes aquí
                ],
                spacing=10,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: close_dialog(dlg)),
                ft.TextButton("Confirmar", on_click=lambda _: save_data(dlg)),
            ],
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def save_data(dlg):
        dlg.open = False
        page.go("/solicitud_guardada")

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
        content=ft.Text("Guardar Solicitud", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        padding=ft.padding.all(10),
    )

    container = ft.Column(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
        spacing=0,
        controls=[
            ft.Text("Registro de Permiso de Salida", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(
                padding=ft.padding.all(20),
                expand=True,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    scroll=ft.ScrollMode.HIDDEN,
                    controls=[
                        name_field,
                        document_field,
                        birth_certificate_field,
                        passport_field,
                        ft.Text("Lugar de Destino del Viaje"),
                        destination_field,
                        purpose_field,
                        departure_date_field,
                        return_date_field,
                        birth_date_field,
                        ft.Text("Información del Padre"),
                        father_name_field,
                        father_id_field,
                        father_phone_field,
                        is_father_deceased,
                        father_death_fields,
                        ft.Text("Información de la Madre"),
                        mother_name_field,
                        mother_id_field,
                        mother_phone_field,
                        is_mother_deceased,
                        mother_death_fields,
                        ft.Text("Departamento de Residencia del menor"),
                        department_dropdown,
                        ft.Text("Ciudad de Residencia del menor"),
                        city_dropdown,
                        save_button,
                    ],
                ),
            ),
        ],
    )
    return container
